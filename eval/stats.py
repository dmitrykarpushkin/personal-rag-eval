"""Bootstrap confidence intervals for per-question metrics (accuracy, hit@k, MRR).

119 questions is small: one question is 0.8 points of accuracy, so every rate in the reports carries a 95%
percentile-bootstrap interval, and comparisons between two systems use a paired bootstrap over the same
questions (resampling question ids, not rows, so the pairing survives).
"""
import random
import statistics as st

N_BOOT = 10_000
SEED = 7  # fixed: reports must not change from one regeneration to the next


def bootstrap_ci(values, n_boot=N_BOOT, alpha=0.05, seed=SEED):
    """(mean, low, high) of a list of numbers (booleans count as 0/1)."""
    xs = [float(v) for v in values]
    if not xs:
        return float("nan"), float("nan"), float("nan")
    rnd = random.Random(seed)
    n = len(xs)
    means = sorted(sum(xs[rnd.randrange(n)] for _ in range(n)) / n for _ in range(n_boot))
    lo = means[int(alpha / 2 * n_boot)]
    hi = means[min(n_boot - 1, int((1 - alpha / 2) * n_boot))]
    return st.mean(xs), lo, hi


def paired_diff_ci(a: dict, b: dict, n_boot=N_BOOT, alpha=0.05, seed=SEED):
    """Mean of a[q] - b[q] over the questions both systems answered, with a paired bootstrap interval.

    a, b: {question_id: value}. Returns (diff, low, high, n_questions).
    """
    ids = sorted(set(a) & set(b))
    diffs = [float(a[i]) - float(b[i]) for i in ids]
    mean, lo, hi = bootstrap_ci(diffs, n_boot, alpha, seed)
    return mean, lo, hi, len(ids)


def fmt_ci(mean, lo, hi, digits=2):
    if mean != mean:  # nan
        return "–"
    return f"{mean:.{digits}f} [{lo:.{digits}f}–{hi:.{digits}f}]"


def fmt_diff(diff, lo, hi, digits=2):
    sign = lambda x: f"{x:+.{digits}f}"  # noqa: E731
    mark = " *" if lo > 0 or hi < 0 else ""  # the interval excludes zero
    return f"{sign(diff)} [{sign(lo)}, {sign(hi)}]{mark}"
