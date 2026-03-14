"""Candidate notes table + pipeline stage compatibility guard.

Revision ID: 9c2d4f1a7b8e
Revises: 4f8a2b9c1d3e
Create Date: 2026-03-14
"""

from alembic import op
import sqlalchemy as sa

revision = "9c2d4f1a7b8e"
down_revision = "4f8a2b9c1d3e"
branch_labels = None
depends_on = None


def _has_table(bind, table_name: str) -> bool:
    return sa.inspect(bind).has_table(table_name)


def _has_column(bind, table_name: str, column_name: str) -> bool:
    inspector = sa.inspect(bind)
    return column_name in {column["name"] for column in inspector.get_columns(table_name)}


def _has_index(bind, table_name: str, index_name: str) -> bool:
    inspector = sa.inspect(bind)
    return index_name in {index["name"] for index in inspector.get_indexes(table_name)}


def upgrade() -> None:
    bind = op.get_bind()
    uuid_type = (
        sa.dialects.postgresql.UUID(as_uuid=True)
        if bind.dialect.name == "postgresql"
        else sa.String(36)
    )

    if _has_table(bind, "candidates") and not _has_column(bind, "candidates", "pipeline_stage"):
        op.add_column(
            "candidates",
            sa.Column("pipeline_stage", sa.String(50), server_default="applied", nullable=False),
        )
    if _has_table(bind, "candidates") and not _has_index(
        bind, "candidates", "ix_candidates_pipeline_stage"
    ):
        op.create_index("ix_candidates_pipeline_stage", "candidates", ["pipeline_stage"])

    if not _has_table(bind, "candidate_notes"):
        op.create_table(
            "candidate_notes",
            sa.Column("id", uuid_type, primary_key=True),
            sa.Column(
                "candidate_id",
                uuid_type,
                sa.ForeignKey("candidates.id", ondelete="CASCADE"),
                nullable=False,
            ),
            sa.Column("text", sa.Text(), nullable=False),
            sa.Column("author", sa.String(120), server_default="Recruiter", nullable=False),
            sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        )

    if _has_table(bind, "candidate_notes") and not _has_index(
        bind, "candidate_notes", "ix_candidate_notes_candidate_id"
    ):
        op.create_index(
            "ix_candidate_notes_candidate_id",
            "candidate_notes",
            ["candidate_id"],
        )


def downgrade() -> None:
    bind = op.get_bind()

    if _has_table(bind, "candidate_notes"):
        if _has_index(bind, "candidate_notes", "ix_candidate_notes_candidate_id"):
            op.drop_index("ix_candidate_notes_candidate_id", table_name="candidate_notes")
        op.drop_table("candidate_notes")
