"""Bounded chronological transcript across inbound, replies and standalone delivery."""

import base64
import uuid
from datetime import datetime
from typing import Any, Literal

from fastapi import HTTPException
from pydantic import BaseModel, field_validator
from sqlalchemy import literal, select, tuple_, union_all
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import undefer

from src.core.security import decrypt_pii
from src.db.models import ConversationEvent, ConversationReply, OutboundMessage
from src.engine.contracts import Event, Reply
from src.engine.transcript import event_text


class Cursor(BaseModel):
    time: datetime
    source: Literal[0, 1, 2]
    id: uuid.UUID

    @field_validator("time")
    @classmethod
    def aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("Cursor needs a timezone")
        return value


async def timeline(
    db: AsyncSession, tenant_id: uuid.UUID, lead_id: uuid.UUID, token: str | None
) -> tuple[list[dict[str, Any]], str | None]:
    cursor = None
    if token is not None:
        try:
            cursor = Cursor.model_validate_json(base64.urlsafe_b64decode(token))
        except (ValueError, TypeError):
            raise HTTPException(400, "Invalid conversation cursor.") from None
    scope = (ConversationEvent.tenant_id == tenant_id, ConversationEvent.lead_id == lead_id)
    entries = union_all(
        select(
            ConversationEvent.created_at.label("time"),
            literal(0).label("source"),
            ConversationEvent.id,
        ).where(*scope),
        select(
            ConversationReply.created_at.label("time"),
            literal(1).label("source"),
            ConversationReply.id,
        )
        .join(
            ConversationEvent,
            (ConversationEvent.id == ConversationReply.event_id)
            & (ConversationEvent.tenant_id == ConversationReply.tenant_id),
        )
        .where(*scope),
        select(
            OutboundMessage.created_at.label("time"), literal(2).label("source"), OutboundMessage.id
        ).where(OutboundMessage.tenant_id == tenant_id, OutboundMessage.lead_id == lead_id),
    ).subquery()
    statement = select(entries)
    if cursor is not None:
        statement = statement.where(
            tuple_(entries.c.time, entries.c.source, entries.c.id)
            < tuple_(cursor.time, cursor.source, cursor.id)
        )
    rows = list(
        (
            await db.execute(
                statement.order_by(
                    entries.c.time.desc(), entries.c.source.desc(), entries.c.id.desc()
                ).limit(51)
            )
        ).all()
    )
    has_more = len(rows) > 50
    rows = rows[:50]
    messages: list[dict[str, Any]] = []
    for row in reversed(rows):
        if row.source == 0:
            event = await db.scalar(
                select(ConversationEvent)
                .options(undefer(ConversationEvent.payload_enc))
                .where(ConversationEvent.id == row.id, *scope)
            )
            if event is None:
                continue
            body = Event.model_validate_json(decrypt_pii(event.payload_enc))
            text = await event_text(db, event, body)
            direction, kind, status, event_id = "inbound", "student", event.status, event.id
        elif row.source == 1:
            reply = await db.scalar(
                select(ConversationReply)
                .options(undefer(ConversationReply.payload_enc))
                .where(ConversationReply.id == row.id, ConversationReply.tenant_id == tenant_id)
            )
            if reply is None:
                continue
            text = Reply.model_validate_json(decrypt_pii(reply.payload_enc)).text
            direction, kind, status, event_id = (
                "outbound",
                "bot_reply",
                reply.status,
                reply.event_id,
            )
        else:
            message = await db.scalar(
                select(OutboundMessage)
                .options(undefer(OutboundMessage.payload_enc))
                .where(
                    OutboundMessage.id == row.id,
                    OutboundMessage.tenant_id == tenant_id,
                    OutboundMessage.lead_id == lead_id,
                )
            )
            if message is None:
                continue
            text = Reply.model_validate_json(decrypt_pii(message.payload_enc)).text
            direction, kind, status, event_id = "outbound", message.kind, message.status, message.id
        messages.append(
            {
                "message_id": f"{row.source}:{row.id}",
                "event_id": str(event_id),
                "direction": direction,
                "kind": kind,
                "text": text,
                "status": status,
                "created_at": row.time.isoformat(),
            }
        )
    older = None
    if has_more:
        last = rows[-1]
        older = base64.urlsafe_b64encode(
            Cursor(time=last.time, source=last.source, id=last.id).model_dump_json().encode()
        ).decode()
    return messages, older
