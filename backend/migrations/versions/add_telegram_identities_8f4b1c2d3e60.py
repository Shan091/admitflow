"""Add Telegram identity without requiring or fabricating phone contacts."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "8f4b1c2d3e60"
down_revision: str | None = "c470f1ebc811"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column("institutions", "whatsapp_phone_number_id", nullable=True)
    op.alter_column("leads", "phone_hash", nullable=True)
    op.alter_column("leads", "phone_enc", nullable=True)
    op.create_unique_constraint("uq_leads_tenant_id_id", "leads", ["tenant_id", "id"])
    op.create_check_constraint(
        op.f("ck_leads_phone_contact_pair"),
        "leads",
        "(phone_hash IS NULL) = (phone_enc IS NULL)",
    )
    op.create_table(
        "telegram_bots",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("telegram_bot_id", sa.BigInteger(), nullable=False),
        sa.Column("token_enc", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(["tenant_id"], ["institutions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("telegram_bot_id"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_telegram_bots_tenant_id_id"),
        sa.CheckConstraint("telegram_bot_id > 0", name=op.f("ck_telegram_bots_positive_bot_id")),
    )
    op.create_index("ix_telegram_bots_tenant_id", "telegram_bots", ["tenant_id"])
    op.create_table(
        "telegram_identities",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("bot_id", sa.Uuid(), nullable=False),
        sa.Column("lead_id", sa.Uuid(), nullable=False),
        sa.Column("user_hash", sa.String(64), nullable=False),
        sa.Column("chat_hash", sa.String(64), nullable=False),
        sa.Column("user_id_enc", sa.Text(), nullable=False),
        sa.Column("chat_id_enc", sa.Text(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(["tenant_id"], ["institutions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["tenant_id", "bot_id"],
            ["telegram_bots.tenant_id", "telegram_bots.id"],
            name="fk_telegram_identities_tenant_bot",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "lead_id"],
            ["leads.tenant_id", "leads.id"],
            name="fk_telegram_identities_tenant_lead",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tenant_id", "bot_id", "user_hash", name="uq_telegram_identity_user"),
        sa.UniqueConstraint("tenant_id", "bot_id", "chat_hash", name="uq_telegram_identity_chat"),
    )
    op.create_index("ix_telegram_identities_tenant_id", "telegram_identities", ["tenant_id"])


def downgrade() -> None:
    # Restoring NOT NULL would otherwise fail after dropping the new identity
    # tables. Refuse before changing anything; never invent phone numbers.
    telegram_data_or_missing_contacts = op.get_bind().scalar(
        sa.text(
            "SELECT EXISTS (SELECT 1 FROM leads WHERE phone_hash IS NULL OR phone_enc IS NULL) "
            "OR EXISTS (SELECT 1 FROM institutions WHERE whatsapp_phone_number_id IS NULL) "
            "OR EXISTS (SELECT 1 FROM telegram_bots) "
            "OR EXISTS (SELECT 1 FROM telegram_identities)"
        )
    )
    if telegram_data_or_missing_contacts:
        raise RuntimeError("Migrate Telegram-only records before downgrading the identity schema")
    op.drop_table("telegram_identities")
    op.drop_table("telegram_bots")
    op.drop_constraint(op.f("ck_leads_phone_contact_pair"), "leads", type_="check")
    op.drop_constraint("uq_leads_tenant_id_id", "leads", type_="unique")
    op.alter_column("leads", "phone_enc", nullable=False)
    op.alter_column("leads", "phone_hash", nullable=False)
    op.alter_column("institutions", "whatsapp_phone_number_id", nullable=False)
