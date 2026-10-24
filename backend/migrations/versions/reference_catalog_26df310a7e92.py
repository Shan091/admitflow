"""Distinguish published reference programmes from configured admissions offerings."""

import sqlalchemy as sa
from alembic import op

revision = "26df310a7e92"
down_revision = "c4817a02f59d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "courses",
        sa.Column("is_reference", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column("courses", sa.Column("reference_url", sa.String(1024), nullable=True))


def downgrade() -> None:
    op.drop_column("courses", "reference_url")
    op.drop_column("courses", "is_reference")
