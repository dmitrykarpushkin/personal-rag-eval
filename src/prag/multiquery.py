"""Multi-query retrieval: a small model rewrites the question into a few search queries, hybrid search runs for the
question and each rewrite, and the score lists are summed (CombSUM over the convex hybrid scores).

Rewrites come from the `claude` CLI (`claude -p`, PRAG_MQ_MODEL, Haiku by default) and are cached in a JSONL file
(PRAG_MQ_CACHE), so a retrieval run is repeatable and its latency excludes the model call; the cache keeps the
model's wall time per question. The fusion rule and the number of rewrites were fixed before the eval run.
"""
import json
import os
import re
import subprocess
import time
from pathlib import Path

N_REWRITES = int(os.environ.get("PRAG_MQ_N", "3"))
MODEL = os.environ.get("PRAG_MQ_MODEL", "claude-haiku-4-5-20251001")
CACHE = Path(os.environ.get("PRAG_MQ_CACHE", Path(__file__).resolve().parents[2] / "eval/results/rewrites.jsonl"))

PROMPT = """You turn a question about someone's personal notes into search queries for a hybrid (keyword +
semantic) search engine. The notes are in English and Russian.
Write {n} different search queries for the question below: use other words and likely synonyms, name the kind of
note the answer would be in, and write at least one query in the other language (Russian if the question is in
English, English if it is in Russian). Do not answer the question and do not invent facts.
Output exactly {n} lines, one query per line, nothing else.

Question: {q}"""

LIST_MARK = re.compile(r"^\s*(?:[-*•]|\d{1,2}[.)])\s+")  # "1. ", "2) ", "- " in front of a query

_cache: dict | None = None


def _load() -> dict:
    global _cache
    if _cache is None:
        _cache = {}
        if CACHE.exists():
            for line in CACHE.open(encoding="utf-8"):
                if line.strip():
                    r = json.loads(line)
                    _cache[(r["model"], r["n"], r["question"])] = r
    return _cache


def generate(q: str, n: int = N_REWRITES, model: str = MODEL) -> dict:
    """Ask the model for n rewrites (no cache). Returns {question, model, n, rewrites, wall_s[, error]}."""
    cmd = ["claude", "-p", "--model", model, "--tools", "", "--strict-mcp-config", "--setting-sources", "",
           "--no-session-persistence", "--output-format", "json"]
    t = time.perf_counter()
    p = subprocess.run(cmd, input=PROMPT.format(n=n, q=q), capture_output=True, text=True, cwd="/tmp", timeout=300)
    rec = {"question": q, "model": model, "n": n, "wall_s": round(time.perf_counter() - t, 2), "rewrites": []}
    try:
        d = json.loads(p.stdout)
        rec["raw"] = d.get("result") or ""
        lines = [LIST_MARK.sub("", ln).strip() for ln in rec["raw"].splitlines()]
        rec["rewrites"] = [ln for ln in lines if ln][:n]
        rec["cost_usd"] = d.get("total_cost_usd")
    except json.JSONDecodeError:
        rec["error"] = (p.stderr or p.stdout)[-300:]
    return rec


def rewrites(q: str, n: int = N_REWRITES, model: str = MODEL) -> list[str]:
    cache = _load()
    if (model, n, q) not in cache:
        rec = generate(q, n, model)
        if rec["rewrites"]:
            CACHE.parent.mkdir(parents=True, exist_ok=True)
            with CACHE.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        cache[(model, n, q)] = rec
    return cache[(model, n, q)]["rewrites"]


def hybrid_multi(conn, q: str, k: int = 50) -> list[dict]:
    from .retrieve import hybrid
    keep, score = {}, {}
    for query in [q] + rewrites(q):
        for d in hybrid(conn, query, k):
            key = (d["path"], d["ord"])
            keep.setdefault(key, d)
            score[key] = score.get(key, 0.0) + d["score"]
    ranked = sorted(score, key=lambda key: -score[key])[:k]
    return [{**keep[key], "score": score[key]} for key in ranked]
