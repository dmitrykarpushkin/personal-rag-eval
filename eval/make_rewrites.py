"""Fill the multi-query rewrite cache for every answerable gold question, in parallel.

  python eval/make_rewrites.py [--workers 4]

Writes to PRAG_MQ_CACHE (default eval/results/rewrites.jsonl); questions already in the cache are skipped. Needs a
logged-in `claude` CLI.
"""
import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "eval"))
from prag import multiquery as mq  # noqa: E402
from run_retrieval import load_gold  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    cache = mq._load()
    todo = [q["question"] for q in load_gold() if q["answerable"]
            and (mq.MODEL, mq.N_REWRITES, q["question"]) not in cache]
    print(f"{len(todo)} questions to rewrite", flush=True)
    with ThreadPoolExecutor(a.workers) as pool:
        recs = list(pool.map(mq.generate, todo))
    mq.CACHE.parent.mkdir(parents=True, exist_ok=True)
    with mq.CACHE.open("a", encoding="utf-8") as fh:
        for r in recs:
            if r["rewrites"]:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    bad = [r for r in recs if len(r["rewrites"]) < mq.N_REWRITES]
    print(f"written {len(recs) - len([r for r in recs if not r['rewrites']])}, short or failed {len(bad)}")
    for r in bad[:5]:
        print(" ", r["question"][:60], r.get("error", r["rewrites"]))


if __name__ == "__main__":
    main()
