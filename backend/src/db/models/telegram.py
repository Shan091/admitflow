"""Tenant-owned Telegram bots and encrypted student routing identities."""

import uuid

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    ForeignKeyConstraint,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base, IdMixin, TenantMixin, TimestampMixin


class TelegramBot(IdMixin, TenantMixin, TimestampMixin, Base):
    """Trusted bot-to-institution mapping; token is application-encrypted."""

    __tablename__ = "telegram_bots"
    __table_args__ = (
        UniqueConstraint("tenant_id", "id", name="uq_telegram_bots_tenant_id_id"),
        CheckConstraint("telegram_bot_id > 0", name="positive_bot_id"),
    )

    telegram_bot_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    token_enc: Mapped[str] = mapped_column(Text, nullable=False)
    last_update_id: Mapped[int | None] = mapped_column(BigInteger)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class TelegramIdentity(IdMixin, TenantMixin, TimestampMixin, Base):
    """A private-chat identity whose bot and lead must belong to its tenant."""

    __tablename__ = "telegram_identities"
    __table_args__ = (
        UniqueConstraint("tenant_id", "bot_id", "id", "lead_id", name="uq_telegram_identity_owner"),
        ForeignKeyConstraint(
            ["tenant_id", "bot_id"],
            ["telegram_bots.tenant_id", "telegram_bots.id"],
            ondelete="CASCADE",
            name="fk_telegram_identities_tenant_bot",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "lead_id"],
            ["leads.tenant_id", "leads.id"],
            ondelete="CASCADE",
            name="fk_telegram_identities_tenant_lead",
        ),
        UniqueConstraint("tenant_id", "bot_id", "user_hash", name="uq_telegram_identity_user"),
        UniqueConstraint("tenant_id", "bot_id", "chat_hash", name="uq_telegram_identity_chat"),
    )

    bot_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    lead_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    user_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    chat_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    user_id_enc: Mapped[str] = mapped_column(Text, nullable=False)
    chat_id_enc: Mapped[str] = mapped_column(Text, nullable=False)
