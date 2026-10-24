"""Durable private-chat intake and transactional engine/outbox processing."""

import logging
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.orm import undefer

from src.core.security import decrypt_pii, encrypt_pii
from src.db.audit import write_audit_log
from src.db.models import (
    ConversationEvent,
    ConversationReply,
    Institution,
    Lead,
    OutboundMessage,
    TelegramBot,
    TelegramIdentity,
)
from src.db.session import get_sessionmaker
from src.engine.contracts import Event, Reply
from src.staff.throttle import consume_limit
from src.telegram import budget
from src.telegram.adapter import TelegramAPIError, TelegramClient, normalize_update
from src.telegram.identity import hash_telegram_identifier

logger = logging.getLogger(__name__)


async def accept_update(bot_id: uuid.UUID, raw: dict[str, Any]) -> uuid.UUID | None:
    """Commit the encrypted inbox and offset in the same transaction, before acknowledging."""
    async with get_sessionmaker()() as db:
        bot = await db.scalar(
            select(TelegramBot)
            .where(TelegramBot.id == bot_id, TelegramBot.is_active.is_(True))
            .with_for_update()
        )
        if bot is None:
            raise ValueError("Unknown or inactive bot")
        event = normalize_update(raw, bot.telegram_bot_id)
        raw_id = raw.get("update_id")
        if isinstance(raw_id, bool) or not isinstance(raw_id, int) or raw_id < 0:
            raise ValueError("Invalid update identifier")
        existing = await db.scalar(
            select(ConversationEvent.id).where(
                ConversationEvent.bot_id == bot.id, ConversationEvent.update_id == raw_id
            )
        )
        if existing:
            return existing
        if bot.last_update_id is not None and raw_id <= bot.last_update_id:
            return None  # Old replay beyond the durable polling checkpoint.
        bot.last_update_id = raw_id
        if event is None:
            await db.commit()
            return None
        user_hash = hash_telegram_identifier(
            bot.tenant_id, bot.telegram_bot_id, "user", event.user_id
        )
        chat_hash = hash_telegram_identifier(
            bot.tenant_id, bot.telegram_bot_id, "chat", event.chat_id
        )
        identity = await db.scalar(
            select(TelegramIdentity).where(
                TelegramIdentity.tenant_id == bot.tenant_id,
                TelegramIdentity.bot_id == bot.id,
                TelegramIdentity.user_hash == user_hash,
                TelegramIdentity.chat_hash == chat_hash,
            )
        )
        if identity is None:
            lead = Lead(tenant_id=bot.tenant_id)
            db.add(lead)
            await db.flush()
            identity = TelegramIdentity(
                tenant_id=bot.tenant_id,
                bot_id=bot.id,
                lead_id=lead.id,
                user_hash=user_hash,
                chat_hash=chat_hash,
                user_id_enc=encrypt_pii(str(event.user_id)),
                chat_id_enc=encrypt_pii(str(event.chat_id)),
            )
            db.add(identity)
            await db.flush()
        record = ConversationEvent(
            tenant_id=bot.tenant_id,
            bot_id=bot.id,
            lead_id=identity.lead_id,
            identity_id=identity.id,
            update_id=raw_id,
            kind=event.kind,
            payload_enc=encrypt_pii(event.model_dump_json()),
            status="queued",
        )
        db.add(record)
        await db.flush()
        record_id = record.id
        await db.commit()
        if event.callback_id:
            try:
                await TelegramClient(decrypt_pii(bot.token_enc)).acknowledge(event.callback_id)
            except TelegramAPIError:
                logger.info("telegram_callback_ack_unavailable event=%s", record_id)
        return record_id


