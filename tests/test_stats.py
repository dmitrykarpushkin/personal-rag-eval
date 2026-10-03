import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "eval"))
from stats import bootstrap_ci, fmt_ci, fmt_diff, paired_diff_ci  # noqa: E402


def test_interval_contains_the_mean_and_is_reproducible():
    xs = [True] * 90 + [False] * 29
    mean, lo, hi = bootstrap_ci(xs, n_boot=2000)
    assert mean == pytest.approx(90 / 119)
    assert lo < mean < hi
    assert 0.6 < lo and hi < 0.9
    assert bootstrap_ci(xs, n_boot=2000) == (mean, lo, hi)  # fixed seed


def test_degenerate_and_empty():
    assert bootstrap_ci([1, 1, 1], n_boot=500) == (1.0, 1.0, 1.0)
    mean, lo, hi = bootstrap_ci([])
    assert mean != mean and lo != lo and hi != hi


def test_more_questions_give_a_narrower_interval():
    _, lo_small, hi_small = bootstrap_ci([1, 0] * 20, n_boot=2000)
    _, lo_big, hi_big = bootstrap_ci([1, 0] * 200, n_boot=2000)
    assert hi_big - lo_big < hi_small - lo_small


def test_paired_difference_uses_only_shared_questions():
    a = {f"q{i}": 1 for i in range(50)}
    b = {f"q{i}": (1 if i % 5 else 0) for i in range(50)} | {"extra": 0}
    diff, lo, hi, n = paired_diff_ci(a, b, n_boot=2000)
    assert n == 50 and diff == pytest.approx(0.2)
    assert lo > 0  # a is better on 10 questions and never worse: the interval excludes zero
    same = paired_diff_ci(a, a, n_boot=500)
    assert same[:3] == (0.0, 0.0, 0.0)


def test_formatting():
    assert fmt_ci(0.875, 0.81, 0.93) == "0.88 [0.81–0.93]"
    assert fmt_ci(float("nan"), 0, 0) == "–"
    assert fmt_diff(0.05, 0.01, 0.1) == "+0.05 [+0.01, +0.10] *"
    assert fmt_diff(0.01, -0.02, 0.04) == "+0.01 [-0.02, +0.04]"
