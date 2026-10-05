"""Local embedding and reranking models (CPU, free, no paid APIs).

Embeddings: intfloat/multilingual-e5-large (1024-d, Russian + English), which expects "query: " / "passage: "
prefixes. Reranker: BAAI/bge-reranker-v2-m3 cross-encoder (multilingual). Both load from Hugging Face by name,
or from a local folder via PRAG_EMBED_MODEL / PRAG_RERANK_MODEL. Another embedder needs its own index (its own
PRAG_DSN database) and PRAG_EMBED_DIM; the "query: " / "passage: " prefixes are used only for E5 models
(PRAG_EMBED_PREFIX=e5|none overrides).
"""
import os
from functools import lru_cache

EMBED_MODEL = os.environ.get("PRAG_EMBED_MODEL", "intfloat/multilingual-e5-large")
RERANK_MODEL = os.environ.get("PRAG_RERANK_MODEL", "BAAI/bge-reranker-v2-m3")
DIM = int(os.environ.get("PRAG_EMBED_DIM", "1024"))
E5_PREFIX = os.environ.get("PRAG_EMBED_PREFIX", "e5" if "e5" in EMBED_MODEL.lower() else "none") == "e5"


@lru_cache(1)
def _embedder():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(EMBED_MODEL, device="cpu")


@lru_cache(1)
def _reranker():
    from sentence_transformers import CrossEncoder
    return CrossEncoder(RERANK_MODEL, device="cpu", max_length=512)


def embed_many(texts: list[str], kind: str = "passage", batch_size: int = 16) -> list:
    prefix = ("query: " if kind == "query" else "passage: ") if E5_PREFIX else ""
    return list(_embedder().encode([prefix + t for t in texts], batch_size=batch_size,
                                   normalize_embeddings=True, show_progress_bar=len(texts) > 50))


def embed_one(text: str, kind: str = "query"):
    return embed_many([text], kind)[0]


def rerank(query: str, docs: list[str]) -> list[float]:
    return [float(s) for s in _reranker().predict([(query, d) for d in docs], batch_size=8)]
