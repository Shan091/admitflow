"""Course catalog: courses, batches, qualification rules, discount codes."""

from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base, IdMixin, TenantMixin, TimestampMixin
from src.db.enums import DiscountType, RuleOperator

if TYPE_CHECKING:
    from src.db.models.institution import Institution


class Course(IdMixin, TenantMixin, TimestampMixin, Base):
    """A program a lead can be qualified for and pay to apply to."""

    __tablename__ = "courses"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    # Application/registration fee in minor units (paise) — money is never a float,
    # and the amount comes from the DB, never the LLM (ADR-006).
    application_fee: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_reference: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    reference_url: Mapped[str | None] = mapped_column(String(1024))

    institution: Mapped[Institution] = relationship(back_populates="courses")
    batches: Mapped[list[Batch]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )
    qualification_rules: Mapped[list[QualificationRule]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )


class Batch(IdMixin, TenantMixin, TimestampMixin, Base):
    """A dated intake of a course with finite seats (SPEC §7.5)."""

    __tablename__ = "batches"

    course_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    seats_remaining: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    course: Mapped[Course] = relationship(back_populates="batches")


class QualificationRule(IdMixin, TenantMixin, TimestampMixin, Base):
    """A structured eligibility rule evaluated in code, not by the LLM (ADR-006).

    ``value`` is JSONB so a single column holds both scalars (``16``, ``"10th
    Pass"``) and lists (``["Kerala", "Karnataka"]``) per SPEC §7.4.
    """

    __tablename__ = "qualification_rules"

    course_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), index=True, nullable=False
    )
    field: Mapped[str] = mapped_column(String(64), nullable=False)
    operator: Mapped[RuleOperator] = mapped_column(
        Enum(RuleOperator, native_enum=False, length=8), nullable=False
    )
    value: Mapped[Any] = mapped_column(JSONB, nullable=False)

    course: Mapped[Course] = relationship(back_populates="qualification_rules")


class DiscountCode(IdMixin, TenantMixin, TimestampMixin, Base):
    """A staff-defined discount the backend (never the LLM) applies to a fee."""

    __tablename__ = "discount_codes"
    __table_args__ = (UniqueConstraint("tenant_id", "code"),)

    code: Mapped[str] = mapped_column(String(64), nullable=False)
    discount_type: Mapped[DiscountType] = mapped_column(
        Enum(DiscountType, native_enum=False, length=8), nullable=False
    )
    # percent: whole percent (e.g. 10). flat: minor units (paise).
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    valid_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    valid_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    max_uses: Mapped[int | None] = mapped_column(Integer)
    uses_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    institution: Mapped[Institution] = relationship(back_populates="discount_codes")
