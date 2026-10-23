"""Explicit staff takeover and replay-safe manual sends through the durable outbox."""

import json
import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import undefer

from src.core.security import decrypt_pii, encrypt_pii
from src.db.audit import write_audit_log
from src.db.enums import LeadStatus
from src.db.models import (
    ConversationEvent,
    ConversationReply,
    HumanRequest,
    Lead,
    OutboundMessage,
    TelegramBot,
    TelegramIdentity,
)
from src.engine.applications import resumed_status
from src.engine.contracts import Reply
from src.engine.journey import load_memory
from src.staff.auth import Db, Staff, require_browser_write
from src.staff.leads import get_lead
from src.telegram.outbound import enqueue_outbound

router = APIRouter(prefix="/api/staff/leads", tags=["staff conversation operations"])


class ManualMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    request_id: uuid.UUID
    text: str = Field(min_length=1, max_length=3500, strict=True)

    @field_validator("text")
    @classmethod
    def validated_reply(cls, value: str) -> str:
        return Reply(text=value.strip()).text


async def active_request(db: AsyncSession, lead: Lead) -> HumanRequest | None:
    return await db.scalar(
        select(HumanRequest)
        .where(
            HumanRequest.tenant_id == lead.tenant_id,
            HumanRequest.lead_id == lead.id,
            HumanRequest.status != "resumed",
        )
        .with_for_update()
    )


async def require_takeover(db: AsyncSession, lead: Lead) -> HumanRequest:
    request = await active_request(db, lead)
    if not lead.copilot_mode or request is None:
        raise HTTPException(409, "Take over this inquiry before composing a staff reply.")
    route = await db.scalar(
        select(TelegramIdentity.id)
        .join(
            TelegramBot,
            (TelegramBot.id == TelegramIdentity.bot_id)
            & (TelegramBot.tenant_id == TelegramIdentity.tenant_id),
        )
        .where(
            TelegramIdentity.tenant_id == lead.tenant_id,
            TelegramIdentity.lead_id == lead.id,
            TelegramBot.is_active.is_(True),
        )
        .limit(1)
    )
    if route is None:
        raise HTTPException(409, "No active Telegram conversation is available for this inquiry.")
    return request


async def finish_takeover(db: AsyncSession, lead: Lead) -> None:
    pending = await db.scalar(
        select(OutboundMessage.id)
        .where(
            OutboundMessage.tenant_id == lead.tenant_id,
            OutboundMessage.lead_id == lead.id,
            OutboundMessage.kind == "staff_reply",
            OutboundMessage.status.in_(["queued", "sending"]),
        )
        .limit(1)
    )
    if pending:
        raise HTTPException(409, "Wait for the queued staff reply to finish before resuming AI.")
    lead.copilot_mode = False
    row, memory = await load_memory(db, lead)
    draft = memory.get("staff_draft")
    if isinstance(draft, dict) and draft.get("status") in {"pending", "generating"}:
        draft["status"] = "ignored"
        row.payload_enc = encrypt_pii(json.dumps(memory, ensure_ascii=False))


@router.post("/{lead_id}/takeover", dependencies=[Depends(require_browser_write)])
async def takeover(lead_id: uuid.UUID, staff: Staff, db: Db) -> dict[str, Any]:
    lead = await get_lead(db, staff, lead_id, lock=True)
    event_ids = select(ConversationEvent.id).where(
        ConversationEvent.tenant_id == staff.tenant_id, ConversationEvent.lead_id == lead.id
    )
    in_flight = await db.scalar(
        select(ConversationReply.id)
        .where(ConversationReply.event_id.in_(event_ids), ConversationReply.status == "sending")
        .limit(1)
    )
    if in_flight:
        raise HTTPException(409, "A bot reply is being delivered. Reload before taking over.")
    await db.execute(
        update(ConversationReply)
        .where(ConversationReply.event_id.in_(event_ids), ConversationReply.status == "queued")
        .values(status="failed", error_code="staff_takeover")
    )
    held = await active_request(db, lead)
    if held is None:
        held = HumanRequest(
            id=uuid.uuid4(), tenant_id=staff.tenant_id, lead_id=lead.id, status="acknowledged"
        )
        db.add(held)
    elif held.status == "open":
        held.status = "acknowledged"
    lead.copilot_mode, lead.status = True, LeadStatus.HANDED_OFF
    await write_audit_log(
        db,
        tenant_id=staff.tenant_id,
        actor=str(staff.id),
        action="staff.takeover",
        lead_id=lead.id,
        details={"request_id": str(held.id)},
    )
    await db.commit()
    return {"copilot_mode": True, "request_id": str(held.id)}


@router.post("/{lead_id}/resume", dependencies=[Depends(require_browser_write)])
async def resume(lead_id: uuid.UUID, staff: Staff, db: Db) -> dict[str, bool]:
    lead = await get_lead(db, staff, lead_id, lock=True)
    request = await active_request(db, lead)
    if request is None and not lead.copilot_mode:
        return {"copilot_mode": False}
    await finish_takeover(db, lead)
    if request:
        request.status = "resumed"
    lead.status = await resumed_status(db, lead)
    await write_audit_log(
        db,
        tenant_id=staff.tenant_id,
        actor=str(staff.id),
        action="staff.resumed_ai",
        lead_id=lead.id,
    )
    await db.commit()
    return {"copilot_mode": False}


@router.post("/{lead_id}/messages", dependencies=[Depends(require_browser_write)])
async def send_message(
    lead_id: uuid.UUID, body: ManualMessage, staff: Staff, db: Db
) -> dict[str, str]:
    lead = await get_lead(db, staff, lead_id, lock=True)
    dedup = f"staff-message:{body.request_id}"
    previous = await db.scalar(
        select(OutboundMessage)
        .options(undefer(OutboundMessage.payload_enc))
        .where(OutboundMessage.tenant_id == staff.tenant_id, OutboundMessage.dedup_key == dedup)
    )
    if previous:
        if (
            previous.lead_id != lead.id
            or Reply.model_validate_json(decrypt_pii(previous.payload_enc)).text != body.text
        ):
            raise HTTPException(
                409, "This send reference was already used for a different message."
            )
        return {"id": str(previous.id), "status": previous.status}
    await require_takeover(db, lead)
    message_id = await enqueue_outbound(
        db,
        tenant_id=staff.tenant_id,
        lead_id=lead.id,
        kind="staff_reply",
        dedup_key=dedup,
        reply=Reply(text=body.text),
    )
    row, memory = await load_memory(db, lead)
    memory["staff_revision"] = int(memory.get("staff_revision", 0)) + 1
    row.payload_enc = encrypt_pii(json.dumps(memory, ensure_ascii=False))
    await write_audit_log(
        db,
        tenant_id=staff.tenant_id,
        actor=str(staff.id),
        action="staff.reply_queued",
        lead_id=lead.id,
        details={"message_id": str(message_id)},
    )
    await db.commit()
    return {"id": str(message_id), "status": "queued"}
