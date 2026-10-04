"""Paired comparison of two retrievers from a saved retrieval run, overall and on question subsets.

  PRAG_TAG=-dates python eval/compare_retrieval.py hybrid hybrid+dates

Reads eval/results/retrieval<TAG>.jsonl and writes eval/results/compare<TAG>.md: hit@5 and MRR for each system with
95% bootstrap intervals, and the paired difference B - A on the same questions. Subsets: all answerable questions,
the "temporal" category (the answer changed over time), and the questions the recency detector flags as asking
for the current value.
"""
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from prag.dates import asks_for_current  # noqa: E402
from stats import bootstrap_ci, fmt_ci, fmt_diff, paired_diff_ci  # noqa: E402

METRICS = ["hit@5", "mrr"]


def subsets(rows) -> dict:
    questions = {r["id"]: r for r in rows}
    return {
        "all answerable": set(questions),
        "temporal": {q for q, r in questions.items() if r["category"] == "temporal"},
        "asks for the current value": {q for q, r in questions.items() if asks_for_current(r.get("question", ""))},
    }


def compare(rows, a: str, b: str) -> list[str]:
    by = defaultdict(dict)
    for r in rows:
        by[r["system"]][r["id"]] = r
    if a not in by or b not in by:
        raise SystemExit(f"need both systems in the results, have: {sorted(by)}")
    L = [f"Paired comparison: {b} vs {a} (95% bootstrap intervals over questions; * = the interval excludes 0)", ""]
    for name, ids in subsets(rows).items():
        ids = sorted(ids & set(by[a]) & set(by[b]))
        if not ids:
            continue
        L += [f"### {name} (n={len(ids)})", "", f"| metric | {a} | {b} | {b} − {a} |", "|---|---|---|---|"]
        for m in METRICS:
            va = {q: float(by[a][q][m]) for q in ids}
            vb = {q: float(by[b][q][m]) for q in ids}
            d, lo, hi, _ = paired_diff_ci(vb, va)
            L.append(f"| {m} | {fmt_ci(*bootstrap_ci(va.values()))} | {fmt_ci(*bootstrap_ci(vb.values()))} | "
                     f"{fmt_diff(d, lo, hi)} |")
        moved = [(q, by[a][q]["first_rank"], by[b][q]["first_rank"]) for q in ids
                 if by[a][q]["first_rank"] != by[b][q]["first_rank"]]
        if moved:
            L += ["", "First gold rank changed: " + ", ".join(f"{q} {ra}→{rb}" for q, ra, rb in moved)]
        L.append("")
    return L


def main():
    a, b = (sys.argv[1:3] + ["hybrid", "hybrid+dates"][len(sys.argv[1:3]):])[:2]
    tag = os.environ.get("PRAG_TAG", "")
    rows = [json.loads(line) for line in (ROOT / f"eval/results/retrieval{tag}.jsonl").open()]
    L = compare(rows, a, b)
    (ROOT / f"eval/results/compare{tag}.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
