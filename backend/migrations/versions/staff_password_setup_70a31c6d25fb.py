"""Require private passwords for newly provisioned/reset staff, preserving old accounts."""

import sqlalchemy as sa
from alembic import op

revision = "70a31c6d25fb"
down_revision = "6dd017583606"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "staff_users",
        sa.Column("must_change_password", sa.Boolean(), nullable=False, server_default=sa.false()),
    )


def downgrade() -> None:
    # Older code cannot enforce setup restrictions. Revoke setup-only sessions and
    # disable those accounts before removing the guard; an admin can reprovision.
    op.execute(
        sa.text(
            "DELETE FROM staff_sessions WHERE user_id IN "
            "(SELECT id FROM staff_users WHERE must_change_password)"
        )
    )
    op.execute(sa.text("UPDATE staff_users SET is_active=false WHERE must_change_password"))
    op.drop_column("staff_users", "must_change_password")
