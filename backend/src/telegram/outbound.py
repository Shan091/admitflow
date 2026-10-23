"""Durable deliveries for explicit staff replies, payment events and consented outreach."""

import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import undefer

from src.core.security import decrypt_pii, encrypt_pii
from src.db.enums import PaymentStatus
from src.db.models import (
    ConversationEvent,
    ConversationReply,
    Institution,
    Lead,
    OutboundMessage,
    PaymentOrder,
    TelegramBot,
    TelegramIdentity,
)
from src.db.session import get_sessionmaker
from src.engine.contracts import Reply
from src.telegram import budget
from src.telegram.adapter import TelegramAPIError, TelegramClient


async def enqueue_outbound(
    db: AsyncSession,
    *,
    tenant_id: uuid.UUID,
    lead_id: uuid.UUID,
    kind: str,
    dedup_key: str,
    reply: Reply,
) -> uuid.UUID:
    body = Reply.model_validate(reply.model_dump())
    if not 1 <= len(dedup_key) <= 128 or not 1 <= len(kind) <= 32:
        raise ValueError("Invalid outbound reference")
    created = await db.scalar(
        insert(OutboundMessage)
        .values(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            lead_id=lead_id,
            kind=kind,
            dedup_key=dedup_key,
            payload_enc=encrypt_pii(body.model_dump_json()),
            status="queued",
            attempts=0,
        )
        .on_conflict_do_nothing(constraint="uq_outbound_tenant_dedup")
        .returning(OutboundMessage.id)
    )
    if created:
        return uuid.UUID(str(created))
    existing = await db.scalar(
        select(OutboundMessage.id).where(
            OutboundMessage.tenant_id == tenant_id,
            OutboundMessage.lead_id == lead_id,
            OutboundMessage.dedup_key == dedup_key,
        )
    )
    if existing is None:
        raise ValueError("Outbound reference belongs to another inquiry")
    return existing


