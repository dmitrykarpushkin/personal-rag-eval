"""The gold set must stay consistent with the corpus it is scored against."""

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
FILES = ["goldset.jsonl", "goldset_extra.jsonl"]


def rows():
    out = []
    for f in FILES:
        p = ROOT / "eval" / f
        out += [(f, json.loads(line)) for line in p.read_text().splitlines() if line.strip()]
    return out


ROWS = rows()
NOTES = {str(p.relative_to(ROOT / "corpus")) for p in (ROOT / "corpus").rglob("*.md")}
ARCHIVE = {str(p.relative_to(ROOT / "archive")) for p in (ROOT / "archive").rglob("*.md")} if (ROOT / "archive").exists() else set()


def test_ids_are_unique_across_files():
    ids = [r["id"] for _, r in ROWS]
    assert len(ids) == len(set(ids)) == 119


@pytest.mark.parametrize("f,row", ROWS, ids=[r["id"] for _, r in ROWS])
def test_row_is_well_formed(f, row):
    assert {"id", "category", "question", "answerable", "answer_patterns", "gold_notes"} <= set(row)
    assert row["question"].strip()
    for pattern in row["answer_patterns"]:
        re.compile(pattern)
    if row["answerable"]:
        assert row["gold_notes"], "an answerable question needs at least one gold note"
        assert row["answer_patterns"], "an answerable question needs facts to check in the answer"
        missing = [n for n in row["gold_notes"] if n not in NOTES]
        assert not missing, f"gold notes not in corpus/: {missing}"
    else:
        assert not row["gold_notes"], "an unanswerable question must not point at a note"


def test_distractors_are_real_notes_and_not_gold():
    for _, row in ROWS:
        for n in row.get("distractor_notes", []):
            assert n in NOTES | ARCHIVE
            assert n not in row["gold_notes"]
