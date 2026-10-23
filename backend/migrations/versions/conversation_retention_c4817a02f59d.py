"""Track completed dialogue expiration without removing business/application records."""

import sqlalchemy as sa
from alembic import op

revision = "c4817a02f59d"
down_revision = "70a31c6d25fb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "leads", sa.Column("conversation_purged_at", sa.DateTime(timezone=True), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("leads", "conversation_purged_at")
