"""Add a bounded institution daily Telegram send-attempt budget."""

import sqlalchemy as sa
from alembic import op

revision = "9c5027e2d614"
down_revision = "f129a064c5e8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "institutions",
        sa.Column("telegram_daily_send_limit", sa.Integer(), nullable=False, server_default="1000"),
    )
    op.create_check_constraint(
        "telegram_daily_send_limit_bounds",
        "institutions",
        "telegram_daily_send_limit BETWEEN 0 AND 100000",
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("ck_institutions_telegram_daily_send_limit_bounds"), "institutions", type_="check"
    )
    op.drop_column("institutions", "telegram_daily_send_limit")
