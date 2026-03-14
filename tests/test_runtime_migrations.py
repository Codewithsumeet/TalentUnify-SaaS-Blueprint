from sqlalchemy import create_engine, inspect

from app.runtime_migrations import ensure_candidate_source_column


def test_ensure_candidate_source_column_adds_column_when_missing():
    engine = create_engine("sqlite:///:memory:")
    try:
        with engine.begin() as connection:
            connection.exec_driver_sql(
                """
                CREATE TABLE candidates (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    sources TEXT
                )
                """
            )

            ensure_candidate_source_column(connection)
            columns = {column["name"] for column in inspect(connection).get_columns("candidates")}
    finally:
        engine.dispose()

    assert "source" in columns


def test_ensure_candidate_source_column_is_noop_without_candidates_table():
    engine = create_engine("sqlite:///:memory:")
    try:
        with engine.begin() as connection:
            ensure_candidate_source_column(connection)
    finally:
        engine.dispose()
