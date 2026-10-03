"""Summarize eval/results/answers.jsonl into eval/results/answers.md."""
import json
import statistics as st
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORDER = ["agentic-grep", "agent+search", "full-context", "rag:lexical", "rag:dense", "rag:hybrid", "rag:hybrid+rerank"]


def main(tag: str = ""):
    rows = [json.loads(l) for l in (ROOT / f"eval/results/answers{tag}.jsonl").open()]
    by = defaultdict(list)
    for r in rows:
        by[r["system"]].append(r)
    systems = [s for s in ORDER if s in by] + [s for s in by if s not in ORDER]
    ans = lambda rs: [r for r in rs if r["category"] != "unanswerable"]  # noqa: E731
    una = lambda rs: [r for r in rs if r["category"] == "unanswerable"]  # noqa: E731
    mean = lambda xs: st.mean(xs) if xs else float("nan")  # noqa: E731
    L = ["| system | accuracy (all) | answerable correct | says \"not found\" when it should | wrongly says \"not found\" | "
         "cites a gold note | median s | median input tokens | mean cost $ |",
         "|---|---|---|---|---|---|---|---|---|"]
    for s in systems:
        rs = by[s]
        a, u = ans(rs), una(rs)
        L.append(f"| {s} | {mean([r['correct'] for r in rs]):.2f} (n={len(rs)}) | {mean([r['correct'] for r in a]):.2f} | "
                 f"{mean([r['correct'] for r in u]):.2f} | {mean([r['abstained'] for r in a]):.2f} | "
                 f"{mean([bool(r['cited_gold']) for r in a]):.2f} | "
                 f"{st.median((r.get('wall_s') or 0) + (r.get('retrieval_s') or 0) for r in rs):.1f} | "
                 f"{st.median(r.get('input_tokens') or 0 for r in rs):,.0f} | "
                 f"{mean([r.get('cost_usd') or 0 for r in rs]):.3f} |")
    cats = sorted({r["category"] for r in rows})
    L += ["", "Accuracy by question type:", "",
          "| system | " + " | ".join(f"{c} (n={len([r for r in by[systems[0]] if r['category']==c])})" for c in cats) + " |",
          "|---|" + "---|" * len(cats)]
    for s in systems:
        L.append(f"| {s} | " + " | ".join(f"{mean([r['correct'] for r in by[s] if r['category']==c]):.2f}" for c in cats) + " |")
    (ROOT / f"eval/results/answers{tag}.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else "")
