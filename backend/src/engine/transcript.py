"""Human-readable callback summaries without exposing routing or signature details."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Batch, ConversationEvent, Course
from src.engine.contracts import Event
from src.telegram.callbacks import parse_callback


async def event_text(db: AsyncSession, row: ConversationEvent, event: Event) -> str:
    if event.kind != "callback":
        return event.text or "Unsupported media received"
    try:
        kind, target = parse_callback(event.text, row.lead_id, row.bot_id)
        if kind == "language":
            return f"Language preference: {target}"
        if kind == "course":
            name = await db.scalar(
                select(Course.name).where(
                    Course.id == uuid.UUID(target), Course.tenant_id == row.tenant_id
                )
            )
            return f"Selected course: {name or 'unavailable course'}"
        if kind == "batch":
            name = await db.scalar(
                select(Batch.name).where(
                    Batch.id == uuid.UUID(target), Batch.tenant_id == row.tenant_id
                )
            )
            return f"Selected batch: {name or 'unavailable batch'}"
        return "Requested staff help" if kind == "human" else "Explored courses"
    except ValueError:
        return "Unverified button selection"
