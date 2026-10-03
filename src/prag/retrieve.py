"""Retrievers. Each returns a ranked list of chunk dicts (path, ord, created, title, heading, body, score)."""
import re
import time
from pathlib import Path

import numpy as np

from . import models

COLS = "path, ord, created, title, heading, body"
STOP = set("""a an the of to in on at for and or is are was were be been do does did what which who whom when where why how
my her his their our your mara mara's she he it this that these those with from by about as into than then there any
now current currently still did does i me you we they get got has have had will would can could should""".split())


def _rows(cur, rows, score_idx=None):
    out = []
    for r in rows:
        d = dict(zip(["path", "ord", "created", "title", "heading", "body"], r[:6]))
        d["created"] = str(d["created"] or "")
        d["score"] = float(r[6]) if len(r) > 6 else 0.0
        out.append(d)
    return out


BM25_SQL = """
WITH q AS (SELECT unnest(%(lex)s::text[]) AS word),
idf AS (
  SELECT q.word, ln(1 + (cs.n - coalesce(ts.ndoc, 0) + 0.5) / (coalesce(ts.ndoc, 0) + 0.5)) AS idf
  FROM q CROSS JOIN corpus_stats cs LEFT JOIN term_stats ts ON ts.word = q.word
),
scored AS (
  SELECT c.id,
         sum(idf.idf * (u.tf * (%(k1)s + 1)) / (u.tf + %(k1)s * (1 - %(b)s + %(b)s * c.len / cs.avglen))) AS s
  FROM chunks c
  CROSS JOIN corpus_stats cs
  JOIN LATERAL (SELECT lexeme, coalesce(array_length(positions, 1), 1)::float AS tf
                FROM unnest(c.tsv) WHERE lexeme = ANY(%(lex)s::text[])) u ON true
  JOIN idf ON idf.word = u.lexeme
  WHERE c.tsv @@ to_tsquery('simple', %(tsq)s)
  GROUP BY c.id
)
SELECT c.path, c.ord, c.created, c.title, c.heading, c.body, scored.s
FROM scored JOIN chunks c USING (id) ORDER BY scored.s DESC LIMIT %(k)s
"""


def lexical(conn, q: str, k: int = 50) -> list[dict]:
    """BM25 over Postgres full-text lexemes (English + Russian stems), computed in SQL."""
    lex = conn.execute(
        "SELECT array(SELECT DISTINCT unnest(tsvector_to_array(to_tsvector('english', %s) || to_tsvector('russian', %s))))",
        (q, q)).fetchone()[0]
    lex = [w for w in lex if w not in STOP]
    if not lex:
        return []
    tsq = " | ".join("'" + w.replace("'", "''") + "'" for w in lex)
    rows = conn.execute(BM25_SQL, {"lex": lex, "tsq": tsq, "k1": 1.2, "b": 0.75, "k": k}).fetchall()
    return _rows(None, rows)


def dense(conn, q: str, k: int = 50) -> list[dict]:
    v = np.array(models.embed_one(q, "query"), dtype=np.float32)
    rows = conn.execute(
        f"SELECT {COLS}, 1 - (embedding <=> %s) AS s FROM chunks ORDER BY embedding <=> %s LIMIT %s",
        (v, v, k)).fetchall()
    return _rows(None, rows)


def rrf(*lists: list[dict], k: int = 60, top: int = 50) -> list[dict]:
    """Reciprocal rank fusion of several ranked chunk lists."""
    score, keep = {}, {}
    for lst in lists:
        for rank, d in enumerate(lst):
            key = (d["path"], d["ord"])
            score[key] = score.get(key, 0.0) + 1.0 / (k + rank + 1)
            keep.setdefault(key, d)
    ranked = sorted(score, key=score.get, reverse=True)[:top]
    return [{**keep[key], "score": score[key]} for key in ranked]


def _minmax(lst: list[dict]) -> dict:
    if not lst:
        return {}
    s = [d["score"] for d in lst]
    lo, hi = min(s), max(s)
    return {(d["path"], d["ord"]): ((d["score"] - lo) / (hi - lo) if hi > lo else 1.0) for d in lst}


ALPHA = 0.7  # weight of the dense score; picked on the hand-written half of the gold set (see README)


def hybrid(conn, q: str, k: int = 50) -> list[dict]:
    """Convex fusion of min-max normalised BM25 and dense scores.

    Plain RRF was tried first and lost to dense alone (hit@5 0.77 vs 0.87): BM25 returns plenty of
    loosely matching chunks, and RRF rewards chunks that appear in both lists over a clear dense winner.
    """
    L, D = lexical(conn, q, k), dense(conn, q, k)
    nl, nd = _minmax(L), _minmax(D)
    keep = {(d["path"], d["ord"]): d for d in L + D}
    ranked = sorted(keep, key=lambda key: -(ALPHA * nd.get(key, 0.0) + (1 - ALPHA) * nl.get(key, 0.0)))[:k]
    return [{**keep[key], "score": ALPHA * nd.get(key, 0.0) + (1 - ALPHA) * nl.get(key, 0.0)} for key in ranked]


def hybrid_rrf(conn, q: str, k: int = 50) -> list[dict]:
    return rrf(lexical(conn, q, k), dense(conn, q, k), top=k)


def hybrid_rerank(conn, q: str, k: int = 50, pool: int = 30) -> list[dict]:
    cands = hybrid(conn, q, pool)
    if not cands:
        return []
    docs = [f"{d['path']} | {d['created']} | {d['title']}\n{d['body']}" for d in cands]
    scores = models.rerank(q, docs)
    for d, s in zip(cands, scores):
        d["score"] = float(s)
    return sorted(cands, key=lambda d: d["score"], reverse=True)[:k]


# ---- naive grep baseline: what an agent's first `grep -ril <keywords>` gives you ----

_corpus_cache: dict = {}


def grep(root: Path, q: str, k: int = 50) -> list[dict]:
    """Rank whole notes by how many distinct query keywords they contain (case-insensitive substring)."""
    if root not in _corpus_cache:
        _corpus_cache[root] = {str(p.relative_to(root)): p.read_text(encoding="utf-8").lower()
                               for p in sorted(root.rglob("*.md"))}
    terms = [t for t in re.findall(r"[\w'-]+", q.lower()) if t not in STOP and len(t) > 2]
    scored = []
    for path, text in _corpus_cache[root].items():
        hits = sum(1 for t in set(terms) if t in text)
        if hits:
            scored.append((hits, text.count(terms[0]) if terms else 0, path))
    scored.sort(reverse=True)
    return [{"path": p, "ord": 0, "created": "", "title": "", "heading": "",
             "body": _corpus_cache[root][p][:1500], "score": float(h)} for h, _, p in scored[:k]]


SYSTEMS = {
    "grep": None,  # handled specially (needs corpus root, not db)
    "lexical": lexical,
    "dense": dense,
    "hybrid-rrf": hybrid_rrf,
    "hybrid": hybrid,
    "hybrid+rerank": hybrid_rerank,
}


def run(system: str, conn, root: Path, q: str, k: int = 50) -> tuple[list[dict], float]:
    t = time.perf_counter()
    hits = grep(root, q, k) if system == "grep" else SYSTEMS[system](conn, q, k)
    return hits, time.perf_counter() - t


def notes_ranked(hits: list[dict]) -> list[str]:
    seen, out = set(), []
    for h in hits:
        if h["path"] not in seen:
            seen.add(h["path"])
            out.append(h["path"])
    return out
