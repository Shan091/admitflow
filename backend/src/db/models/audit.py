"""Append-only audit trail (SPEC §12 / security-and-production.md)."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base, IdMixin, TenantMixin


class AuditLog(IdMixin, TenantMixin, Base):
    """One recorded significant action (state change, payment, deletion, takeover).

    Append-only, so it carries its own ``created_at`` instead of the
    update-tracking :class:`TimestampMixin`. ``details`` is free-form JSONB;
    it must never contain raw PII — reference records by id (``lead_id``).
    """

    __tablename__ = "audit_logs"

    lead_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("leads.id", ondelete="SET NULL"), index=True
    )
    action: Mapped[str] = mapped_column(String(64), nullable=False)
    actor: Mapped[str] = mapped_column(String(255), nullable=False)
    details: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
