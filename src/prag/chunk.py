"""Split markdown notes into retrieval chunks.

A note is split on markdown headings; long sections are cut into windows of ~MAX_WORDS words with a small
overlap. Every chunk carries the note path, its date and title, so the answer step can reason about recency.
"""
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import yaml

MAX_WORDS = 220
OVERLAP = 40
FM = re.compile(r"^---\n(.*?)\n---\n?", re.S)
HEADING = re.compile(r"^#{1,6}\s+(.*)$", re.M)
CYR = re.compile(r"[а-яё]", re.I)
LAT = re.compile(r"[a-z]", re.I)


@dataclass
class Note:
    path: str
    created: str
    source: str
    tags: list[str]
    title: str
    body: str


@dataclass
class Chunk:
    path: str
    ord: int
    created: str
    title: str
    heading: str
    text: str
    lang: str = "en"
    meta: dict = field(default_factory=dict)


def load_note(root: Path, p: Path) -> Note:
    raw = redact(p.read_text(encoding="utf-8", errors="replace"))
    meta, body = {}, raw
    m = FM.match(raw)
    if m:
        try:
            meta = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            meta = {}
        body = raw[m.end():]
    h = HEADING.search(body)
    title = h.group(1).strip() if h else p.stem
    created = str(meta.get("created") or "")[:10]
    if not created:
        d = re.search(r"\d{4}-\d{2}-\d{2}", p.name)
        created = d.group(0) if d else ""
    if not created and os.environ.get("PRAG_DATE_FROM_MTIME") == "1":  # real notebooks; meaningless on a fresh checkout
        created = datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).date().isoformat()
    tags = meta.get("tags") or []
    return Note(str(p.relative_to(root)), created, str(meta.get("source") or ""),
                [str(t) for t in tags] if isinstance(tags, list) else [str(tags)], title, body.strip())


def lang_of(text: str) -> str:
    c, l = len(CYR.findall(text)), len(LAT.findall(text))
    return "ru" if c > l else "en"


def _windows(words: list[str]):
    if len(words) <= MAX_WORDS:
        yield words
        return
    step = MAX_WORDS - OVERLAP
    for i in range(0, len(words), step):
        yield words[i:i + MAX_WORDS]
        if i + MAX_WORDS >= len(words):
            break


def chunk_note(n: Note) -> list[Chunk]:
    sections, last, heading = [], 0, ""
    for m in HEADING.finditer(n.body):
        if m.start() > last:
            sections.append((heading, n.body[last:m.start()]))
        heading, last = m.group(1).strip(), m.end()
    sections.append((heading, n.body[last:]))
    out = []
    for heading, text in sections:
        words = text.split()
        if not words:
            continue
        for w in _windows(words):
            t = " ".join(w)
            out.append(Chunk(n.path, len(out), n.created, n.title, heading, t, lang_of(t)))
    if not out:
        out.append(Chunk(n.path, 0, n.created, n.title, "", n.title, lang_of(n.title)))
    return out


# Folders that are never notes (real notebooks live next to code and build output).
SKIP_DIRS = {".git", "node_modules", "dist", "build", ".venv", "venv", "__pycache__", ".next"}
# Lines that look like credentials are dropped before indexing: raw captures sometimes contain them.
SECRET = re.compile(r"(?i)(api[_-]?key|token|secret|password|passwd|пароль)\s*[:=]|"
                    r"\b(sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|xox[abp]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16}|"
                    r"\d{8,10}:[A-Za-z0-9_-]{30,})")


def redact(text: str) -> str:
    return "\n".join("[line removed: looks like a credential]" if SECRET.search(l) else l for l in text.split("\n"))


def note_paths(root: Path, exclude: tuple[str, ...] = ()) -> list[Path]:
    out = []
    for p in sorted(root.rglob("*.md")):
        rel = p.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts[:-1]):
            continue
        if any(rel.match(g) or str(rel).startswith(g.rstrip("/") + "/") for g in exclude):
            continue
        out.append(p)
    return out


def load_corpus(root: Path, exclude: tuple[str, ...] = ()) -> tuple[list[Note], list[Chunk]]:
    notes = [load_note(root, p) for p in note_paths(root, exclude)]
    chunks = [c for n in notes for c in chunk_note(n)]
    return notes, chunks


def header(c: Chunk) -> str:
    """Context line the embedder and the answer model see in front of the chunk text."""
    parts = [c.path, c.created, c.title]
    if c.heading and c.heading != c.title:
        parts.append(c.heading)
    return " | ".join(p for p in parts if p)
