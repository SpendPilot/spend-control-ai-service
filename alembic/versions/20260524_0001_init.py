"""initial ai schema

Revision ID: 20260524_0001
Revises:
Create Date: 2026-05-24
"""

import sqlalchemy as sa

from alembic import op

revision = "20260524_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS ai")
    op.create_table(
        "ai_conversations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        schema="ai",
    )
    op.create_table(
        "ai_messages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("conversation_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["conversation_id"], ["ai.ai_conversations.id"], ondelete="CASCADE"),
        schema="ai",
    )


def downgrade() -> None:
    op.drop_table("ai_messages", schema="ai")
    op.drop_table("ai_conversations", schema="ai")
    op.execute("DROP SCHEMA IF EXISTS ai CASCADE")

