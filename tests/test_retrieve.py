"""Fusion and the grep baseline, without Postgres or models: the retrievers are replaced with fixed lists."""

from pathlib import Path

import pytest

from prag import retrieve


def hit(path, ord_=0, score=0.0):
    return {"path": path, "ord": ord_, "created": "", "title": "", "heading": "", "body": path, "score": score}


def test_rrf_rewards_agreement_and_keeps_first_seen_fields():
    a = [hit("x.md"), hit("y.md"), hit("z.md")]
    b = [hit("y.md"), hit("w.md")]
    out = retrieve.rrf(a, b, k=60, top=10)
    assert [d["path"] for d in out][:2] == ["y.md", "x.md"]  # in both lists beats first in one
    assert out[0]["score"] == pytest.approx(1 / 62 + 1 / 61)
    assert len(retrieve.rrf(a, b, top=2)) == 2


def test_minmax_scales_to_unit_range_and_handles_ties():
    out = retrieve._minmax([hit("a", score=2.0), hit("b", score=4.0), hit("c", score=3.0)])
    assert out == {("a", 0): 0.0, ("b", 0): 1.0, ("c", 0): 0.5}
    assert retrieve._minmax([hit("a", score=5.0), hit("b", score=5.0)]) == {("a", 0): 1.0, ("b", 0): 1.0}
    assert retrieve._minmax([]) == {}


def test_hybrid_is_a_convex_blend_weighted_towards_dense(monkeypatch):
    # BM25 likes "lex.md", dense likes "den.md"; with ALPHA = 0.7 the dense winner stays on top.
    lex = [hit("lex.md", score=12.0), hit("both.md", score=6.0), hit("den.md", score=0.0)]
    den = [hit("den.md", score=0.9), hit("both.md", score=0.6), hit("lex.md", score=0.3)]
    monkeypatch.setattr(retrieve, "lexical", lambda conn, q, k, *a: lex)
    monkeypatch.setattr(retrieve, "dense", lambda conn, q, k, *a: den)
    out = retrieve.hybrid(None, "q", k=3)
    assert [d["path"] for d in out] == ["den.md", "both.md", "lex.md"]
    a = retrieve.ALPHA
    assert out[0]["score"] == pytest.approx(a * 1.0 + (1 - a) * 0.0)
    assert out[1]["score"] == pytest.approx(a * 0.5 + (1 - a) * 0.5)


def test_hybrid_keeps_chunks_found_by_only_one_retriever(monkeypatch):
    monkeypatch.setattr(retrieve, "lexical", lambda conn, q, k, *a: [hit("only-lex.md", score=3.0)])
    monkeypatch.setattr(retrieve, "dense", lambda conn, q, k, *a: [])
    assert [d["path"] for d in retrieve.hybrid(None, "q")] == ["only-lex.md"]


def test_notes_ranked_dedupes_chunks_of_the_same_note():
    hits = [hit("a.md", 0), hit("b.md", 0), hit("a.md", 3), hit("c.md", 1)]
    assert retrieve.notes_ranked(hits) == ["a.md", "b.md", "c.md"]


def test_grep_baseline_ranks_by_distinct_keywords(tmp_path: Path):
    (tmp_path / "people").mkdir()
    (tmp_path / "people" / "ines.md").write_text("Ines is my Portuguese tutor. Portuguese lessons on Tuesday.")
    (tmp_path / "trip.md").write_text("Lisbon trip, practise Portuguese.")
    (tmp_path / "other.md").write_text("Groceries.")
    out = retrieve.grep(tmp_path, "Who is my Portuguese tutor?")
    assert [d["path"] for d in out] == ["people/ines.md", "trip.md"]  # stop words ("who", "is", "my") ignored
    assert out[0]["score"] == 2.0


def test_run_dispatches_grep_without_a_connection(tmp_path: Path):
    (tmp_path / "a.md").write_text("dentist on friday")
    hits, secs = retrieve.run("grep", None, tmp_path, "dentist appointment", 5)
    assert [h["path"] for h in hits] == ["a.md"] and secs >= 0
