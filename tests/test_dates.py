"""Date filters, the recency term and the 'current value' detector, without Postgres or models."""

import os
from datetime import date
from pathlib import Path

import pytest

from prag import retrieve
from prag.chunk import load_note
from prag.dates import Recency, asks_for_current, in_range, recency, rerank_by_recency

TODAY = date(2026, 9, 30)


def hit(path, created, score):
    return {"path": path, "ord": 0, "created": created, "title": "", "heading": "", "body": "", "score": score}


@pytest.mark.parametrize("q", ["What is Mara's current hourly rate?", "Which flat did she finally choose?",
                               "Is she still running with the club?", "Где Мара сейчас работает?",
                               "Какой последний план по переезду?", "What is the latest version of the plan?"])
def test_detects_questions_about_the_current_value(q):
    assert asks_for_current(q)


@pytest.mark.parametrize("q", ["What is the name of Mara's Portuguese tutor?", "When did she visit Porto in 2025?",
                               "Which studio fires her pottery?", "Как зовут её репетитора?"])
def test_ignores_other_questions(q):
    assert not asks_for_current(q)


def test_recency_halves_every_half_life_and_ignores_undated():
    assert recency("2026-09-30", TODAY, 90) == 1.0
    assert recency("2026-07-02", TODAY, 90) == pytest.approx(0.5)
    assert recency("2026-10-05", TODAY, 90) == 1.0  # future dates count as today
    assert recency("", TODAY, 90) == 0.0 and recency("not a date", TODAY, 90) == 0.0


def test_recency_lifts_the_newer_of_two_similar_notes():
    old = hit("money/2026-03-01-rate.md", "2026-03-01", 0.92)
    new = hit("money/2026-07-01-rate-renewal.md", "2026-07-01", 0.88)
    other = hit("people/ines.md", "", 0.50)
    cfg = Recency(mode="always", weight=0.3, half_life_days=90, today=TODAY)
    out = rerank_by_recency([old, new, other], cfg)
    assert [h["path"] for h in out][:2] == ["money/2026-07-01-rate-renewal.md", "money/2026-03-01-rate.md"]
    assert out[0]["relevance"] == pytest.approx((0.88 - 0.5) / (0.92 - 0.5))
    assert rerank_by_recency([], cfg) == []


def test_weight_zero_keeps_relevance_order():
    hits = [hit("a", "2020-01-01", 0.9), hit("b", "2026-09-29", 0.8)]
    out = rerank_by_recency(hits, Recency(mode="always", weight=0.0, today=TODAY))
    assert [h["path"] for h in out] == ["a", "b"]


def test_modes(monkeypatch):
    assert Recency(mode="off").applies("current rate?") is False
    assert Recency(mode="always").applies("tutor's name?") is True
    assert Recency(mode="auto").applies("current rate?") and not Recency(mode="auto").applies("tutor's name?")
    monkeypatch.setenv("PRAG_RECENCY", "sometimes")
    with pytest.raises(ValueError):
        Recency.from_env()
    monkeypatch.setenv("PRAG_RECENCY", "always")
    monkeypatch.setenv("PRAG_RECENCY_WEIGHT", "0.5")
    monkeypatch.setenv("PRAG_RECENCY_HALF_LIFE_DAYS", "30")
    monkeypatch.setenv("PRAG_TODAY", "2026-01-15")
    cfg = Recency.from_env()
    assert (cfg.mode, cfg.weight, cfg.half_life_days, cfg.today) == ("always", 0.5, 30.0, date(2026, 1, 15))


def test_in_range():
    assert in_range("2026-05-01", None, None) and in_range("", None, None)
    assert in_range("2026-05-01", date(2026, 5, 1), date(2026, 5, 31))
    assert not in_range("2026-04-30", date(2026, 5, 1), None)
    assert not in_range("", date(2026, 5, 1), None)  # undated chunks drop out once a filter is set


def test_hybrid_dated_reranks_only_current_questions(monkeypatch):
    cands = [hit("old.md", "2026-01-10", 0.9), hit("new.md", "2026-09-20", 0.7), hit("x.md", "", 0.1)]
    seen = {}

    def fake_hybrid(conn, q, k, since=None, until=None):
        seen.update(k=k, since=since, until=until)
        return cands

    monkeypatch.setattr(retrieve, "hybrid", fake_hybrid)
    cfg = Recency(mode="auto", weight=0.4, half_life_days=60, today=TODAY)
    assert [h["path"] for h in retrieve.hybrid_dated(None, "What is the current plan?", 2, recency=cfg)] == [
        "new.md", "old.md"]
    assert [h["path"] for h in retrieve.hybrid_dated(None, "What was the plan?", 2, recency=cfg)] == [
        "old.md", "new.md"]
    retrieve.hybrid_dated(None, "q", 5, since=date(2026, 1, 1), until=date(2026, 6, 30), recency=cfg)
    assert seen == {"k": 50, "since": date(2026, 1, 1), "until": date(2026, 6, 30)}  # wide pool, filters passed on


def test_note_date_falls_back_to_mtime_only_when_asked(tmp_path: Path, monkeypatch):
    p = tmp_path / "people.md"
    p.write_text("# People\nnames")
    os.utime(p, (1_790_000_000, 1_790_000_000))  # 2026-09-21
    assert load_note(tmp_path, p).created == ""
    monkeypatch.setenv("PRAG_DATE_FROM_MTIME", "1")
    assert load_note(tmp_path, p).created == "2026-09-21"
