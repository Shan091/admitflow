"""Student-owned reminder preferences apply even while staff has paused the bot."""

from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.audit import write_audit_log
from src.db.models import Institution, Lead, OutboundMessage, TelegramBot
from src.engine.contracts import Event, Reply
from src.engine.journey import button, copy
from src.telegram.callbacks import parse_callback


async def cancel_queued(db: AsyncSession, lead: Lead, reason: str) -> None:
    await db.execute(
        update(OutboundMessage)
        .where(
            OutboundMessage.tenant_id == lead.tenant_id,
            OutboundMessage.lead_id == lead.id,
            OutboundMessage.kind == "followup",
            OutboundMessage.status == "queued",
        )
        .values(status="failed", error_code=reason)
    )


async def note_inbound(db: AsyncSession, lead: Lead, memory: dict[str, Any], now: datetime) -> None:
    lead.last_inbound_at = now
    await cancel_queued(db, lead, "followup_new_activity")
    claim = memory.get("followup_claim", {})
    if claim.get("status") in {"generating", "queued"}:
        claim["status"] = "cancelled"
    institution = await db.get(Institution, lead.tenant_id)
    lead.followup_due_at = (
        now + timedelta(days=institution.reengagement_delay_days)
        if institution and lead.followup_consent and lead.reengagement_attempts < 2
        else None
    )


async def preference_reply(
    db: AsyncSession,
    lead: Lead,
    bot: TelegramBot,
    event: Event,
    memory: dict[str, Any],
    now: datetime,
) -> Reply | None:
    command = (event.text.strip().split() or [""])[0].split("@")[0].lower()
    choice = "off" if event.kind == "text" and command == "/stop" else None
    if event.kind == "callback":
        try:
            kind, target = parse_callback(event.text, lead.id, bot.id)
            if kind == "reminders" and target in {"on", "off"}:
                choice = target
        except ValueError:
            pass
    if choice is not None:
        lead.followup_consent = choice == "on"
        lead.followup_consent_updated_at = now
        institution = await db.get(Institution, lead.tenant_id)
        lead.followup_due_at = (
            now + timedelta(days=institution.reengagement_delay_days)
            if choice == "on" and institution and lead.reengagement_attempts < 2
            else None
        )
        if choice == "off":
            await cancel_queued(db, lead, "followup_opt_out")
        await write_audit_log(
            db,
            tenant_id=lead.tenant_id,
            actor="student",
            lead_id=lead.id,
            action="followup.opted_in" if choice == "on" else "followup.opted_out",
        )
        return Reply(
            text=copy(
                "reminders_on"
                if choice == "on" and lead.reengagement_attempts < 2
                else "reminders_limit"
                if choice == "on"
                else "reminders_off",
                memory,
            )
        )
    if event.kind == "text" and command == "/followups":
        return Reply(
            text=copy("reminders_prompt", memory),
            buttons=[
                button(copy("reminders_enable", memory), "reminders", "on", lead, bot),
                button(copy("reminders_disable", memory), "reminders", "off", lead, bot),
            ],
        )
    return None
