import json
import subprocess

from prag import multiquery as mq
from prag import retrieve


def _hit(path, score):
    return {"path": path, "ord": 0, "created": "", "title": "", "heading": "", "body": "", "score": score}


def test_hybrid_multi_sums_scores_over_queries(monkeypatch):
    lists = {"q": [_hit("a.md", 1.0), _hit("b.md", 0.6)],
             "r1": [_hit("b.md", 1.0), _hit("c.md", 0.9)],
             "r2": [_hit("b.md", 0.8)]}
    monkeypatch.setattr(mq, "rewrites", lambda q: ["r1", "r2"])
    monkeypatch.setattr(retrieve, "hybrid", lambda conn, q, k=50: lists[q])
    out = mq.hybrid_multi(None, "q", 3)
    assert [d["path"] for d in out] == ["b.md", "a.md", "c.md"]
    assert abs(out[0]["score"] - 2.4) < 1e-9


def test_generate_parses_lines_and_strips_numbering(monkeypatch):
    res = {"result": "1. hourly rate\n- почасовая ставка\n\n3) rate contract\nextra", "total_cost_usd": 0.01}
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: subprocess.CompletedProcess(a, 0, json.dumps(res), ""))
    rec = mq.generate("What is my rate?", n=3)
    assert rec["rewrites"] == ["hourly rate", "почасовая ставка", "rate contract"]


def test_rewrites_uses_cache_without_calling_model(monkeypatch, tmp_path):
    cache = tmp_path / "rw.jsonl"
    cache.write_text(json.dumps({"question": "q", "model": "m", "n": 2, "rewrites": ["x", "y"]}) + "\n")
    monkeypatch.setattr(mq, "CACHE", cache)
    monkeypatch.setattr(mq, "_cache", None)
    monkeypatch.setattr(mq, "generate", lambda *a: (_ for _ in ()).throw(AssertionError("model called")))
    assert mq.rewrites("q", 2, "m") == ["x", "y"]


def test_generate_keeps_leading_numbers_that_are_part_of_the_query(monkeypatch):
    res = {"result": "2026 invoice hourly rate\n10 km race time"}
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: subprocess.CompletedProcess(a, 0, json.dumps(res), ""))
    assert mq.generate("q", n=2)["rewrites"] == ["2026 invoice hourly rate", "10 km race time"]
