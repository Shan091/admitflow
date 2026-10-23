"""Telegram inbox and outbox jobs contain only internal identifiers."""

import uuid

from sqlalchemy import select

from src.db.models import ConversationEvent, ConversationReply, PaymentOrder
from src.db.session import get_sessionmaker
from src.tasks.broker import broker
from src.tasks.payments import create_payment_link
from src.telegram.service import process_event, send_reply


@broker.task
async def process_telegram_event(event_id: str) -> None:
    await process_event(uuid.UUID(event_id))
    async with get_sessionmaker()() as db:
        reply_id = await db.scalar(
            select(ConversationReply.id).where(
                ConversationReply.event_id == uuid.UUID(event_id),
                ConversationReply.status == "queued",
            )
        )
    if reply_id:
        await send_reply(reply_id)
    async with get_sessionmaker()() as db:
        event = await db.get(ConversationEvent, uuid.UUID(event_id))
        if event is None:
            return
        orders = list(
            (
                await db.scalars(
                    select(PaymentOrder.id)
                    .where(
                        PaymentOrder.tenant_id == event.tenant_id,
                        PaymentOrder.lead_id == event.lead_id,
                        PaymentOrder.creation_state == "queued",
                    )
                    .limit(10)
                )
            ).all()
        )
    for order_id in orders:
        await create_payment_link.kiq(str(order_id))


@broker.task
async def send_telegram_reply(reply_id: str) -> None:
    await send_reply(uuid.UUID(reply_id))
