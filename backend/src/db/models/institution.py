"""Institution (the tenant root) and its staff users."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, CheckConstraint, Enum, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base, IdMixin, TenantMixin, TimestampMixin
from src.db.enums import StaffRole

if TYPE_CHECKING:
    from src.db.models.catalog import Course, DiscountCode
    from src.db.models.lead import Lead


class Institution(IdMixin, TimestampMixin, Base):
    """An institution, optionally connected to a legacy WhatsApp number.

    The tenant root: its ``id`` *is* the ``tenant_id`` every other table
    references, so it does not carry a ``tenant_id`` of its own (ADR-003).
    """

    __tablename__ = "institutions"
    __table_args__ = (
        CheckConstraint(
            "telegram_daily_send_limit BETWEEN 0 AND 100000",
            name="telegram_daily_send_limit_bounds",
        ),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str | None] = mapped_column(String(64), unique=True)
    # Meta's phone_number_id -> tenant. The webhook maps inbound messages by it.
    whatsapp_phone_number_id: Mapped[str | None] = mapped_column(String(64), unique=True)
    whatsapp_business_account_id: Mapped[str | None] = mapped_column(String(64))
    timezone: Mapped[str] = mapped_column(String(64), nullable=False, default="Asia/Kolkata")
    business_hours: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    reengagement_delay_days: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    telegram_daily_send_limit: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1000, server_default="1000"
    )
    retention_days: Mapped[int | None] = mapped_column(Integer)
    # Envelope-encrypted per-tenant credentials (ciphertext only; encryption in Task 4).
    wa_credentials_enc: Mapped[str | None] = mapped_column(Text)
    razorpay_credentials_enc: Mapped[str | None] = mapped_column(Text)

    staff: Mapped[list[StaffUser]] = relationship(back_populates="institution")
    courses: Mapped[list[Course]] = relationship(back_populates="institution")
    discount_codes: Mapped[list[DiscountCode]] = relationship(back_populates="institution")
    leads: Mapped[list[Lead]] = relationship(back_populates="institution")


class StaffUser(IdMixin, TenantMixin, TimestampMixin, Base):
    """A dashboard user (admin or agent) belonging to one institution."""

    __tablename__ = "staff_users"
    __table_args__ = (
        UniqueConstraint("tenant_id", "email"),
        UniqueConstraint("tenant_id", "id", name="uq_staff_users_tenant_id_id"),
    )

    email: Mapped[str] = mapped_column(String(320), nullable=False)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255))
    role: Mapped[StaffRole] = mapped_column(
        Enum(StaffRole, native_enum=False, length=16), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    must_change_password: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )

    institution: Mapped[Institution] = relationship(back_populates="staff")
