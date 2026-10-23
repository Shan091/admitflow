"""Add durable payment creation and encrypted outbound messages without changing legacy orders."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f129a064c5e8"
down_revision: str | None = "d82c0a75b912"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def common() -> list[sa.Column]:  # type: ignore[type-arg]
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
    for column in [
        sa.Column("request_key", sa.String(64), nullable=True),
        sa.Column("creation_state", sa.String(16), server_default="legacy", nullable=False),
        sa.Column("creation_attempts", sa.Integer(), server_default="0", nullable=False),
        sa.Column("payment_url_enc", sa.Text(), nullable=True),
        sa.Column("last_error", sa.String(64), nullable=True),
        sa.Column("next_attempt_at", sa.DateTime(timezone=True), nullable=True),
    ]:
        op.add_column("payment_orders", column)
    op.create_unique_constraint("uq_payment_order_tenant_id", "payment_orders", ["tenant_id", "id"])
    op.create_unique_constraint(
        "uq_payment_order_request", "payment_orders", ["tenant_id", "request_key"]
    )
    op.create_check_constraint(
        "ck_payment_orders_payment_creation_state",
        "payment_orders",
        "creation_state IN ('legacy','queued','creating','created','failed','uncertain')",
    )
    op.create_unique_constraint(
        "uq_payment_provider_payment", "payment_orders", ["tenant_id", "razorpay_payment_id"]
    )
    op.create_table(
        "outbound_messages",
        *common(),
        sa.Column("lead_id", sa.Uuid(), nullable=False),
        sa.Column("dedup_key", sa.String(128), nullable=False),
        sa.Column("kind", sa.String(32), nullable=False),
        sa.Column("payload_enc", sa.Text(), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("error_code", sa.String(64), nullable=True),
        sa.Column("next_attempt_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("telegram_message_id", sa.BigInteger(), nullable=True),
        sa.UniqueConstraint("tenant_id", "dedup_key", name="uq_outbound_tenant_dedup"),
        sa.ForeignKeyConstraint(
            ["tenant_id", "lead_id"],
            ["leads.tenant_id", "leads.id"],
            ondelete="CASCADE",
            name="fk_outbound_lead_owner",
        ),
        sa.CheckConstraint(
            "status IN ('queued','sending','sent','failed','uncertain')",
            name="ck_outbound_messages_outbound_message_status",
        ),
    )
    op.create_index("ix_outbound_messages_lead_id", "outbound_messages", ["lead_id"])
    op.create_table(
        "payment_events",
        *common(),
        sa.Column("payment_order_id", sa.Uuid(), nullable=False),
        sa.Column("body_digest", sa.String(64), nullable=False),
        sa.Column("kind", sa.String(64), nullable=False),
        sa.UniqueConstraint("tenant_id", "body_digest", name="uq_payment_event_body"),
        sa.ForeignKeyConstraint(
            ["tenant_id", "payment_order_id"],
            ["payment_orders.tenant_id", "payment_orders.id"],
            ondelete="CASCADE",
            name="fk_payment_event_order_owner",
        ),
    )
    op.create_index("ix_payment_events_payment_order_id", "payment_events", ["payment_order_id"])


def downgrade() -> None:
    connection = op.get_bind()
    if (
        connection.scalar(sa.text("SELECT count(*) FROM outbound_messages"))
        or connection.scalar(sa.text("SELECT count(*) FROM payment_events"))
        or connection.scalar(
            sa.text(
                "SELECT count(*) FROM payment_orders "
                "WHERE request_key IS NOT NULL OR creation_state <> 'legacy'"
            )
        )
    ):
        raise RuntimeError("Refusing to discard payment operations or outbound deliveries")
    op.drop_table("payment_events")
    op.drop_table("outbound_messages")
    op.drop_constraint("uq_payment_order_request", "payment_orders", type_="unique")
    op.drop_constraint("uq_payment_provider_payment", "payment_orders", type_="unique")
    op.drop_constraint("uq_payment_order_tenant_id", "payment_orders", type_="unique")
    op.drop_constraint("ck_payment_orders_payment_creation_state", "payment_orders", type_="check")
    for name in [
        "next_attempt_at",
        "last_error",
        "payment_url_enc",
        "creation_attempts",
        "creation_state",
        "request_key",
    ]:
        op.drop_column("payment_orders", name)
