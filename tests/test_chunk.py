from pathlib import Path

from prag.chunk import chunk_note, load_corpus, load_note, redact


def test_redact_drops_credential_lines():
    text = "met Rui\napi_key = abc123\nbot 1234567890:AAAbbbcccdddeeefffggghhhiiijjjkkkl\nok"
    out = redact(text).split("\n")
    assert out[0] == "met Rui" and out[-1] == "ok"
    assert "abc123" not in redact(text) and "AAAbbb" not in redact(text)


def test_skip_dirs_and_exclude(tmp_path: Path):
    for rel in ["a.md", "node_modules/x/readme.md", "inbox/attachments/b.md", "inbox/c.md"]:
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("# t\nhello")
    notes, _ = load_corpus(tmp_path, ("inbox/attachments",))
    assert sorted(n.path for n in notes) == ["a.md", "inbox/c.md"]


def test_chunks_keep_date_and_headings(tmp_path: Path):
    p = tmp_path / "projects" / "2026-05-01-x.md"
    p.parent.mkdir(parents=True)
    p.write_text("---\ncreated: 2026-05-01T10:00:00\n---\n# Title\nintro\n## Part\n" + "word " * 500)
    n = load_note(tmp_path, p)
    cs = chunk_note(n)
    assert n.created == "2026-05-01" and n.title == "Title"
    assert len(cs) >= 3 and all(c.created == "2026-05-01" for c in cs)
    assert cs[-1].heading == "Part"
