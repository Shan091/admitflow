"""Declarative base, metadata naming convention, and shared column mixins.

Every ORM model inherits from :class:`Base`. The explicit ``naming_convention``
gives constraints deterministic names so Alembic emits stable, reversible
migrations (an unnamed constraint can't be reliably dropped on downgrade).

Two mixins carry the cross-cutting columns:

* :class:`TimestampMixin` — ``created_at`` / ``updated_at`` (DB-side ``now()``).
* :class:`TenantMixin` — ``tenant_id`` (FK → ``institutions.id``, indexed, NOT
  NULL). Row-level multi-tenancy per ADR-003: every tenant-scoped table mixes
  this in, and every query must filter on it. The tenant root (Institution)
  deliberately does **not** use it — its own ``id`` *is* the tenant.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, MetaData, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Stable constraint names -> reversible Alembic migrations.
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Declarative base shared by every AdmitFlow model."""

    metadata = MetaData(naming_convention=NAMING_CONVENTION)


class IdMixin:
    """UUID primary key with an application-side default.

    UUIDs avoid cross-tenant enumeration and are safe to expose in the
    dashboard and webhook payloads.
    """

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)


class TimestampMixin:
    """Server-side created/updated timestamps."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class TenantMixin:
    """Row-level tenant scoping (ADR-003). Mixed into every tenant-scoped table."""

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("institutions.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