async def process_event(event_id: uuid.UUID) -> None:
    """Serialize by locked lead, then atomically commit memory, result and one reply."""
    import json

    from src.engine.journey import build_reply, load_memory
    from src.engine.session_controls import is_reset_event
    from src.outreach.consent import note_inbound, preference_reply

    async with get_sessionmaker()() as db:
        reference = await db.get(ConversationEvent, event_id)
        if reference is None:
            return
        lead = await db.scalar(
            select(Lead)
            .where(Lead.id == reference.lead_id, Lead.tenant_id == reference.tenant_id)
            .with_for_update()
        )
        event = await db.scalar(
            select(ConversationEvent)
            .options(undefer(ConversationEvent.payload_enc))
            .where(ConversationEvent.id == event_id)
            .with_for_update()
            .execution_options(populate_existing=True)
        )
        if lead is None or event is None or event.status != "queued":
            return
        earlier = await db.scalar(
            select(ConversationEvent.id)
            .where(
                ConversationEvent.tenant_id == event.tenant_id,
                ConversationEvent.lead_id == event.lead_id,
                ConversationEvent.update_id < event.update_id,
                ConversationEvent.status == "queued",
            )
            .limit(1)
        )
        if earlier:
            return  # Delivery order is recovered by the durable queue sweep.
        bot = await db.get(TelegramBot, event.bot_id)
        if bot is None or not bot.is_active:
            return
        payload = Event.model_validate_json(decrypt_pii(event.payload_enc))
        now = datetime.now(UTC)
        memory_row, memory = await load_memory(db, lead)
        await note_inbound(db, lead, memory, now)
        preference = await preference_reply(db, lead, bot, payload, memory, now)
        memory_row.payload_enc = encrypt_pii(json.dumps(memory, ensure_ascii=False))
        if lead.copilot_mode and preference is None and not is_reset_event(payload):
            # Consent/opt-out commands still apply while staff owns normal replies.
            event.status = "done"
            await db.commit()
            return
        try:
            if preference is not None:
                reply = preference
            else:
                await consume_limit(f"telegram-chat:{lead.id}", 30)
                await consume_limit(f"telegram-tenant:{lead.tenant_id}", 300)
                async with TelegramClient(decrypt_pii(bot.token_enc)).typing(payload.chat_id):
                    reply = await build_reply(db, lead, bot, payload)
        except HTTPException:
            reply = Reply(
                text="Please pause and try again in a few minutes. "
                "Your message is saved; the service is temporarily busy."
            )
        # Every branch, including canned replies, crosses the same validation boundary.
        reply = Reply.model_validate(reply.model_dump())
        db.add(
            ConversationReply(
                tenant_id=event.tenant_id,
                event_id=event.id,
                payload_enc=encrypt_pii(reply.model_dump_json()),
            )
        )
        event.status = "done"
        lead.last_inbound_at = datetime.now(UTC)
        await db.commit()


