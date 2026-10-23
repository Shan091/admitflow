"""Lead, its semantic facts (lead_facts), and episodic messages (ADR-004)."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    event,
    inspect,
    text,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Mapped, Mapper, mapped_column, relationship

from src.db.base import Base, IdMixin, TenantMixin, TimestampMixin
from src.db.enums import LeadStatus, MessageDirection

if TYPE_CHECKING:
    from src.db.models.institution import Institution


class Lead(IdMixin, TenantMixin, TimestampMixin, Base):
    """A prospective applicant with optional phone contact and channel identities.

    ``phone_hash`` is a deterministic hash for lookup/dedup; ``phone_enc`` /
    ``name_enc`` hold ciphertext PII (encryption lands in Task 4). ``status``
    tracks the SPEC §7.3 lifecycle; ``readiness_score`` is the calibrated
    System-1 signal (ADR-008) surfaced beside the stage.
    """

    __tablename__ = "leads"
    __table_args__ = (
        UniqueConstraint("tenant_id", "phone_hash"),
        UniqueConstraint("tenant_id", "id", name="uq_leads_tenant_id_id"),
        CheckConstraint(
            "(phone_hash IS NULL) = (phone_enc IS NULL)",
            name="phone_contact_pair",
        ),
        Index("ix_leads_name_search", "name_search_tokens", postgresql_using="gin"),
        Index(
            "ix_leads_followup_due",
            "followup_due_at",
            postgresql_where=text("followup_consent AND followup_due_at IS NOT NULL"),
        ),
    )

    phone_hash: Mapped[str | None] = mapped_column(String(64), index=True)
    phone_enc: Mapped[str | None] = mapped_column(Text)
    name_enc: Mapped[str | None] = mapped_column(Text)
    name_search_tokens: Mapped[list[str]] = mapped_column(
        ARRAY(String(64)), nullable=False, default=list, server_default="{}"
    )
    status: Mapped[LeadStatus] = mapped_column(
        Enum(LeadStatus, native_enum=False, length=32),
        nullable=False,
        default=LeadStatus.NEW,
    )
    readiness_score: Mapped[float | None] = mapped_column(Float)
    current_course_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("courses.id", ondelete="SET NULL")
    )
    current_batch_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("batches.id", ondelete="SET NULL")
    )
    copilot_mode: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    reengagement_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    followup_consent: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    followup_consent_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    followup_due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_inbound_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_outbound_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    institution: Mapped[Institution] = relationship(back_populates="leads")
    facts: Mapped[list[LeadFact]] = relationship(
        back_populates="lead", cascade="all, delete-orphan"
    )
    messages: Mapped[list[Message]] = relationship(
        back_populates="lead", cascade="all, delete-orphan"
    )


@event.listens_for(Lead, "before_insert")
@event.listens_for(Lead, "before_update")
def index_known_name(_mapper: Mapper[Lead], _connection: Connection, lead: Lead) -> None:
    """Keep index updates atomic with encrypted names, including name removal."""
    state = inspect(lead)
    if state.pending or state.attrs.name_enc.history.has_changes():
        from src.core.name_search import name_tokens
        from src.core.security import decrypt_pii

        lead.name_search_tokens = (
            name_tokens(lead.tenant_id, decrypt_pii(lead.name_enc)) if lead.name_enc else []
        )


class LeadFact(IdMixin, TenantMixin, TimestampMixin, Base):
    """Semantic memory: a durable key/value fact about a lead (ADR-004).

    Unique on ``(tenant_id, lead_id, key)`` so each fact upserts in place.
    """

    __tablename__ = "lead_facts"
    __table_args__ = (UniqueConstraint("tenant_id", "lead_id", "key"),)

    lead_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"), index=True, nullable=False
    )
    key: Mapped[str] = mapped_column(String(64), nullable=False)
    value: Mapped[Any] = mapped_column(JSONB, nullable=False)

    lead: Mapped[Lead] = relationship(back_populates="facts")


class Message(IdMixin, TenantMixin, TimestampMixin, Base):
    """Episodic memory: one WhatsApp turn (ADR-004).

    The single source of truth for the engine, the dashboard, and Laya training
    labels. ``wa_message_id`` is Meta's id, used for dedup. ``content`` may hold
    PII; column-level handling is layered in Task 4.
    """

    __tablename__ = "messages"

    lead_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"), index=True, nullable=False
    )
    direction: Mapped[MessageDirection] = mapped_column(
        Enum(MessageDirection, native_enum=False, length=8), nullable=False
    )
    wa_message_id: Mapped[str | None] = mapped_column(String(128), index=True)
    msg_type: Mapped[str] = mapped_column(String(32), nullable=False, default="text")
    content: Mapped[str | None] = mapped_column(Text)

    lead: Mapped[Lead] = relationship(back_populates="messages")
