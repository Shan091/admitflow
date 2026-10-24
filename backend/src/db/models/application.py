"""Application form submissions and their payment orders."""

from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base, IdMixin, TenantMixin, TimestampMixin
from src.db.enums import ApplicationStatus, PaymentStatus


class Application(IdMixin, TenantMixin, TimestampMixin, Base):
    """Structured application data collected from an admission-ready lead (SPEC §7.9).

    Name/parent/address/ID-proof are ciphertext PII (encryption in Task 4).
    """

    __tablename__ = "applications"
    is_demo: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )

    lead_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"), index=True, nullable=False
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("courses.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    batch_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("batches.id", ondelete="SET NULL")
    )
    full_name_enc: Mapped[str] = mapped_column(Text, nullable=False)
    # New forms keep DOB/school and all remaining fields in encrypted storage.
    # Legacy plaintext columns remain nullable for historical row compatibility.
    form_data_enc: Mapped[str | None] = mapped_column(Text)
    dob: Mapped[date | None] = mapped_column(Date)
    parent_name_enc: Mapped[str | None] = mapped_column(Text)
    address_enc: Mapped[str | None] = mapped_column(Text)
    previous_school: Mapped[str | None] = mapped_column(String(255))
    id_proof_number_enc: Mapped[str | None] = mapped_column(Text)
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus, native_enum=False, length=16),
        nullable=False,
        default=ApplicationStatus.SUBMITTED,
    )
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    payment_orders: Mapped[list[PaymentOrder]] = relationship(back_populates="application")


class PaymentOrder(IdMixin, TenantMixin, TimestampMixin, Base):
    """A Razorpay order for an application fee (SPEC §7.10).

    Amount is DB-sourced minor units (paise), never LLM-decided (ADR-006).
    ``payment_link_sent`` is the replay guard that stops duplicate links.
    """

    __tablename__ = "payment_orders"
    __table_args__ = (
        UniqueConstraint("tenant_id", "id", name="uq_payment_order_tenant_id"),
        UniqueConstraint("tenant_id", "request_key", name="uq_payment_order_request"),
        UniqueConstraint("tenant_id", "razorpay_payment_id", name="uq_payment_provider_payment"),
        CheckConstraint(
            "creation_state IN ('legacy','queued','creating','created','failed','uncertain')",
            name="payment_creation_state",
        ),
    )

    request_key: Mapped[str | None] = mapped_column(String(64))
    is_demo: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    creation_state: Mapped[str] = mapped_column(String(16), nullable=False, default="legacy")
    creation_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    payment_url_enc: Mapped[str | None] = mapped_column(Text)
    last_error: Mapped[str | None] = mapped_column(String(64))
    next_attempt_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    lead_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"), index=True, nullable=False
    )
    application_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("applications.id", ondelete="CASCADE"), index=True, nullable=False
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("courses.id", ondelete="RESTRICT"), nullable=False
    )
    discount_code_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("discount_codes.id", ondelete="SET NULL")
    )
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="INR")
    razorpay_order_id: Mapped[str | None] = mapped_column(String(128), index=True)
    razorpay_payment_link_id: Mapped[str | None] = mapped_column(String(128))
    razorpay_payment_id: Mapped[str | None] = mapped_column(String(128))
    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus, native_enum=False, length=16),
        nullable=False,
        default=PaymentStatus.CREATED,
    )
    payment_link_sent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    webhook_event: Mapped[dict[str, Any] | None] = mapped_column(JSONB)

    application: Mapped[Application] = relationship(back_populates="payment_orders")
