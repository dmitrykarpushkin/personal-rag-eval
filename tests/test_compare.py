import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "eval"))
from compare_retrieval import compare, subsets  # noqa: E402


def row(qid, system, rank, category="lookup", question="What is it?"):
    return {"id": qid, "system": system, "category": category, "question": question, "first_rank": rank,
            "hit@5": bool(rank and rank <= 5), "mrr": 1 / rank if rank else 0.0}


def test_subsets_and_paired_table():
    rows = []
    for i in range(30):
        rows += [row(f"L{i}", "hybrid", 1), row(f"L{i}", "hybrid+dates", 1)]
    for i in range(10):  # temporal questions: the new note was at rank 6, recency brings it to 1
        q = "What is her current rate?" if i % 2 else "When is the appointment?"
        rows += [row(f"T{i}", "hybrid", 6, "temporal", q), row(f"T{i}", "hybrid+dates", 1, "temporal", q)]
    s = subsets(rows)
    assert len(s["all answerable"]) == 40 and len(s["temporal"]) == 10
    assert s["asks for the current value"] == {f"T{i}" for i in range(1, 10, 2)}
    text = "\n".join(compare(rows, "hybrid", "hybrid+dates"))
    assert "### all answerable (n=40)" in text and "### temporal (n=10)" in text
    assert "| hit@5 | 0.75 [" in text and "| +0.25 [" in text
    temporal = text.split("### temporal")[1].split("###")[0]
    assert "| +1.00 [+1.00, +1.00] * |" in temporal  # hit@5 goes 0 → 1 on every temporal question
    assert "T0 6→1" in text


def test_missing_system_is_an_error():
    import pytest

    with pytest.raises(SystemExit):
        compare([row("q", "hybrid", 1)], "hybrid", "hybrid+dates")
