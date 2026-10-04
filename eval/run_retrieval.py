"""Retrieval eval: for every answerable gold question and every retriever, where do the gold notes rank?

Metrics are note-level (a note counts as found if any of its chunks is retrieved):
  hit@k     - at least one gold note in the top-k notes
  recall@k  - share of gold notes in the top-k notes (matters for multi-note questions)
  mrr       - 1 / rank of the first gold note (0 if not in top 50)
"""
import json
import os
import statistics as st
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = Path(os.environ.get("PRAG_CORPUS", ROOT / "corpus")).resolve()
TAG = os.environ.get("PRAG_TAG", "")  # results suffix, e.g. "-xl"
sys.path.insert(0, str(ROOT / "src"))
from stats import bootstrap_ci, fmt_ci  # noqa: E402

ALL_SYSTEMS = ["grep", "lexical", "dense", "hybrid-rrf", "hybrid", "hybrid+dates", "hybrid+rerank"]
# PRAG_SYSTEMS=hybrid,hybrid+dates runs a subset (the full set includes the slow CPU reranker)
SYSTEMS = [s for s in os.environ.get("PRAG_SYSTEMS", "").split(",") if s] or [
    s for s in ALL_SYSTEMS if s != "hybrid+dates"]


def load_gold():
    qs = []
    for f in ["goldset.jsonl", "goldset_extra.jsonl"]:
        p = ROOT / "eval" / f
        if p.exists():
            qs += [json.loads(l) for l in p.open() if l.strip()]
    return qs


def main():
    from prag import retrieve, store

    qs = [q for q in load_gold() if q["answerable"]]
    conn = store.connect()
    retrieve.dense(conn, "warm up", 1)  # load the embedding model outside the timings
    if "hybrid+rerank" in SYSTEMS:
        retrieve.hybrid_rerank(conn, "warm up", 1, pool=2)
    out = ROOT / "eval/results"
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for q in qs:
        for s in SYSTEMS:
            hits, secs = retrieve.run(s, conn, CORPUS, q["question"], 50)
            notes = retrieve.notes_ranked(hits)
            gold = set(q["gold_notes"])
            ranks = [notes.index(g) + 1 for g in gold if g in notes]
            rows.append({"id": q["id"], "category": q["category"], "question": q["question"], "system": s,
                         "ms": round(secs * 1000, 1),
                         "first_rank": min(ranks) if ranks else None,
                         "top5": notes[:5],
                         **{f"hit@{k}": any(r <= k for r in ranks) for k in (1, 3, 5, 10)},
                         **{f"recall@{k}": sum(r <= k for r in ranks) / len(gold) for k in (5, 10)},
                         "mrr": 1 / min(ranks) if ranks else 0.0})
        print(q["id"], *(f"{r['system']}:{r['first_rank']}" for r in rows[-len(SYSTEMS):]), flush=True)
    with open(out / f"retrieval{TAG}.jsonl", "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    summarize(rows, out)


def summarize(rows, out):
    by = defaultdict(list)
    for r in rows:
        by[r["system"]].append(r)
    lines = ["| retriever | hit@1 | hit@5, 95% CI | recall@5 | recall@10 | MRR, 95% CI | median ms |",
             "|---|---|---|---|---|---|---|"]
    systems = [s for s in ALL_SYSTEMS if s in by] + [s for s in by if s not in ALL_SYSTEMS]
    for s in systems:
        rs = by[s]
        m = lambda k: st.mean(float(r[k]) for r in rs)  # noqa: E731
        ci = lambda k: fmt_ci(*bootstrap_ci([r[k] for r in rs]))  # noqa: E731
        lines.append(f"| {s} | {m('hit@1'):.2f} | {ci('hit@5')} | {m('recall@5'):.2f} | {m('recall@10'):.2f} | "
                     f"{ci('mrr')} | {st.median(r['ms'] for r in rs):.0f} |")
    cats = sorted({r["category"] for r in rows})
    lines += ["", "hit@5 by question type:", "",
              "| retriever | " + " | ".join(f"{c} (n={len([r for r in by[systems[0]] if r['category']==c])})" for c in cats) + " |",
              "|---|" + "---|" * len(cats)]
    for s in systems:
        cells = []
        for c in cats:
            rs = [r for r in by[s] if r["category"] == c]
            cells.append(f"{st.mean(float(r['hit@5']) for r in rs):.2f}")
        lines.append(f"| {s} | " + " | ".join(cells) + " |")
    (out / f"retrieval{TAG}.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    if "--summary-only" in sys.argv:  # rebuild the Markdown from the saved rows, no database or models
        out = ROOT / "eval/results"
        summarize([json.loads(line) for line in (out / f"retrieval{TAG}.jsonl").open()], out)
    else:
        main()
