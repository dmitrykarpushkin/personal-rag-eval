"""Summarize eval/results/answers.jsonl into eval/results/answers.md.

Rates carry 95% bootstrap intervals over questions (eval/stats.py). When a system was run several times
(`run_answers.py --repeat N`, rows carry "run"), a question's score is its mean over runs, and a separate table
shows per-run accuracy and how often a question flips between right and wrong.
"""
import json
import statistics as st
from collections import defaultdict
from pathlib import Path

from stats import bootstrap_ci, fmt_ci, fmt_diff, paired_diff_ci

ROOT = Path(__file__).resolve().parent.parent
ORDER = ["agentic-grep", "agent+search", "full-context", "rag:lexical", "rag:dense", "rag:hybrid", "rag:hybrid+rerank"]
BASELINE = "agentic-grep"


def per_question(rows, key="correct") -> dict:
    """{question id: mean of `key` over that question's runs}."""
    acc = defaultdict(list)
    for r in rows:
        acc[r["id"]].append(float(bool(r[key])))
    return {q: st.mean(v) for q, v in acc.items()}


def runs_of(rows) -> dict:
    by = defaultdict(list)
    for r in rows:
        by[r.get("run", 0)].append(r)
    return dict(sorted(by.items()))


def flip_rate(rows) -> float:
    """Share of questions whose correctness is not the same in every run (0 with a single run)."""
    outcomes = defaultdict(set)
    for r in rows:
        outcomes[r["id"]].add(bool(r["correct"]))
    return st.mean(len(v) > 1 for v in outcomes.values()) if outcomes else float("nan")


def build(rows) -> list[str]:
    by = defaultdict(list)
    for r in rows:
        by[r["system"]].append(r)
    systems = [s for s in ORDER if s in by] + [s for s in by if s not in ORDER]
    ans = lambda rs: [r for r in rs if r["category"] != "unanswerable"]  # noqa: E731
    una = lambda rs: [r for r in rs if r["category"] == "unanswerable"]  # noqa: E731
    mean = lambda xs: st.mean(xs) if xs else float("nan")  # noqa: E731
    L = ["| system | accuracy (all), 95% CI | answerable correct | says \"not found\" when it should | "
         "wrongly says \"not found\" | cites a gold note | median s | median input tokens | mean cost $ |",
         "|---|---|---|---|---|---|---|---|---|"]
    for s in systems:
        rs = by[s]
        a, u = ans(rs), una(rs)
        n_q, n_runs = len({r["id"] for r in rs}), len(runs_of(rs))
        size = f"n={n_q}" + (f" × {n_runs} runs" if n_runs > 1 else "")
        L.append(f"| {s} | {fmt_ci(*bootstrap_ci(per_question(rs).values()))} ({size}) | "
                 f"{mean([r['correct'] for r in a]):.2f} | {mean([r['correct'] for r in u]):.2f} | "
                 f"{mean([r['abstained'] for r in a]):.2f} | {mean([bool(r['cited_gold']) for r in a]):.2f} | "
                 f"{st.median((r.get('wall_s') or 0) + (r.get('retrieval_s') or 0) for r in rs):.1f} | "
                 f"{st.median(r.get('input_tokens') or 0 for r in rs):,.0f} | "
                 f"{mean([r.get('cost_usd') or 0 for r in rs]):.3f} |")
    if BASELINE in by and len(systems) > 1:
        base = per_question(by[BASELINE])
        L += ["", f"Paired difference in accuracy vs {BASELINE} (same questions, 95% bootstrap CI; "
              "* = the interval excludes 0):", "", "| system | difference | questions |", "|---|---|---|"]
        for s in systems:
            if s != BASELINE:
                d, lo, hi, n = paired_diff_ci(per_question(by[s]), base)
                L.append(f"| {s} | {fmt_diff(d, lo, hi)} | {n} |")
    repeated = [s for s in systems if len(runs_of(by[s])) > 1]
    if repeated:
        L += ["", "Repeated runs (same questions, same settings):", "",
              "| system | runs | accuracy per run | mean ± sd | questions that flip |", "|---|---|---|---|---|"]
        for s in repeated:
            accs = [st.mean(bool(r["correct"]) for r in rs) for rs in runs_of(by[s]).values()]
            sd = st.stdev(accs) if len(accs) > 1 else 0.0
            L.append(f"| {s} | {len(accs)} | {' / '.join(f'{x:.3f}' for x in accs)} | "
                     f"{st.mean(accs):.3f} ± {sd:.3f} | {flip_rate(by[s]):.1%} |")
    cats = sorted({r["category"] for r in rows})
    first = by[systems[0]]
    L += ["", "Accuracy by question type:", "",
          "| system | " + " | ".join(f"{c} (n={len({r['id'] for r in first if r['category'] == c})})" for c in cats)
          + " |", "|---|" + "---|" * len(cats)]
    for s in systems:
        L.append(f"| {s} | " + " | ".join(f"{mean([r['correct'] for r in by[s] if r['category'] == c]):.2f}"
                                           for c in cats) + " |")
    return L


def main(tag: str = ""):
    rows = [json.loads(line) for line in (ROOT / f"eval/results/answers{tag}.jsonl").open()]
    L = build(rows)
    (ROOT / f"eval/results/answers{tag}.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    import sys

    main(sys.argv[1] if len(sys.argv) > 1 else "")
