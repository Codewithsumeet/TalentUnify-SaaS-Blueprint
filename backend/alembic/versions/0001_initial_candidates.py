"""Initial candidates table

Revision ID: 0001
Revises:
Create Date: 2026-03-14
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSON

revision      = '0001'
down_revision = None
branch_labels = None
depends_on    = None


def upgrade() -> None:
    # BUG FIX 8: pgcrypto is required for gen_random_uuid() on Postgres 15 alpine.
    # uuid-ossp is an alternative but pgcrypto is pre-bundled in the official image.
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    op.create_table(
        'candidates',
        sa.Column(
            'id',
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text('gen_random_uuid()'),
            nullable=False,
        ),
        sa.Column('name',             sa.String(255), nullable=True),

        # BUG FIX 9: unique=True prevents two concurrent workers inserting
        # the same email at the same millisecond (race condition in dedup).
        # The DB itself is now the last line of defense.
        sa.Column('email',            sa.String(255), nullable=True, unique=True),

        sa.Column('phone',            sa.String(50),  nullable=True),
        sa.Column('location',         sa.String(255), nullable=True),
        sa.Column('linkedin_url',     sa.String(500), nullable=True),
        sa.Column('github_url',       sa.String(500), nullable=True),
        sa.Column('current_role',     sa.String(255), nullable=True),
        sa.Column('current_company',  sa.String(255), nullable=True),
        sa.Column('experience_years', sa.Float(),     nullable=True),
        sa.Column('experience_level', sa.String(50),  nullable=True),
        sa.Column('skills',           JSON, server_default='[]', nullable=False),
        sa.Column('all_experience',   JSON, server_default='[]', nullable=False),
        sa.Column('certifications',   JSON, server_default='[]', nullable=False),
        sa.Column('candidate_bio',    sa.Text(),      nullable=True),
        sa.Column('sources',          JSON, server_default='[]', nullable=False),
        sa.Column('github_enrichment',JSON,           nullable=True),
        sa.Column('parse_quality',    sa.String(20),  server_default='high'),
        sa.Column('pinecone_index',   sa.String(50),  nullable=True),
        sa.Column('created_at',       sa.DateTime(),  server_default=sa.text('now()')),
        sa.Column('updated_at',       sa.DateTime(),  server_default=sa.text('now()')),
    )
    op.create_index('ix_candidates_email',            'candidates', ['email'],            unique=True)
    op.create_index('ix_candidates_experience_level', 'candidates', ['experience_level'], unique=False)
    op.create_index('ix_candidates_location',         'candidates', ['location'],         unique=False)


def downgrade() -> None:
    op.drop_table('candidates')
    op.execute("DROP EXTENSION IF EXISTS pgcrypto")
