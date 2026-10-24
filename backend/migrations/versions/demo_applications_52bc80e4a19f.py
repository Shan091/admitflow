"""Separate reference demo fees and persistent application/invoice mode."""

import sqlalchemy as sa
from alembic import op

revision = "52bc80e4a19f"
down_revision = "26df310a7e92"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("courses", sa.Column("demo_application_fee", sa.Integer(), nullable=True))
    op.create_check_constraint(
        "demo_reference_fee",
        "courses",
        "demo_application_fee IS NULL OR (is_reference AND demo_application_fee >= 100)",
    )
    for table in ("applications", "payment_orders"):
        op.add_column(
            table, sa.Column("is_demo", sa.Boolean(), nullable=False, server_default="false")
        )


def downgrade() -> None:
    for table in ("payment_orders", "applications"):
        op.drop_column(table, "is_demo")
    op.drop_constraint("demo_reference_fee", "courses", type_="check")
    op.drop_column("courses", "demo_application_fee")
