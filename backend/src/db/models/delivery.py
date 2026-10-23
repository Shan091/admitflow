"""Encrypted durable non-conversation deliveries and payment-event deduplication."""

import uuid
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base, IdMixin, TenantMixin, TimestampMixin


class OutboundMessage(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "outbound_messages"
    __table_args__ = (
        UniqueConstraint("tenant_id", "dedup_key", name="uq_outbound_tenant_dedup"),
        ForeignKeyConstraint(
            ["tenant_id", "lead_id"],
            ["leads.tenant_id", "leads.id"],
            ondelete="CASCADE",
            name="fk_outbound_lead_owner",
        ),
        CheckConstraint(
            "status IN ('queued','sending','sent','failed','uncertain')",
            name="outbound_message_status",
        ),
    )
    lead_id: Mapped[uuid.UUID] = mapped_column(index=True, nullable=False)
    dedup_key: Mapped[str] = mapped_column(String(128), nullable=False)
    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    payload_enc: Mapped[str] = mapped_column(Text, nullable=False, deferred=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="queued")
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error_code: Mapped[str | None] = mapped_column(String(64))
    next_attempt_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    telegram_message_id: Mapped[int | None] = mapped_column(BigInteger)


class PaymentEvent(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "payment_events"
    __table_args__ = (
        UniqueConstraint("tenant_id", "body_digest", name="uq_payment_event_body"),
        ForeignKeyConstraint(
            ["tenant_id", "payment_order_id"],
            ["payment_orders.tenant_id", "payment_orders.id"],
            ondelete="CASCADE",
            name="fk_payment_event_order_owner",
        ),
    )
    payment_order_id: Mapped[uuid.UUID] = mapped_column(nullable=False, index=True)
    body_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    kind: Mapped[str] = mapped_column(String(64), nullable=False)
