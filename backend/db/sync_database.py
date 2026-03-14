from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import get_settings

settings = get_settings()

sync_engine = create_engine(
    settings.sync_database_url,
    future=True,
    pool_pre_ping=True,
    echo=settings.debug,
)

SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
)