async def send_outbound(message_id: uuid.UUID) -> None:
    sessions = get_sessionmaker()
    async with sessions() as db:
        reference = (
            await db.execute(
                select(OutboundMessage.lead_id, OutboundMessage.tenant_id).where(
                    OutboundMessage.id == message_id, OutboundMessage.status == "queued"
                )
            )
        ).first()
        if reference is None:
            return
        lead = await db.scalar(
            select(Lead)
            .where(Lead.tenant_id == reference.tenant_id, Lead.id == reference.lead_id)
            .with_for_update()
        )
        if lead is None:
            return
        # Load after taking the lead lock, so a competing worker cannot reuse stale queued state.
        message = await db.scalar(
            select(OutboundMessage)
            .options(undefer(OutboundMessage.payload_enc))
            .where(
                OutboundMessage.id == message_id,
                OutboundMessage.tenant_id == lead.tenant_id,
                OutboundMessage.status == "queued",
            )
        )
        now = datetime.now(UTC)
        if message is None or (message.next_attempt_at and message.next_attempt_at > now):
            return
        older = await db.scalar(
            select(OutboundMessage.id)
            .where(
                OutboundMessage.tenant_id == lead.tenant_id,
                OutboundMessage.lead_id == lead.id,
                OutboundMessage.status.in_(["queued", "sending"]),
                (OutboundMessage.status == "sending")
                | (OutboundMessage.created_at < message.created_at)
                | (
                    (OutboundMessage.created_at == message.created_at)
                    & (OutboundMessage.id < message.id)
                ),
            )
            .limit(1)
        )
        reply_pending = await db.scalar(
            select(ConversationReply.id)
            .join(ConversationEvent, ConversationEvent.id == ConversationReply.event_id)
            .where(
                ConversationEvent.tenant_id == lead.tenant_id,
                ConversationEvent.lead_id == lead.id,
                ConversationReply.status.in_(["queued", "sending"]),
                (ConversationReply.status == "sending")
                | (ConversationReply.created_at <= message.created_at),
            )
            .limit(1)
        )
        if older or reply_pending:
            return
        if message.kind == "followup":
            from src.outreach.followups import before_send

            if not await before_send(db, lead, message, now):
                await db.commit()
                return
        routing = (
            await db.execute(
                select(TelegramIdentity, TelegramBot)
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
                .order_by(TelegramIdentity.created_at)
                .limit(1)
            )
        ).first()
        if routing is None:
            message.status, message.error_code = "failed", "routing_unavailable"
            await db.commit()
            return
        identity, bot = routing
        token = decrypt_pii(bot.token_enc)
        chat_id = int(decrypt_pii(identity.chat_id_enc))
        body = Reply.model_validate_json(decrypt_pii(message.payload_enc))
        institution = await db.get(Institution, lead.tenant_id)
        if institution is None:
            return
        reservation = await budget.reserve(
            institution, f"o:{message_id}:{message.attempts + 1}", now=now
        )
        if not reservation.allowed:
            message.next_attempt_at, message.error_code = reservation.retry_at, reservation.reason
            await db.commit()
            return
        if message.kind == "followup" and message.attempts == 0:
            lead.reengagement_attempts += 1
            lead.followup_due_at = None
        message.status = "sending"
        message.attempts += 1
        tenant_id, lead_id = lead.tenant_id, lead.id
        kind, dedup_key = message.kind, message.dedup_key
        await db.commit()
    state, error, message_reference, next_attempt = "sent", None, None, None
    try:
        message_reference = await TelegramClient(token).send(chat_id, body)
    except TelegramAPIError as failure:
        state = "uncertain" if failure.uncertain else "failed"
        error = f"telegram_{failure.code}"
        if failure.code == 429:
            state = "queued"
            next_attempt = datetime.now(UTC) + timedelta(seconds=max(failure.retry_after, 1))
    except Exception:
        state, error = "uncertain", "delivery_unknown"
    async with sessions() as db:
        await db.execute(
            update(OutboundMessage)
            .where(
                OutboundMessage.id == message_id,
                OutboundMessage.tenant_id == tenant_id,
                OutboundMessage.status == "sending",
            )
            .values(
                status=state,
                error_code=error,
                telegram_message_id=message_reference,
                next_attempt_at=next_attempt,
            )
        )
        if state == "sent":
            await db.execute(
                update(Lead)
                .where(Lead.id == lead_id, Lead.tenant_id == tenant_id)
                .values(last_outbound_at=datetime.now(UTC))
            )
            if kind == "payment_link" and dedup_key.startswith("payment-link:"):
                order_id = uuid.UUID(dedup_key.split(":", 1)[1])
                order = await db.scalar(
                    select(PaymentOrder)
                    .where(
                        PaymentOrder.id == order_id,
                        PaymentOrder.tenant_id == tenant_id,
                        PaymentOrder.lead_id == lead_id,
                    )
                    .with_for_update()
                )
                if order:
                    order.payment_link_sent = True
                    if order.status == PaymentStatus.CREATED:
                        order.status = PaymentStatus.LINK_SENT
        if kind == "followup":
            from src.outreach.followups import after_send

            await after_send(db, tenant_id, lead_id, dedup_key, state, datetime.now(UTC))
        await db.commit()
        if state == "sent":
            await budget.record_sent(reservation)


async def recover_outbound() -> None:
    from src.tasks.outbound import send_outbound_message

    async with get_sessionmaker()() as db:
        await db.execute(
            update(OutboundMessage)
            .where(
                OutboundMessage.status == "sending",
                OutboundMessage.updated_at < datetime.now(UTC) - timedelta(seconds=90),
            )
            .values(status="uncertain", error_code="worker_interrupted")
        )
        ids = list(
            (
                await db.scalars(
                    select(OutboundMessage.id)
                    .where(
                        OutboundMessage.status == "queued",
                        (OutboundMessage.next_attempt_at.is_(None))
                        | (OutboundMessage.next_attempt_at <= datetime.now(UTC)),
                    )
                    .order_by(OutboundMessage.created_at, OutboundMessage.id)
                    .limit(100)
                )
            ).all()
        )
        await db.commit()
    for message_id in ids:
        await send_outbound_message.kiq(str(message_id))
