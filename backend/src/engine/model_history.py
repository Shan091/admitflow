"""Bounded bulk model context; reset boundaries preserve the staff audit trail."""

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import literal, select, union_all
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import decrypt_pii
from src.db.models import Batch, ConversationEvent, ConversationReply, Course, Lead, OutboundMessage
from src.engine.contracts import Event, Reply
from src.telegram.callbacks import parse_callback


async def model_history(
    db: AsyncSession, lead: Lead, memory: dict[str, Any]
) -> list[dict[str, str]]:
    entries = union_all(
        select(
            ConversationEvent.created_at.label("time"),
            ConversationEvent.id.label("id"),
            literal("user").label("role"),
            ConversationEvent.payload_enc.label("payload"),
            ConversationEvent.bot_id.label("bot_id"),
        ).where(
            ConversationEvent.tenant_id == lead.tenant_id,
            ConversationEvent.lead_id == lead.id,
            ConversationEvent.status == "done",
        ),
        select(
            ConversationReply.created_at,
            ConversationReply.id,
            literal("assistant"),
            ConversationReply.payload_enc,
            ConversationEvent.bot_id,
        )
        .join(
            ConversationEvent,
            (ConversationEvent.id == ConversationReply.event_id)
            & (ConversationEvent.tenant_id == ConversationReply.tenant_id),
        )
        .where(
            ConversationEvent.tenant_id == lead.tenant_id,
            ConversationEvent.lead_id == lead.id,
            ConversationReply.status == "sent",
        ),
        select(
            OutboundMessage.created_at,
            OutboundMessage.id,
            literal("assistant"),
            OutboundMessage.payload_enc,
            literal(None),
        ).where(
            OutboundMessage.tenant_id == lead.tenant_id,
            OutboundMessage.lead_id == lead.id,
            OutboundMessage.status == "sent",
        ),
    ).subquery()
    statement = select(entries)
    if memory.get("history_after"):
        statement = statement.where(
            entries.c.time >= datetime.fromisoformat(memory["history_after"])
        )
    rows = list(
        (
            await db.execute(
                statement.order_by(entries.c.time.desc(), entries.c.id.desc()).limit(20)
            )
        ).all()
    )
    messages: list[dict[str, str]] = []
    lookups: list[tuple[int, str, uuid.UUID]] = []
    for row in reversed(rows):
        body = decrypt_pii(row.payload)
        if row.role != "user":
            text = Reply.model_validate_json(body).text
        else:
            event = Event.model_validate_json(body)
            text = event.text
            if event.kind == "callback":
                try:
                    kind, target = parse_callback(text, lead.id, row.bot_id)
                    text = {
                        "human": "Requested staff help",
                        "guide": "Requested course guidance",
                        "apply": "Application step",
                        "reset": "Conversation reset control",
                        "courses": "Explored course catalogue",
                    }.get(kind, "Used a chat control")
                    if kind == "answer" and event.selected_answer:
                        text = event.selected_answer
                    if kind in {"course", "batch"}:
                        lookups.append((len(messages), kind, uuid.UUID(target)))
                except ValueError:
                    text = "Unverified button selection"
        messages.append({"role": row.role, "content": text or "Unsupported media received"})
    if lookups:
        ids = [target for _, _, target in lookups]
        names = (
            await db.execute(
                union_all(
                    select(literal("course"), Course.id, Course.name).where(
                        Course.tenant_id == lead.tenant_id, Course.id.in_(ids)
                    ),
                    select(literal("batch"), Batch.id, Batch.name).where(
                        Batch.tenant_id == lead.tenant_id, Batch.id.in_(ids)
                    ),
                )
            )
        ).all()
        by_id = {(kind, target): name for kind, target, name in names}
        for index, kind, target_id in lookups:
            messages[index]["content"] = (
                f"Selected {kind}: {by_id.get((kind, target_id), 'unavailable')}"
            )
    return messages
