"""Student-confirmed context reset is separate from deletion and institutional review."""

import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.audit import write_audit_log
from src.db.enums import LeadStatus
from src.db.models import Application, HumanRequest, Lead, TelegramBot
from src.engine.contracts import Event, Reply
from src.telegram.callbacks import parse_callback


def is_reset_event(event: Event) -> bool:
    return (event.kind == "text" and event.text.strip().split("@")[0].lower() == "/reset") or (
        event.kind == "callback" and event.text.startswith("reset:")
    )


async def reset_reply(
    db: AsyncSession, lead: Lead, bot: TelegramBot, event: Event, memory: dict[str, Any]
) -> Reply | None:
    from src.engine.journey import button, copy

    if not is_reset_event(event):
        return None
    if event.kind == "text":
        new_nonce = uuid.uuid4().hex[:12]
        memory["reset_nonce"] = new_nonce
        return Reply(
            text="Start a fresh conversation? This clears chat memory and any unfinished "
            "application draft. Submitted applications, payments and staff requests stay saved.",
            buttons=[
                button("Start fresh", "reset", f"yes-{new_nonce}", lead, bot),
                button("Keep this conversation", "reset", f"no-{new_nonce}", lead, bot),
            ],
        )
    try:
        kind, target = parse_callback(event.text, lead.id, bot.id)
    except ValueError:
        return Reply(text=copy("stale", memory))
    nonce = memory.get("reset_nonce")
    if kind != "reset" or not nonce or target not in {f"yes-{nonce}", f"no-{nonce}"}:
        return Reply(text=copy("stale", memory))
    memory.pop("reset_nonce", None)
    if target.startswith("no-"):
        return Reply(text="Kept your conversation. We can continue where you left off.")
    submitted = await db.scalar(
        select(Application.id)
        .where(Application.tenant_id == lead.tenant_id, Application.lead_id == lead.id)
        .limit(1)
    )
    held = await db.scalar(
        select(HumanRequest.id)
        .where(
            HumanRequest.tenant_id == lead.tenant_id,
            HumanRequest.lead_id == lead.id,
            HumanRequest.status != "resumed",
        )
        .limit(1)
    )
    handoff = memory.get("handoff")
    memory.clear()
    memory.update(
        facts={},
        language="en",
        history_after=datetime.now(UTC).isoformat(),
        callback_after_message_id=event.message_id,
    )
    if handoff and held:
        memory["handoff"] = handoff
    if not submitted and not held and not lead.copilot_mode:
        lead.current_course_id, lead.current_batch_id = None, None
        lead.status, lead.readiness_score = LeadStatus.NEW, None
    await write_audit_log(
        db,
        tenant_id=lead.tenant_id,
        lead_id=lead.id,
        actor="student",
        action="conversation.context_reset",
        details={
            "submitted_preserved": bool(submitted),
            "staff_owned": bool(held or lead.copilot_mode),
        },
    )
    if held or lead.copilot_mode:
        return Reply(text="Chat memory cleared. This conversation stays with the admissions team.")
    if submitted:
        return Reply(
            text="Chat memory cleared. Your submitted application is still saved. "
            "You can ask institution questions or use /human to change the application."
        )
    return Reply(
        text="Fresh start. What are you interested in studying, or would you like help exploring?"
    )
