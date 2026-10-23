"""Add encrypted Telegram inbox/outbox, memory, human requests and polling offsets."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "714f092da3b8"
down_revision: str | None = "b627da2f7e11"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def columns() -> list[sa.Column]:  # type: ignore[type-arg]
    return [
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "tenant_id",
            sa.Uuid(),
            sa.ForeignKey("institutions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    ]


def upgrade() -> None:
    op.add_column("telegram_bots", sa.Column("last_update_id", sa.BigInteger(), nullable=True))
    op.create_unique_constraint(
        "uq_telegram_identity_owner",
        "telegram_identities",
        ["tenant_id", "bot_id", "id", "lead_id"],
    )
    op.create_table(
        "conversation_events",
        *columns(),
        sa.Column("bot_id", sa.Uuid(), nullable=False),
        sa.Column("identity_id", sa.Uuid(), nullable=False),
        sa.Column("lead_id", sa.Uuid(), nullable=False),
        sa.Column("update_id", sa.BigInteger(), nullable=False),
        sa.Column("kind", sa.String(16), nullable=False),
        sa.Column("payload_enc", sa.Text(), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.UniqueConstraint("bot_id", "update_id", name="uq_conversation_bot_update"),
        sa.UniqueConstraint("tenant_id", "id", name="uq_conversation_event_tenant_id"),
        sa.ForeignKeyConstraint(
            ["tenant_id", "bot_id", "identity_id", "lead_id"],
            [
                "telegram_identities.tenant_id",
                "telegram_identities.bot_id",
                "telegram_identities.id",
                "telegram_identities.lead_id",
            ],
            ondelete="CASCADE",
            name="fk_event_identity_owner",
        ),
        sa.CheckConstraint(
            "status IN ('queued','done')",
            name=op.f("ck_conversation_events_conversation_event_status"),
        ),
    )
    op.create_table(
        "conversation_replies",
        *columns(),
        sa.Column("event_id", sa.Uuid(), nullable=False),
        sa.Column("payload_enc", sa.Text(), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("error_code", sa.String(48)),
        sa.Column("telegram_message_id", sa.BigInteger()),
        sa.Column("next_attempt_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("event_id", name="uq_conversation_reply_event"),
        sa.ForeignKeyConstraint(
            ["tenant_id", "event_id"],
            ["conversation_events.tenant_id", "conversation_events.id"],
            ondelete="CASCADE",
            name="fk_reply_event_owner",
        ),
        sa.CheckConstraint(
            "status IN ('queued','sending','sent','failed','uncertain')",
            name=op.f("ck_conversation_replies_conversation_reply_status"),
        ),
    )
    op.create_table(
        "conversation_memories",
        *columns(),
        sa.Column("lead_id", sa.Uuid(), nullable=False),
        sa.Column("payload_enc", sa.Text(), nullable=False),
        sa.UniqueConstraint("tenant_id", "lead_id", name="uq_conversation_memory_lead"),
        sa.ForeignKeyConstraint(
            ["tenant_id", "lead_id"],
            ["leads.tenant_id", "leads.id"],
            ondelete="CASCADE",
            name="fk_memory_lead_owner",
        ),
    )
    op.create_table(
        "human_requests",
        *columns(),
        sa.Column("lead_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.ForeignKeyConstraint(
            ["tenant_id", "lead_id"],
            ["leads.tenant_id", "leads.id"],
            ondelete="CASCADE",
            name="fk_human_request_lead_owner",
        ),
        sa.CheckConstraint(
            "status IN ('open','acknowledged','resolved','resumed')",
            name=op.f("ck_human_requests_human_request_status"),
        ),
    )
    op.create_index(
        "uq_human_request_pending",
        "human_requests",
        ["tenant_id", "lead_id"],
        unique=True,
        postgresql_where=sa.text("status != 'resumed'"),
    )
    for table in (
        "conversation_events",
        "conversation_replies",
        "conversation_memories",
        "human_requests",
    ):
        op.create_index(f"ix_{table}_tenant_id", table, ["tenant_id"])
    for table in ("conversation_events", "human_requests"):
        op.create_index(f"ix_{table}_lead_id", table, ["lead_id"])


def downgrade() -> None:
    if op.get_bind().scalar(
        sa.text(
            "SELECT EXISTS (SELECT 1 FROM conversation_events) "
            "OR EXISTS (SELECT 1 FROM human_requests) "
            "OR EXISTS (SELECT 1 FROM conversation_memories)"
        )
    ):
        raise RuntimeError("Export and remove conversation data before downgrading")
    for table in (
        "human_requests",
        "conversation_memories",
        "conversation_replies",
        "conversation_events",
    ):
        op.drop_table(table)
    op.drop_constraint("uq_telegram_identity_owner", "telegram_identities", type_="unique")
    op.drop_column("telegram_bots", "last_update_id")
