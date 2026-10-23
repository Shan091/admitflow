"""Real database delivery claims, deduplication, ordering and ambiguous-send behavior."""

import asyncio
from typing import Any

import pytest
from sqlalchemy import select, update

from src.core.security import encrypt_pii
from src.db.models import (
    ConversationEvent,
    ConversationReply,
    IntegrationEvent,
    OutboundMessage,
    TelegramBot,
)
from src.engine.contracts import Reply
from src.telegram import outbound, service
from src.telegram.adapter import TelegramAPIError, TelegramClient
from tests.integration.test_knowledge_workspace import workspace as workspace
from tests.integration.test_telegram_journey import journey as journey

pytestmark = pytest.mark.integration


def test_outbound_dedup_claims_order_and_uncertainty(
    journey: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(outbound, "get_sessionmaker", lambda: journey["sessions"])
    calls = 0

    async def deliver(self: TelegramClient, chat_id: int, reply: Reply) -> int:
        nonlocal calls
        calls += 1
        assert chat_id == 73
        if reply.text == "Ambiguous delivery":
            raise TelegramAPIError(-1, uncertain=True)
        await asyncio.sleep(0.02)
        return 500 + calls

    monkeypatch.setattr(TelegramClient, "send", deliver)

    async def exercise() -> None:
        tenant = journey["tenants"][0]
        async with journey["sessions"]() as db:
            bot = TelegramBot(
                tenant_id=tenant, telegram_bot_id=431, token_enc=encrypt_pii("synthetic-token")
            )
            db.add(bot)
            await db.flush()
            bot_id = bot.id
            await db.commit()
        event_id = await service.accept_update(
            bot_id,
            {
                "update_id": 1,
                "message": {
                    "message_id": 1,
                    "from": {"id": 73},
                    "chat": {"id": 73, "type": "private"},
                    "text": "/start",
                },
            },
        )
        assert event_id is not None
        await service.process_event(event_id)
        async with journey["sessions"]() as db:
            event = await db.get(ConversationEvent, event_id)
            lead_id = event.lead_id
            first = await outbound.enqueue_outbound(
                db,
                tenant_id=tenant,
                lead_id=lead_id,
                kind="payment_link",
                dedup_key="link:synthetic",
                reply=Reply(text="Payment link ready"),
            )
            assert first == await outbound.enqueue_outbound(
                db,
                tenant_id=tenant,
                lead_id=lead_id,
                kind="payment_link",
                dedup_key="link:synthetic",
                reply=Reply(text="Payment link ready"),
            )
            await db.commit()
        await outbound.send_outbound(first)
        assert calls == 0  # The preceding conversation response must go first.
        async with journey["sessions"]() as db:
            await db.execute(
                update(ConversationReply)
                .where(ConversationReply.event_id == event_id)
                .values(status="sent")
            )
            await db.commit()
        await asyncio.gather(outbound.send_outbound(first), outbound.send_outbound(first))
        assert calls == 1
        async with journey["sessions"]() as db:
            stored = await db.get(OutboundMessage, first)
            assert stored.status == "sent" and stored.attempts == 1
            second = await outbound.enqueue_outbound(
                db,
                tenant_id=tenant,
                lead_id=lead_id,
                kind="payment_paid",
                dedup_key="paid:synthetic",
                reply=Reply(text="Ambiguous delivery"),
            )
            await db.commit()
        await outbound.send_outbound(second)
        await outbound.send_outbound(second)
        assert calls == 2
        async with journey["sessions"]() as db:
            stored = await db.get(OutboundMessage, second)
            assert stored.status == "uncertain" and stored.attempts == 1
            notifications = (
                await db.scalars(
                    select(IntegrationEvent).where(
                        IntegrationEvent.tenant_id == tenant,
                        IntegrationEvent.lead_id == lead_id,
                        IntegrationEvent.notification == "delivery",
                    )
                )
            ).all()
            assert len(notifications) == 1
            third = await outbound.enqueue_outbound(
                db,
                tenant_id=tenant,
                lead_id=lead_id,
                kind="payment_paid",
                dedup_key="paid:next",
                reply=Reply(text="Earlier payment confirmation"),
            )
            await db.commit()
        next_event = await service.accept_update(
            bot_id,
            {
                "update_id": 2,
                "message": {
                    "message_id": 2,
                    "from": {"id": 73},
                    "chat": {"id": 73, "type": "private"},
                    "text": "/start",
                },
            },
        )
        await service.process_event(next_event)
        async with journey["sessions"]() as db:
            reply_id = await db.scalar(
                select(ConversationReply.id).where(ConversationReply.event_id == next_event)
            )
        await service.send_reply(reply_id)
        assert calls == 2  # A later bot reply cannot overtake a pending standalone send.
        await asyncio.gather(outbound.send_outbound(third), outbound.send_outbound(third))
        assert calls == 3
        await asyncio.gather(service.send_reply(reply_id), service.send_reply(reply_id))
        assert calls == 4

    asyncio.run(exercise())
