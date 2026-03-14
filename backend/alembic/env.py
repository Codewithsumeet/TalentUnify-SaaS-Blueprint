import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from db.database import get_sync_db_url
from db import models  # noqa: F401 — registers models

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def _build_sync_url() -> str:
    """
    Build a psycopg2-compatible URL from environment variables.
    Works whether DATABASE_URL uses asyncpg or not.
    """
    raw = os.getenv(
        "DATABASE_URL",
        f"postgresql://{os.getenv('DB_USER','user')}:"
        f"{os.getenv('DB_PASS','pass')}@"
        f"{os.getenv('DB_HOST','localhost')}/"
        f"{os.getenv('DB_NAME','talentflow')}"
    )
    return get_sync_db_url(raw)


# Import Base AFTER models are registered
from db.base import Base
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = _build_sync_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    sync_url = _build_sync_url()
    # Override whatever is in alembic.ini with the runtime URL
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = sync_url

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # NullPool is mandatory for Alembic
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
