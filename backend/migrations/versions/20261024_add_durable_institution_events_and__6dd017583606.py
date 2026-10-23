"""Add durable institution events and webhook delivery

Revision ID: 6dd017583606
Revises: a82df107e436
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6dd017583606"
down_revision: str | None = "a82df107e436"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "webhook_endpoints",
        sa.Column("url_enc", sa.Text(), nullable=False),
        sa.Column("secret_enc", sa.Text(), nullable=False),
        sa.Column("display_host", sa.String(length=255), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("generation", sa.Uuid(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["institutions.id"],
            name=op.f("fk_webhook_endpoints_tenant_id_institutions"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_webhook_endpoints")),
        sa.UniqueConstraint("tenant_id", "id", name="uq_webhook_endpoint_owner"),
        sa.UniqueConstraint("tenant_id", name=op.f("uq_webhook_endpoints_tenant_id")),
    )
    op.create_index(
        op.f("ix_webhook_endpoints_tenant_id"), "webhook_endpoints", ["tenant_id"], unique=False
    )
    op.create_table(
        "integration_events",
        sa.Column("lead_id", sa.Uuid(), nullable=True),
        sa.Column("kind", sa.String(length=64), nullable=False),
        sa.Column("state", sa.String(length=32), nullable=True),
        sa.Column("notification", sa.String(length=16), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tenant_id", "lead_id"],
            ["leads.tenant_id", "leads.id"],
            name="fk_integration_event_lead",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["institutions.id"],
            name=op.f("fk_integration_events_tenant_id_institutions"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_integration_events")),
        sa.UniqueConstraint("tenant_id", "id", name="uq_integration_event_owner"),
    )
    op.create_index(
        "ix_integration_event_timeline",
        "integration_events",
        ["tenant_id", "created_at", "id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_integration_events_tenant_id"), "integration_events", ["tenant_id"], unique=False
    )
    op.create_table(
        "notification_receipts",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("event_id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tenant_id", "event_id"],
            ["integration_events.tenant_id", "integration_events.id"],
            name="fk_notification_receipt_event",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "user_id"],
            ["staff_users.tenant_id", "staff_users.id"],
            name="fk_notification_receipt_user",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["institutions.id"],
            name=op.f("fk_notification_receipts_tenant_id_institutions"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("user_id", "event_id", name=op.f("pk_notification_receipts")),
    )
    op.create_index(
        op.f("ix_notification_receipts_tenant_id"),
        "notification_receipts",
        ["tenant_id"],
        unique=False,
    )
    op.create_table(
        "webhook_deliveries",
        sa.Column("endpoint_id", sa.Uuid(), nullable=False),
        sa.Column("event_id", sa.Uuid(), nullable=False),
        sa.Column("generation", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("lease_id", sa.Uuid(), nullable=True),
        sa.Column("next_attempt_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_code", sa.String(length=48), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "status IN ('queued','sending','sent','dead','cancelled')",
            name=op.f("ck_webhook_deliveries_webhook_delivery_status"),
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "endpoint_id"],
            ["webhook_endpoints.tenant_id", "webhook_endpoints.id"],
            name="fk_webhook_delivery_endpoint",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "event_id"],
            ["integration_events.tenant_id", "integration_events.id"],
            name="fk_webhook_delivery_event",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["institutions.id"],
            name=op.f("fk_webhook_deliveries_tenant_id_institutions"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_webhook_deliveries")),
        sa.UniqueConstraint("endpoint_id", "event_id", name="uq_webhook_delivery_event"),
    )
    op.create_index(
        op.f("ix_webhook_deliveries_tenant_id"), "webhook_deliveries", ["tenant_id"], unique=False
    )
    op.create_index(
        "ix_webhook_delivery_due", "webhook_deliveries", ["status", "next_attempt_at"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_webhook_delivery_due", table_name="webhook_deliveries")
    op.drop_index(op.f("ix_webhook_deliveries_tenant_id"), table_name="webhook_deliveries")
    op.drop_table("webhook_deliveries")
    op.drop_index(op.f("ix_notification_receipts_tenant_id"), table_name="notification_receipts")
    op.drop_table("notification_receipts")
    op.drop_index(op.f("ix_integration_events_tenant_id"), table_name="integration_events")
    op.drop_index("ix_integration_event_timeline", table_name="integration_events")
    op.drop_table("integration_events")
    op.drop_index(op.f("ix_webhook_endpoints_tenant_id"), table_name="webhook_endpoints")
    op.drop_table("webhook_endpoints")