async def send_reply(reply_id: uuid.UUID) -> None:
    sessions = get_sessionmaker()
    async with sessions() as db:
        now = datetime.now(UTC)
        reference = (
            await db.execute(
                select(
                    ConversationEvent.lead_id,
                    ConversationEvent.tenant_id,
                    ConversationEvent.update_id,
                    ConversationReply.created_at,
                )
                .join(ConversationReply, ConversationReply.event_id == ConversationEvent.id)
                .where(ConversationReply.id == reply_id, ConversationReply.status == "queued")
            )
        ).first()
        if reference is None:
            return
        await db.scalar(
            select(Lead)
            .where(Lead.id == reference.lead_id, Lead.tenant_id == reference.tenant_id)
            .with_for_update()
        )
        earlier_outbound = await db.scalar(
            select(OutboundMessage.id)
            .where(
                OutboundMessage.lead_id == reference.lead_id,
                OutboundMessage.tenant_id == reference.tenant_id,
                (OutboundMessage.status == "sending")
                | (
                    (OutboundMessage.status == "queued")
                    & (OutboundMessage.created_at < reference.created_at)
                ),
            )
            .limit(1)
        )
        if earlier_outbound:
            return
        earlier = await db.scalar(
            select(ConversationReply.id)
            .join(ConversationEvent, ConversationEvent.id == ConversationReply.event_id)
            .where(
                ConversationEvent.lead_id == reference.lead_id,
                ConversationEvent.tenant_id == reference.tenant_id,
                ConversationEvent.update_id < reference.update_id,
                ConversationReply.status.in_(["queued", "sending"]),
            )
            .limit(1)
        )
        if earlier:
            return  # Do not let a later response overtake a pending send in this conversation.
        pending = await db.scalar(
            select(ConversationReply).where(
                ConversationReply.id == reply_id,
                ConversationReply.status == "queued",
                (ConversationReply.next_attempt_at.is_(None))
                | (ConversationReply.next_attempt_at <= now),
            )
        )
        institution = await db.get(Institution, reference.tenant_id)
        if pending is None or institution is None:
            return
        reservation = await budget.reserve(
            institution, f"r:{reply_id}:{pending.attempts + 1}", now=now
        )
        if not reservation.allowed:
            pending.next_attempt_at, pending.error_code = reservation.retry_at, reservation.reason
            await db.commit()
            return
        row = (
            await db.execute(
                update(ConversationReply)
                .where(
                    ConversationReply.id == reply_id,
                    ConversationReply.status == "queued",
                    (ConversationReply.next_attempt_at.is_(None))
                    | (ConversationReply.next_attempt_at <= now),
                )
                .values(status="sending", attempts=ConversationReply.attempts + 1)
                .returning(
                    ConversationReply.event_id,
                    ConversationReply.payload_enc,
                    ConversationReply.attempts,
                )
            )
        ).first()
        await db.commit()
        if row is None:
            return
        event = await db.get(ConversationEvent, row.event_id)
        if event is None:
            return
        bot = await db.scalar(
            select(TelegramBot).where(
                TelegramBot.id == event.bot_id,
                TelegramBot.tenant_id == event.tenant_id,
                TelegramBot.is_active.is_(True),
            )
        )
        identity = await db.scalar(
            select(TelegramIdentity).where(
                TelegramIdentity.id == event.identity_id,
                TelegramIdentity.tenant_id == event.tenant_id,
                TelegramIdentity.bot_id == event.bot_id,
                TelegramIdentity.lead_id == event.lead_id,
            )
        )
        status = "failed"
        code: str | None = "routing_unavailable"
        message_id: int | None = None
        next_attempt: datetime | None = None
        if bot and identity:
            try:
                reply = Reply.model_validate_json(decrypt_pii(row.payload_enc))
                message_id = await TelegramClient(decrypt_pii(bot.token_enc)).send(
                    int(decrypt_pii(identity.chat_id_enc)), reply
                )
                status, code = "sent", None
            except TelegramAPIError as error:
                status = "uncertain" if error.uncertain else "failed"
                code = f"telegram_{error.code}"
                if error.code == 429:
                    status = "queued"
                    next_attempt = datetime.now(UTC) + timedelta(seconds=max(error.retry_after, 1))
            except Exception:
                status, code = "failed", "invalid_reply"
        delivered = await db.execute(
            update(ConversationReply)
            .where(ConversationReply.id == reply_id, ConversationReply.status == "sending")
            .values(
                status=status,
                error_code=code,
                telegram_message_id=message_id,
                next_attempt_at=next_attempt,
            )
            .returning(ConversationReply.id)
        )
        if delivered.first() and status in {"failed", "uncertain"}:
            await write_audit_log(
                db,
                tenant_id=event.tenant_id,
                lead_id=event.lead_id,
                actor="telegram-delivery",
                action="delivery.attention",
                details={"reply_id": str(reply_id)},
            )
        if status == "sent":
            await db.execute(
                update(Lead)
                .where(Lead.id == event.lead_id, Lead.tenant_id == event.tenant_id)
                .values(last_outbound_at=datetime.now(UTC))
            )
        await db.commit()
        if status == "sent":
            await budget.record_sent(reservation)


async def recover_pending() -> None:
    from src.tasks.telegram import process_telegram_event, send_telegram_reply

    async with get_sessionmaker()() as db:
        interrupted = await db.execute(
            update(ConversationReply)
            .where(
                ConversationReply.status == "sending",
                ConversationReply.updated_at < datetime.now(UTC) - timedelta(seconds=90),
            )
            .values(status="uncertain", error_code="worker_interrupted")
            .returning(ConversationReply.event_id)
        )
        interrupted_ids = list(interrupted.scalars())
        if interrupted_ids:
            affected = (
                await db.scalars(
                    select(ConversationEvent).where(ConversationEvent.id.in_(interrupted_ids))
                )
            ).all()
            for event in affected:
                await write_audit_log(
                    db,
                    tenant_id=event.tenant_id,
                    lead_id=event.lead_id,
                    actor="telegram-recovery",
                    action="delivery.attention",
                    details={"event_id": str(event.id)},
                )
        events = list(
            (
                await db.scalars(
                    select(ConversationEvent.id)
                    .where(ConversationEvent.status == "queued")
                    .order_by(ConversationEvent.created_at, ConversationEvent.update_id)
                    .limit(100)
                )
            ).all()
        )
        replies = list(
            (
                await db.scalars(
                    select(ConversationReply.id)
                    .where(
                        ConversationReply.status == "queued",
                        (ConversationReply.next_attempt_at.is_(None))
                        | (ConversationReply.next_attempt_at <= datetime.now(UTC)),
                    )
                    .order_by(ConversationReply.created_at)
                    .limit(100)
                )
            ).all()
        )
        await db.commit()
    for event_id in events:
        await process_telegram_event.kiq(str(event_id))
    for reply_id in replies:
        await send_telegram_reply.kiq(str(reply_id))
    from src.payments.service import recover_payments
    from src.telegram.outbound import recover_outbound

    await recover_payments()
    await recover_outbound()
