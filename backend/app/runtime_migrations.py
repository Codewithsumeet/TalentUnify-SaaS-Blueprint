from sqlalchemy import inspect
from sqlalchemy.engine import Connection


def ensure_candidate_source_column(sync_connection: Connection) -> None:
    inspector = inspect(sync_connection)
    if "candidates" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("candidates")}
    if "source" not in columns:
        sync_connection.exec_driver_sql(
            "ALTER TABLE candidates ADD COLUMN source VARCHAR(50)"
        )
        columns.add("source")

    if sync_connection.dialect.name == "postgresql" and "sources" in columns:
        sync_connection.exec_driver_sql(
            """
            UPDATE candidates
            SET source = COALESCE(source, NULLIF((sources::jsonb ->> 0), ''))
            WHERE source IS NULL
            """
        )
