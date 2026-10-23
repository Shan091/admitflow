"""Add staff sessions and durable institution knowledge uploads."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b627da2f7e11"
down_revision: str | None = "8f4b1c2d3e60"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _timestamps() -> list[sa.Column[sa.DateTime]]:
    return [
        sa.Column(name, sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)
        for name in ("created_at", "updated_at")
    ]


def upgrade() -> None:
    op.add_column("institutions", sa.Column("slug", sa.String(64), nullable=True))
    op.create_unique_constraint("uq_institutions_slug", "institutions", ["slug"])
    op.create_unique_constraint("uq_staff_users_tenant_id_id", "staff_users", ["tenant_id", "id"])
    op.create_unique_constraint("uq_documents_tenant_id_id", "documents", ["tenant_id", "id"])
    op.create_table(
        "staff_sessions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("token_hash", sa.String(64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        *_timestamps(),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["tenant_id"], ["institutions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["tenant_id", "user_id"],
            ["staff_users.tenant_id", "staff_users.id"],
            ondelete="CASCADE",
            name="fk_staff_sessions_owner",
        ),
        sa.UniqueConstraint("token_hash"),
    )
    op.create_index("ix_staff_sessions_tenant_id", "staff_sessions", ["tenant_id"])
    op.create_table(
        "knowledge_uploads",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("uploaded_by", sa.Uuid(), nullable=False),
        sa.Column("filename", sa.String(255), nullable=False),
        sa.Column("relative_path", sa.String(500), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("source_enc", sa.LargeBinary(), nullable=False),
        sa.Column("byte_size", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("error_code", sa.String(48), nullable=True),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("attempt_id", sa.Uuid(), nullable=True),
        sa.Column("document_id", sa.Uuid(), nullable=True),
        sa.Column("chunk_count", sa.Integer(), nullable=False),
        *_timestamps(),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["tenant_id"], ["institutions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["tenant_id", "uploaded_by"],
            ["staff_users.tenant_id", "staff_users.id"],
            name="fk_knowledge_uploads_staff",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "document_id"],
            ["documents.tenant_id", "documents.id"],
            name="fk_knowledge_uploads_document",
        ),
        sa.UniqueConstraint("tenant_id", "content_hash", name="uq_knowledge_upload_content"),
        sa.CheckConstraint(
            "status IN ('queued','processing','ready','failed')",
            name=op.f("ck_knowledge_uploads_upload_status"),
        ),
    )
    op.create_index("ix_knowledge_uploads_tenant_id", "knowledge_uploads", ["tenant_id"])


def downgrade() -> None:
    if op.get_bind().scalar(sa.text("SELECT EXISTS (SELECT 1 FROM knowledge_uploads)")):
        raise RuntimeError("Export and remove uploaded knowledge before downgrading this schema")
    op.drop_table("knowledge_uploads")
    op.drop_table("staff_sessions")
    op.drop_constraint("uq_documents_tenant_id_id", "documents", type_="unique")
    op.drop_constraint("uq_staff_users_tenant_id_id", "staff_users", type_="unique")
    op.drop_constraint("uq_institutions_slug", "institutions", type_="unique")
    op.drop_column("institutions", "slug")
