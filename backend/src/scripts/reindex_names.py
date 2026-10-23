"""Backfill encrypted lead names from latest submitted forms and rebuild blind prefixes.

Run after migration/key rotation: uv run python -m src.scripts.reindex_names.
Only record counts are printed. Each batch commits atomically; reruns are safe.
"""

import asyncio
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.name_search import name_tokens
from src.core.security import decrypt_pii
from src.db.models import Application, Lead
from src.db.session import get_sessionmaker


async def reindex_batch(
    db: AsyncSession, after: uuid.UUID | None = None
) -> tuple[uuid.UUID | None, int]:
    statement = select(Lead).order_by(Lead.id).limit(200).with_for_update()
    if after:
        statement = statement.where(Lead.id > after)
    leads = (await db.scalars(statement)).all()
    for lead in leads:
        if not lead.name_enc:
            lead.name_enc = await db.scalar(
                select(Application.full_name_enc)
                .where(Application.tenant_id == lead.tenant_id, Application.lead_id == lead.id)
                .order_by(Application.submitted_at.desc(), Application.id.desc())
                .limit(1)
            )
        lead.name_search_tokens = (
            name_tokens(lead.tenant_id, decrypt_pii(lead.name_enc)) if lead.name_enc else []
        )
    await db.commit()
    return (leads[-1].id if leads else after), len(leads)


async def main() -> None:
    after = None
    total = 0
    async with get_sessionmaker()() as db:
        while True:
            after, count = await reindex_batch(db, after)
            total += count
            if count < 200:
                break
    print(f"Reindexed {total} inquiries.")


if __name__ == "__main__":
    asyncio.run(main())
