"""Encrypted durable conversation inbox, reply outbox, memory and human requests."""

import uuid
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base, IdMixin, TenantMixin, TimestampMixin


class ConversationEvent(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "conversation_events"
    __table_args__ = (
        UniqueConstraint("bot_id", "update_id", name="uq_conversation_bot_update"),
        UniqueConstraint("tenant_id", "id", name="uq_conversation_event_tenant_id"),
        ForeignKeyConstraint(
            ["tenant_id", "bot_id", "identity_id", "lead_id"],
            [
                "telegram_identities.tenant_id",
                "telegram_identities.bot_id",
                "telegram_identities.id",
                "telegram_identities.lead_id",
            ],
            ondelete="CASCADE",
            name="fk_event_identity_owner",
        ),
        CheckConstraint("status IN ('queued','done')", name="conversation_event_status"),
    )
    bot_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    identity_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    lead_id: Mapped[uuid.UUID] = mapped_column(index=True, nullable=False)
    update_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    kind: Mapped[str] = mapped_column(String(16), nullable=False)
    payload_enc: Mapped[str] = mapped_column(Text, nullable=False, deferred=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="queued")


class ConversationReply(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "conversation_replies"
    __table_args__ = (
        UniqueConstraint("event_id", name="uq_conversation_reply_event"),
        ForeignKeyConstraint(
            ["tenant_id", "event_id"],
            ["conversation_events.tenant_id", "conversation_events.id"],
            ondelete="CASCADE",
            name="fk_reply_event_owner",
        ),
        CheckConstraint(
            "status IN ('queued','sending','sent','failed','uncertain')",
            name="conversation_reply_status",
        ),
    )
    event_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    payload_enc: Mapped[str] = mapped_column(Text, nullable=False, deferred=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="queued")
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error_code: Mapped[str | None] = mapped_column(String(48))
    telegram_message_id: Mapped[int | None] = mapped_column(BigInteger)
    next_attempt_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class ConversationMemory(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "conversation_memories"
    __table_args__ = (
        UniqueConstraint("tenant_id", "lead_id", name="uq_conversation_memory_lead"),
        ForeignKeyConstraint(
            ["tenant_id", "lead_id"],
            ["leads.tenant_id", "leads.id"],
            ondelete="CASCADE",
            name="fk_memory_lead_owner",
        ),
    )
    lead_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    payload_enc: Mapped[str] = mapped_column(Text, nullable=False)


class HumanRequest(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "human_requests"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "lead_id"],
            ["leads.tenant_id", "leads.id"],
            ondelete="CASCADE",
            name="fk_human_request_lead_owner",
        ),
        CheckConstraint(
            "status IN ('open','acknowledged','resolved','resumed')", name="human_request_status"
        ),
        Index(
            "uq_human_request_pending",
            "tenant_id",
            "lead_id",
            unique=True,
            postgresql_where=text("status != 'resumed'"),
        ),
    )
    lead_id: Mapped[uuid.UUID] = mapped_column(index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="open")
