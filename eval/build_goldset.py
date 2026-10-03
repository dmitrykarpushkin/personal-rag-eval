"""Build eval/goldset.jsonl from spec/world.yaml and check it against the generated corpus.

Checks (all mechanical):
  - every gold/distractor note exists;
  - for answerable questions, every required answer pattern matches the union of gold notes;
  - for temporal questions, the distractor note does NOT match the required answer (it must hold the old value).
"""
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpus"


def main():
    w = yaml.safe_load((ROOT / "spec/world.yaml").read_text())
    out, problems, warnings = [], [], []
    for f in w["facts"]:
        gold = list((f.get("gold") or {}).keys())
        distr = list((f.get("distractors") or {}).keys())
        for p in gold + distr:
            if not (CORPUS / p).exists():
                problems.append(f"{f['id']}: missing note {p}")
        answerable = f["cat"] != "unanswerable"
        if answerable:
            text = "\n".join((CORPUS / p).read_text() for p in gold if (CORPUS / p).exists())
            for pat in f["a"]:
                if not re.search(pat, text, re.I):
                    problems.append(f"{f['id']}: pattern {pat!r} not found in gold notes {gold}")
            if f["cat"] == "temporal":
                for p in distr:
                    if (CORPUS / p).exists() and all(re.search(pat, (CORPUS / p).read_text(), re.I) for pat in f["a"]):
                        warnings.append(f"{f['id']}: distractor {p} also mentions the current answer (check by hand)")
        out.append({"id": f["id"], "category": f["cat"], "question": f["q"], "answerable": answerable,
                    "answer_patterns": f.get("a", []), "gold_notes": gold, "distractor_notes": distr})
    with open(ROOT / "eval/goldset.jsonl", "w") as fh:
        for r in out:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{len(out)} questions written; {len(problems)} problems")
    for p in problems:
        print("  -", p)
    for p in warnings:
        print("  warn:", p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
