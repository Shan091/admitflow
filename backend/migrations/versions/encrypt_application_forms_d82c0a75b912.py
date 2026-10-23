"""Add encrypted application form payload without modifying historical rows."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d82c0a75b912"
down_revision: str | None = "714f092da3b8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("applications", sa.Column("form_data_enc", sa.Text(), nullable=True))


def downgrade() -> None:
    if op.get_bind().scalar(
        sa.text("SELECT count(*) FROM applications WHERE form_data_enc IS NOT NULL")
    ):
        raise RuntimeError("Refusing to discard encrypted application forms")
    op.drop_column("applications", "form_data_enc")
