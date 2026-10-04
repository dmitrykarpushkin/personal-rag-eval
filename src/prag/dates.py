"""Date-aware retrieval: date filters and a recency term for questions about the current state of things.

Notes go stale: "what is my hourly rate" has an old answer in a March note and the current one in a July note,
and plain relevance ranks them about the same. Two tools, both off unless asked for:

- filters: `since` / `until` on the chunk date (front matter `created`, else a date in the file name, else, with
  PRAG_DATE_FROM_MTIME=1, the file's modification time);
- recency: final score = (1 - w) * relevance + w * 2^(-age / half_life), with age in days before `today`.
  In "auto" mode it applies only to questions that ask for the current, latest or final value.

Settings (env): PRAG_RECENCY = off | auto | always, PRAG_RECENCY_WEIGHT (w), PRAG_RECENCY_HALF_LIFE_DAYS,
PRAG_TODAY (YYYY-MM-DD; defaults to the real date).
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from datetime import date

CURRENT = re.compile(
    r"\b(current(ly)?|now|nowadays|latest|most recent|newest|still|anymore|final(ly)?|in the end|ended up|"
    r"at the moment|these days)\b"
    r"|сейчас|теперь|текущ|последн|в итоге|всё ещё|все еще|на данный момент",
    re.I,
)


def _today() -> date:
    v = os.environ.get("PRAG_TODAY")
    return date.fromisoformat(v) if v else date.today()


@dataclass(frozen=True)
class Recency:
    mode: str = "auto"  # off | auto | always
    weight: float = 0.3
    half_life_days: float = 90.0
    today: date = field(default_factory=_today)

    @classmethod
    def from_env(cls) -> Recency:
        mode = os.environ.get("PRAG_RECENCY", "auto")
        if mode not in ("off", "auto", "always"):
            raise ValueError(f"PRAG_RECENCY must be off, auto or always, not {mode!r}")
        return cls(mode=mode, weight=float(os.environ.get("PRAG_RECENCY_WEIGHT", cls.weight)),
                   half_life_days=float(os.environ.get("PRAG_RECENCY_HALF_LIFE_DAYS", cls.half_life_days)))

    def applies(self, question: str) -> bool:
        return self.mode == "always" or (self.mode == "auto" and asks_for_current(question))


def asks_for_current(question: str) -> bool:
    return bool(CURRENT.search(question))


def parse_date(v) -> date | None:
    if isinstance(v, date):
        return v
    try:
        return date.fromisoformat(str(v)[:10]) if v else None
    except ValueError:
        return None


def recency(created, today: date, half_life_days: float) -> float:
    """1.0 for today, 0.5 one half-life ago; undated chunks get 0 (no boost, no penalty beyond losing it)."""
    d = parse_date(created)
    if d is None:
        return 0.0
    age = max((today - d).days, 0)
    return 2.0 ** (-age / half_life_days)


def rerank_by_recency(hits: list[dict], cfg: Recency) -> list[dict]:
    """Blend each hit's relevance (min-max normalised over the list) with its recency."""
    if not hits:
        return []
    s = [h["score"] for h in hits]
    lo, hi = min(s), max(s)
    out = []
    for h in hits:
        rel = (h["score"] - lo) / (hi - lo) if hi > lo else 1.0
        out.append({**h, "relevance": rel,
                    "score": (1 - cfg.weight) * rel + cfg.weight * recency(h.get("created"), cfg.today,
                                                                          cfg.half_life_days)})
    return sorted(out, key=lambda h: -h["score"])


def in_range(created, since: date | None, until: date | None) -> bool:
    d = parse_date(created)
    if since is None and until is None:
        return True
    if d is None:
        return False
    return (since is None or d >= since) and (until is None or d <= until)
