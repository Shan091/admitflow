"""Durable, institution-scoped upload jobs and hashed staff sessions."""

import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Integer,
    LargeBinary,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base, IdMixin, TenantMixin, TimestampMixin


class StaffSession(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "staff_sessions"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "user_id"],
            ["staff_users.tenant_id", "staff_users.id"],
            ondelete="CASCADE",
            name="fk_staff_sessions_owner",
        ),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class KnowledgeUpload(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "knowledge_uploads"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "uploaded_by"],
            ["staff_users.tenant_id", "staff_users.id"],
            ondelete="CASCADE",
            name="fk_knowledge_uploads_staff",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "document_id"],
            ["documents.tenant_id", "documents.id"],
            name="fk_knowledge_uploads_document",
        ),
        UniqueConstraint("tenant_id", "content_hash", name="uq_knowledge_upload_content"),
        CheckConstraint("status IN ('queued','processing','ready','failed')", name="upload_status"),
    )

    uploaded_by: Mapped[uuid.UUID] = mapped_column(nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    relative_path: Mapped[str] = mapped_column(String(500), nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    source_enc: Mapped[bytes] = mapped_column(LargeBinary, nullable=False, deferred=True)
    byte_size: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="queued")
    error_code: Mapped[str | None] = mapped_column(String(48))
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    attempt_id: Mapped[uuid.UUID | None] = mapped_column()
    document_id: Mapped[uuid.UUID | None] = mapped_column()
    chunk_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
