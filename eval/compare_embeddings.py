"""Paired comparison of embedding models from separate retrieval runs, one index per model.

  python eval/compare_embeddings.py e5-large e5-base bge-m3

Reads eval/results/retrieval-emb-<model>.jsonl (dense and hybrid run against that model's index), merges them into
eval/results/retrieval-emb.jsonl with systems renamed to "<system>@<model>", writes the summary table to
eval/results/retrieval-emb.md and the paired differences against the first model to eval/results/compare-emb.md.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "eval"))
from compare_retrieval import compare  # noqa: E402
from run_retrieval import summarize  # noqa: E402

OUT = ROOT / "eval/results"


def main():
    models = sys.argv[1:] or ["e5-large", "e5-base", "bge-m3"]
    rows = []
    for m in models:
        for line in (OUT / f"retrieval-emb-{m}.jsonl").open():
            r = json.loads(line)
            r["system"] = f"{r['system']}@{m}"
            rows.append(r)
    with open(OUT / "retrieval-emb.jsonl", "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    import run_retrieval
    run_retrieval.TAG = "-emb"
    summarize(rows, OUT)
    base, L = models[0], []
    for system in ["dense", "hybrid"]:
        for m in models[1:]:
            L += [f"## {system}: {m} vs {base}", ""] + compare(rows, f"{system}@{base}", f"{system}@{m}")
    (OUT / "compare-emb.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
