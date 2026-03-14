"""
Tier 5B embeddings.

PRIMARY:  OpenAI text-embedding-3-small → 1536-dim vectors → PINECONE_INDEX_MAIN
FALLBACK: all-MiniLM-L6-v2 (local, CPU, ~5ms) → 384-dim vectors → PINECONE_INDEX_LOCAL

IMPORTANT: These two models produce DIFFERENT dimension vectors.
They MUST be stored in SEPARATE Pinecone indexes (see pinecone_client.py).
Set EMBEDDING_MODEL=local in .env to force the fallback permanently.
The fallback also triggers automatically if the OpenAI call raises any exception.
"""
from functools import lru_cache
from config import get_settings

settings = get_settings()


@lru_cache(maxsize=1)
def _get_local_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")


async def get_embedding(text: str) -> list[float]:
    """
    Returns embedding vector for text.
    Automatically routes to correct model based on settings.
    """
    use_local = settings.embedding_model.lower() == "local"

    if not use_local:
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=settings.openai_api_key)
            resp   = await client.embeddings.create(
                model="text-embedding-3-small",
                input=text[:8191],
            )
            return resp.data[0].embedding
        except Exception:
            # Auto-fallback: OpenAI is down or rate-limited
            pass

    # Local fallback: all-MiniLM-L6-v2 (384-dim)
    model = _get_local_model()
    emb   = model.encode(text, normalize_embeddings=True)
    return emb.tolist()


def get_active_index_name() -> str:
    """
    Returns the correct Pinecone index name based on current embedding model.
    Call this everywhere you need to pick between the two indexes.
    """
    if settings.embedding_model.lower() == "local":
        return settings.pinecone_index_local
    return settings.pinecone_index_main


def get_active_embedding_dim() -> int:
    """Returns the vector dimension for the currently active embedding model."""
    if settings.embedding_model.lower() == "local":
        return 384
    return 1536
