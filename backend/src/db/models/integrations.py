"""Minimal committed events, per-user read receipts and a recoverable webhook outbox."""

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base, IdMixin, TenantMixin, TimestampMixin


class IntegrationEvent(IdMixin, TenantMixin, Base):
    __tablename__ = "integration_events"
    __table_args__ = (
        UniqueConstraint("tenant_id", "id", name="uq_integration_event_owner"),
        ForeignKeyConstraint(
            ["tenant_id", "lead_id"],
            ["leads.tenant_id", "leads.id"],
            ondelete="CASCADE",
            name="fk_integration_event_lead",
        ),
        Index("ix_integration_event_timeline", "tenant_id", "created_at", "id"),
    )
    lead_id: Mapped[uuid.UUID | None] = mapped_column()
    kind: Mapped[str] = mapped_column(String(64), nullable=False)
    state: Mapped[str | None] = mapped_column(String(32))
    notification: Mapped[str | None] = mapped_column(String(16))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class WebhookEndpoint(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "webhook_endpoints"
    __table_args__ = (
        UniqueConstraint("tenant_id"),
        UniqueConstraint("tenant_id", "id", name="uq_webhook_endpoint_owner"),
    )
    url_enc: Mapped[str] = mapped_column(Text, nullable=False)
    secret_enc: Mapped[str] = mapped_column(Text, nullable=False)
    display_host: Mapped[str] = mapped_column(String(255), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    generation: Mapped[uuid.UUID] = mapped_column(nullable=False, default=uuid.uuid4)


class WebhookDelivery(IdMixin, TenantMixin, TimestampMixin, Base):
    __tablename__ = "webhook_deliveries"
    __table_args__ = (
        UniqueConstraint("endpoint_id", "event_id", name="uq_webhook_delivery_event"),
        ForeignKeyConstraint(
            ["tenant_id", "endpoint_id"],
            ["webhook_endpoints.tenant_id", "webhook_endpoints.id"],
            ondelete="CASCADE",
            name="fk_webhook_delivery_endpoint",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "event_id"],
            ["integration_events.tenant_id", "integration_events.id"],
            ondelete="CASCADE",
            name="fk_webhook_delivery_event",
        ),
        CheckConstraint(
            "status IN ('queued','sending','sent','dead','cancelled')",
            name="webhook_delivery_status",
        ),
        Index("ix_webhook_delivery_due", "status", "next_attempt_at"),
    )
    endpoint_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    event_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    generation: Mapped[uuid.UUID] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="queued")
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    lease_id: Mapped[uuid.UUID | None] = mapped_column()
    next_attempt_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    error_code: Mapped[str | None] = mapped_column(String(48))


class NotificationReceipt(TenantMixin, Base):
    __tablename__ = "notification_receipts"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "user_id"],
            ["staff_users.tenant_id", "staff_users.id"],
            ondelete="CASCADE",
            name="fk_notification_receipt_user",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "event_id"],
            ["integration_events.tenant_id", "integration_events.id"],
            ondelete="CASCADE",
            name="fk_notification_receipt_event",
        ),
    )
    user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    event_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
