"""
Pinecone dual-index client.

Two indexes are maintained — dimensions CANNOT be mixed in one index:
  PINECONE_INDEX_MAIN  → 1536-dim  (OpenAI text-embedding-3-small)
  PINECONE_INDEX_LOCAL → 384-dim   (all-MiniLM-L6-v2 local fallback)

BUG FIX 7: dimension is derived from the ACTUAL embedding model name,
not from the EMBEDDING_DIM env var. The env var can lie (e.g. default 1536
while the model is actually local/384). The model name never lies.
"""
import os
from functools import lru_cache

from pinecone import Pinecone, ServerlessSpec

from config import get_settings

settings = get_settings()

_pc_instance: Pinecone | None = None


def _get_pc() -> Pinecone:
    global _pc_instance
    if _pc_instance is None:
        _pc_instance = Pinecone(api_key=settings.pinecone_api_key)
    return _pc_instance


def _model_is_local() -> bool:
    """True when the local fallback model is active."""
    model = os.getenv("EMBEDDING_MODEL", settings.embedding_model)
    return model.lower() in ("local", "all-minilm-l6-v2")


def active_index() -> str:
    """Returns the correct Pinecone index name for the current embedding model."""
    return settings.pinecone_index_local if _model_is_local() else settings.pinecone_index_main


def active_dim() -> int:
    """
    BUG FIX 7: Returns dimension derived from ACTUAL model, not env var.
    all-MiniLM-L6-v2 → 384
    text-embedding-3-small → 1536
    """
    return 384 if _model_is_local() else 1536


def _ensure_index(name: str, dim: int) -> None:
    """Creates the Pinecone index if it doesn't already exist."""
    pc       = _get_pc()
    existing = [idx.name for idx in pc.list_indexes()]
    if name not in existing:
        pc.create_index(
            name=name,
            dimension=dim,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region=settings.pinecone_env),
        )


@lru_cache(maxsize=2)
def _get_index(name: str):
    return _get_pc().Index(name)


def _resolve(index_name: str | None):
    """Resolve None → active index, ensure it exists, return Index object."""
    name = index_name or active_index()
    dim  = active_dim()
    _ensure_index(name, dim)
    return _get_index(name)


async def upsert(
    candidate_id: str,
    embedding:    list[float],
    metadata:     dict,
    index_name:   str | None = None,
) -> None:
    """Upsert a single candidate vector."""
    _resolve(index_name).upsert(vectors=[{
        "id":       str(candidate_id),
        "values":   embedding,
        "metadata": metadata,
    }])


async def query(
    vector:     list[float],
    top_k:      int          = 20,
    filter:     dict | None  = None,
    index_name: str | None   = None,
):
    """ANN search. Returns raw Pinecone QueryResponse."""
    return _resolve(index_name).query(
        vector=vector,
        top_k=top_k,
        include_metadata=True,
        filter=filter,
    )


async def delete(
    candidate_id: str,
    index_name:   str | None = None,
) -> None:
    """Delete a candidate vector from the index."""
    _resolve(index_name).delete(ids=[str(candidate_id)])


async def upsert_candidate(candidate_id: str, embedding: list[float], metadata: dict, index_name: str | None = None) -> None:
    """Backward-compatible wrapper."""
    await upsert(candidate_id, embedding, metadata, index_name)


async def query_index(vector: list[float], top_k: int = 20, filter: dict | None = None, index_name: str | None = None):
    """Backward-compatible wrapper."""
    return await query(vector, top_k=top_k, filter=filter, index_name=index_name)


async def delete_candidate(candidate_id: str, index_name: str | None = None) -> None:
    """Backward-compatible wrapper."""
    await delete(candidate_id, index_name)
