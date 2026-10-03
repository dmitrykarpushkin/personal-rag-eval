"""prag CLI: `index` a notebook folder into Postgres, `search` it.

  python -m prag.cli index corpus/ [--reset]
  python -m prag.cli search "when is my dentist appointment" [--system hybrid+rerank] [-k 5]
"""
import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

from . import retrieve, store
from .chunk import load_corpus


def cmd_index(a):
    root = Path(a.root)
    t = time.perf_counter()
    notes, chunks = load_corpus(root)
    conn = store.connect()
    store.init(conn, reset=a.reset)
    # Incremental: re-embed only chunks whose text changed.
    have = {(p, o): h for p, o, h in conn.execute("SELECT path, ord, md5(body) FROM chunks").fetchall()}
    todo = [c for c in chunks if have.get((c.path, c.ord)) != hashlib.md5(c.text.encode()).hexdigest()]
    from .models import embed_many
    vecs = embed_many([store.embed_text(c) for c in todo]) if todo else []
    store.upsert(conn, todo, vecs)
    live = {(c.path, c.ord) for c in chunks}
    gone = [k for k in have if k not in live]
    for p, o in gone:
        conn.execute("DELETE FROM chunks WHERE path=%s AND ord=%s", (p, o))
    print(json.dumps({"notes": len(notes), "chunks": len(chunks), "embedded": len(todo), "deleted": len(gone),
                      "seconds": round(time.perf_counter() - t, 1)}))


def cmd_search(a):
    conn = store.connect() if a.system != "grep" else None
    hits, secs = retrieve.run(a.system, conn, Path(a.root), a.query, a.k)
    for h in hits[:a.k]:
        print(f"{h['score']:.3f}  {h['path']}  ({h['created']})  {h['body'][:160]!r}")
    print(f"-- {secs*1000:.0f} ms", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(prog="prag")
    sub = ap.add_subparsers(required=True)
    i = sub.add_parser("index"); i.add_argument("root"); i.add_argument("--reset", action="store_true")
    i.set_defaults(fn=cmd_index)
    s = sub.add_parser("search"); s.add_argument("query"); s.add_argument("--system", default="hybrid+rerank")
    s.add_argument("-k", type=int, default=5); s.add_argument("--root", default="corpus"); s.set_defaults(fn=cmd_search)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
