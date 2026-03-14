from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


def _resolve_env_file() -> str:
    config_file = Path(__file__).resolve()
    candidates = [
        Path.cwd() / ".env",
        config_file.parent / ".env",
        config_file.parent.parent / ".env",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    return ".env"


class Settings(BaseSettings):
    # Parsing
    llama_cloud_api_key: str = ""

    # LLM
    anthropic_api_key: str = ""

    # Embeddings
    openai_api_key: str = ""
    embedding_model: str = "text-embedding-3-small"
    embedding_dim: int = 1536

    # Pinecone — two separate indexes for different embedding dimensions
    pinecone_api_key: str = ""
    pinecone_env: str = "us-east-1"
    pinecone_index_main: str = "candidates"       # 1536-dim (OpenAI)
    pinecone_index_local: str = "candidates-local"  # 384-dim (MiniLM)

    # Task Queue
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"

    # Database
    # FastAPI async engine uses this directly (must start with postgresql+asyncpg://)
    database_url: str = "sqlite+aiosqlite:///./talentunify.db"

    # Gmail
    gmail_client_id: str = ""
    gmail_client_secret: str = ""
    gmail_redirect_uri: str = "http://localhost:8000/integration/gmail/callback"

    # Calendly
    calendly_personal_access_token: str = ""
    calendly_organization_uri: str = ""
    calendly_user_uri: str = ""
    calendly_mock_mode: bool = True

    # Demo
    demo_mode: bool = False

    model_config = SettingsConfigDict(
        env_file=_resolve_env_file(),
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
