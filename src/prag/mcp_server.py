"""MCP server exposing the notebook search as a tool for agents (agentic retrieval).

The agent keeps its own tools (Grep/Read) and gets one more: `search_notes`, hybrid retrieval over the index.
Runs as a long-lived HTTP server so the embedding model loads once:

  python -m prag.mcp_server            # http://127.0.0.1:8765/mcp
"""
import os

from mcp.server.fastmcp import FastMCP

from . import retrieve, store

PORT = int(os.environ.get("PRAG_MCP_PORT", "8765"))
SYSTEM = os.environ.get("PRAG_MCP_RETRIEVER", "hybrid")

mcp = FastMCP("notes", host="127.0.0.1", port=PORT)
_conn = None


def conn():
    global _conn
    if _conn is None or _conn.closed:
        _conn = store.connect()
    return _conn


@mcp.tool()
def search_notes(query: str, k: int = 8) -> str:
    """Semantic + keyword search over the user's notes (English and Russian). Works with paraphrases and
    across languages. Returns the best matching passages with note path and date; open a note with Read
    for full context. Prefer this over grep when you don't know the exact words used in the notes."""
    hits, _ = retrieve.run(SYSTEM, conn(), None, query, max(1, min(k, 20)))
    return "\n\n".join(f"[{i + 1}] {h['path']} (date: {h['created']})\n{h['body'][:900]}"
                       for i, h in enumerate(hits[:k])) or "no matches"


if __name__ == "__main__":
    retrieve.dense(conn(), "warm up", 1)
    mcp.run(transport="streamable-http")
