"""Postgres + pgvector store: one table of chunks with a full-text vector and an embedding."""
import os

import psycopg
from pgvector.psycopg import register_vector

from .chunk import Chunk, header
from .models import DIM

DSN = os.environ.get("PRAG_DSN", "postgresql://prag:prag@127.0.0.1:5433/prag")

SCHEMA = f"""
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS chunks (
  id        bigserial PRIMARY KEY,
  path      text NOT NULL,
  ord       int  NOT NULL,
  created   date,
  title     text,
  heading   text,
  lang      text,
  body      text NOT NULL,
  -- English and Russian stemming side by side: notes mix both languages.
  tsv       tsvector GENERATED ALWAYS AS (
              setweight(to_tsvector('english', coalesce(title,'') || ' ' || coalesce(heading,'')), 'A') ||
              to_tsvector('english', body) || to_tsvector('russian', body) || to_tsvector('simple', path)
            ) STORED,
  embedding vector({DIM}),
  UNIQUE (path, ord)
);
CREATE INDEX IF NOT EXISTS chunks_tsv ON chunks USING gin (tsv);
CREATE INDEX IF NOT EXISTS chunks_emb ON chunks USING hnsw (embedding vector_cosine_ops);
"""

def connect():
    conn = psycopg.connect(DSN, autocommit=True)
    conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
    register_vector(conn)
    return conn


def init(conn, reset: bool = False):
    if reset:
        conn.execute("DROP TABLE IF EXISTS chunks")
    conn.execute(SCHEMA)


def upsert(conn, chunks: list[Chunk], vectors):
    import numpy as np
    with conn.cursor() as cur:
        for c, v in zip(chunks, vectors):
            cur.execute(
                """INSERT INTO chunks (path, ord, created, title, heading, lang, body, embedding)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                   ON CONFLICT (path, ord) DO UPDATE SET created=EXCLUDED.created, title=EXCLUDED.title,
                     heading=EXCLUDED.heading, lang=EXCLUDED.lang, body=EXCLUDED.body, embedding=EXCLUDED.embedding""",
                (c.path, c.ord, c.created or None, c.title, c.heading, c.lang, c.text, np.array(v, dtype=np.float32)))


def embed_text(c: Chunk) -> str:
    return header(c) + "\n" + c.text
