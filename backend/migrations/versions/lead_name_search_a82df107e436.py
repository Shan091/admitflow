"""Add blind name-prefix lookup without placing names in plaintext storage."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "a82df107e436"
down_revision = "e31b0847c629"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "leads",
        sa.Column(
            "name_search_tokens",
            postgresql.ARRAY(sa.String(64)),
            nullable=False,
            server_default="{}",
        ),
    )
    op.create_index("ix_leads_name_search", "leads", ["name_search_tokens"], postgresql_using="gin")


def downgrade() -> None:
    op.drop_index("ix_leads_name_search", table_name="leads")
    op.drop_column("leads", "name_search_tokens")
