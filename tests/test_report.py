import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "eval"))
from report import build, flip_rate, per_question, runs_of  # noqa: E402


def row(qid, system, correct, run=None, category="lookup"):
    r = {"id": qid, "system": system, "correct": correct, "category": category, "abstained": False,
         "cited_gold": correct, "wall_s": 1.0, "input_tokens": 100, "cost_usd": 0.01}
    if run is not None:
        r["run"] = run
    return r


def test_per_question_averages_runs():
    rows = [row("q1", "s", True, 0), row("q1", "s", False, 1), row("q2", "s", True, 0), row("q2", "s", True, 1)]
    assert per_question(rows) == {"q1": 0.5, "q2": 1.0}
    assert list(runs_of(rows)) == [0, 1]
    assert flip_rate(rows) == 0.5


def test_single_run_rows_without_a_run_field():
    rows = [row("q1", "s", True), row("q2", "s", False)]
    assert list(runs_of(rows)) == [0] and flip_rate(rows) == 0.0


def test_report_has_intervals_paired_differences_and_repeats():
    rows = []
    for i in range(40):
        rows.append(row(f"q{i}", "agentic-grep", True))
        rows.append(row(f"q{i}", "rag:hybrid", i % 4 != 0))  # wrong on 10 of 40
        for run in range(3):
            rows.append(row(f"q{i}", "full-context@haiku", not (i == 0 and run == 1), run))
    text = "\n".join(build(rows))
    assert "| agentic-grep | 1.00 [1.00–1.00] (n=40) |" in text
    assert "| rag:hybrid | 0.75 [" in text
    assert "| rag:hybrid | -0.25 [" in text and "] * | 40 |" in text  # clearly worse than the baseline
    assert "(n=40 × 3 runs)" in text
    assert "| full-context@haiku | 3 | 1.000 / 0.975 / 1.000 |" in text and "| 2.5% |" in text


def test_no_baseline_no_paired_table():
    text = "\n".join(build([row("q1", "rag:dense", True), row("q1", "rag:hybrid", False)]))
    assert "Paired difference" not in text and "Repeated runs" not in text
