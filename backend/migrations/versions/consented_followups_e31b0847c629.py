"""Default existing inquiries to no proactive outreach and index due follow-ups."""

import sqlalchemy as sa
from alembic import op

revision = "e31b0847c629"
down_revision = "9c5027e2d614"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "leads",
        sa.Column("followup_consent", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column("leads", sa.Column("followup_consent_updated_at", sa.DateTime(timezone=True)))
    op.add_column("leads", sa.Column("followup_due_at", sa.DateTime(timezone=True)))
    op.create_index(
        "ix_leads_followup_due",
        "leads",
        ["followup_due_at"],
        postgresql_where=sa.text("followup_consent AND followup_due_at IS NOT NULL"),
    )


def downgrade() -> None:
    # Older senders do not know reminder consent. Never leave executable outreach
    # behind when removing those fields; in-flight requests retain uncertainty.
    op.execute(
        sa.text(
            "UPDATE outbound_messages SET status = CASE WHEN status='sending' "
            "THEN 'uncertain' ELSE 'failed' END, error_code='followup_rollback', "
            "next_attempt_at=NULL, updated_at=CURRENT_TIMESTAMP "
            "WHERE kind='followup' AND status IN ('queued','sending')"
        )
    )
    op.drop_index("ix_leads_followup_due", table_name="leads")
    op.drop_column("leads", "followup_due_at")
    op.drop_column("leads", "followup_consent_updated_at")
    op.drop_column("leads", "followup_consent")
