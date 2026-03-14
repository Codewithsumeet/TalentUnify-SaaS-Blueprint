"""Phase 7 feature columns: merge, fraud, shortlist, interviews, tokens

Revision ID: 4f8a2b9c1d3e
Revises: 0001
Create Date: 2026-03-14
"""

from alembic import op
import sqlalchemy as sa

revision = "4f8a2b9c1d3e"
down_revision = "0001"
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


def _json_default(bind) -> sa.TextClause:
    if bind.dialect.name == "postgresql":
        return sa.text("'[]'::json")
    return sa.text("'[]'")


def upgrade() -> None:
    bind = op.get_bind()
    json_default = _json_default(bind)
    uuid_type = (
        sa.dialects.postgresql.UUID(as_uuid=True)
        if bind.dialect.name == "postgresql"
        else sa.String(36)
    )

    if _has_table(bind, "candidates"):
        candidate_columns = [
            sa.Column("status", sa.String(20), server_default="active", nullable=False),
            sa.Column("merged_into", sa.String(36), nullable=True),
            sa.Column("merged_by", sa.String(100), nullable=True),
            sa.Column("all_experience", sa.JSON, server_default=json_default, nullable=False),
            sa.Column("ai_score", sa.Integer, server_default="0", nullable=False),
            sa.Column("pipeline_stage", sa.String(50), server_default="applied", nullable=False),
            sa.Column("fraud_risk", sa.String(10), server_default="low", nullable=False),
            sa.Column("fraud_score", sa.Integer, server_default="10", nullable=False),
            sa.Column("fraud_signals", sa.JSON, server_default=json_default, nullable=False),
            sa.Column("shortlisted", sa.Boolean, server_default=sa.false(), nullable=False),
            sa.Column("shortlist_rule_id", sa.String(36), nullable=True),
            sa.Column("suggested_merge_id", sa.String(36), nullable=True),
        ]

        for column in candidate_columns:
            if not _has_column(bind, "candidates", column.name):
                op.add_column("candidates", column)

        if not _has_index(bind, "candidates", "ix_candidates_status"):
            op.create_index("ix_candidates_status", "candidates", ["status"])
        if not _has_index(bind, "candidates", "ix_candidates_shortlisted"):
            op.create_index("ix_candidates_shortlisted", "candidates", ["shortlisted"])
        if (
            _has_column(bind, "candidates", "created_at")
            and not _has_index(bind, "candidates", "ix_candidates_created_at")
        ):
            op.create_index("ix_candidates_created_at", "candidates", ["created_at"])
        if (
            _has_column(bind, "candidates", "pipeline_stage")
            and not _has_index(bind, "candidates", "ix_candidates_pipeline_stage")
        ):
            op.create_index("ix_candidates_pipeline_stage", "candidates", ["pipeline_stage"])

    if not _has_table(bind, "shortlist_rules"):
        op.create_table(
            "shortlist_rules",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("name", sa.String(200), nullable=False),
            sa.Column("role_target", sa.String(200), nullable=True),
            sa.Column("min_score", sa.Integer, server_default="70"),
            sa.Column("required_skills", sa.JSON, server_default=json_default),
            sa.Column("any_of_skills", sa.JSON, server_default=json_default),
            sa.Column("min_experience_years", sa.Float, server_default="0"),
            sa.Column("location_filter", sa.String(100), nullable=True),
            sa.Column("level_filter", sa.JSON, server_default=json_default),
            sa.Column("auto_apply", sa.Boolean, server_default=sa.false()),
            sa.Column("is_active", sa.Boolean, server_default=sa.true()),
            sa.Column("priority", sa.Integer, server_default="0"),
            sa.Column("match_count", sa.Integer, server_default="0"),
            sa.Column("created_at", sa.DateTime, server_default=sa.text("now()")),
            sa.Column("created_by", sa.String(100), nullable=True),
        )

    if not _has_table(bind, "scheduled_interviews"):
        op.create_table(
            "scheduled_interviews",
            sa.Column("id", uuid_type, primary_key=True),
            sa.Column(
                "candidate_id",
                uuid_type,
                sa.ForeignKey("candidates.id", ondelete="CASCADE"),
                nullable=False,
            ),
            sa.Column("event_type_uri", sa.String(500), nullable=True),
            sa.Column("calendly_link", sa.String(500), nullable=True),
            sa.Column("scheduling_link_uuid", sa.String(100), nullable=True),
            sa.Column("calendly_event_uri", sa.String(500), nullable=True),
            sa.Column("status", sa.String(20), server_default="link_created"),
            sa.Column("scheduled_at", sa.DateTime, nullable=True),
            sa.Column("invitee_name", sa.String(200), nullable=True),
            sa.Column("invitee_email", sa.String(200), nullable=True),
            sa.Column("created_at", sa.DateTime, server_default=sa.text("now()")),
        )

    if _has_table(bind, "scheduled_interviews"):
        if not _has_index(bind, "scheduled_interviews", "ix_scheduled_interviews_link_uuid"):
            op.create_index(
                "ix_scheduled_interviews_link_uuid",
                "scheduled_interviews",
                ["scheduling_link_uuid"],
            )
        if not _has_index(bind, "scheduled_interviews", "ix_scheduled_interviews_candidate_id"):
            op.create_index(
                "ix_scheduled_interviews_candidate_id",
                "scheduled_interviews",
                ["candidate_id"],
            )

    if not _has_table(bind, "integration_tokens"):
        op.create_table(
            "integration_tokens",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("service", sa.String(50), nullable=False),
            sa.Column("access_token", sa.Text, nullable=False),
            sa.Column("refresh_token", sa.Text, nullable=True),
            sa.Column("expires_at", sa.DateTime, nullable=True),
            sa.UniqueConstraint("service", name="uq_integration_tokens_service"),
        )

    if _has_table(bind, "integration_tokens") and not _has_index(
        bind, "integration_tokens", "ix_integration_tokens_service"
    ):
        op.create_index("ix_integration_tokens_service", "integration_tokens", ["service"])


def downgrade() -> None:
    bind = op.get_bind()

    if _has_table(bind, "integration_tokens"):
        if _has_index(bind, "integration_tokens", "ix_integration_tokens_service"):
            op.drop_index("ix_integration_tokens_service", table_name="integration_tokens")
        op.drop_table("integration_tokens")

    if _has_table(bind, "scheduled_interviews"):
        if _has_index(bind, "scheduled_interviews", "ix_scheduled_interviews_candidate_id"):
            op.drop_index("ix_scheduled_interviews_candidate_id", table_name="scheduled_interviews")
        if _has_index(bind, "scheduled_interviews", "ix_scheduled_interviews_link_uuid"):
            op.drop_index("ix_scheduled_interviews_link_uuid", table_name="scheduled_interviews")
        op.drop_table("scheduled_interviews")

    if _has_table(bind, "shortlist_rules"):
        op.drop_table("shortlist_rules")

    if _has_table(bind, "candidates"):
        for index_name in (
            "ix_candidates_status",
            "ix_candidates_shortlisted",
            "ix_candidates_created_at",
            "ix_candidates_pipeline_stage",
        ):
            if _has_index(bind, "candidates", index_name):
                op.drop_index(index_name, table_name="candidates")

        for column_name in (
            "suggested_merge_id",
            "shortlist_rule_id",
            "shortlisted",
            "fraud_signals",
            "fraud_score",
            "fraud_risk",
            "pipeline_stage",
            "ai_score",
            "all_experience",
            "merged_by",
            "merged_into",
            "status",
        ):
            if _has_column(bind, "candidates", column_name):
                op.drop_column("candidates", column_name)

