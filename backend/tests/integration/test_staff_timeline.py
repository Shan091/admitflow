"""All delivery types remain visible across stable, tenant-scoped transcript pages."""

import asyncio
from datetime import UTC, datetime, timedelta
from typing import Any

import pytest

from src.core.security import encrypt_pii
from src.db.models import ConversationEvent, OutboundMessage, TelegramBot
from src.engine.contracts import Reply
from src.telegram import service
from tests.integration.test_knowledge_workspace import signin
from tests.integration.test_knowledge_workspace import workspace as workspace
from tests.integration.test_telegram_journey import journey as journey

pytestmark = pytest.mark.integration


def test_transcript_paginates_inbound_bot_and_standalone_deliveries(
    journey: dict[str, Any],
) -> None:
    async def prepare():
        tenant = journey["tenants"][0]
        async with journey["sessions"]() as db:
            bot = TelegramBot(
                tenant_id=tenant, telegram_bot_id=732, token_enc=encrypt_pii("synthetic-token")
            )
            db.add(bot)
            await db.commit()
            bot_id = bot.id
        event_id = await service.accept_update(
            bot_id,
            {
                "update_id": 990,
                "message": {
                    "message_id": 990,
                    "from": {"id": 55},
                    "chat": {"id": 55, "type": "private"},
                    "text": "/start",
                },
            },
        )
        await service.process_event(event_id)
        async with journey["sessions"]() as db:
            event = await db.get(ConversationEvent, event_id)
            # Equal timestamps exercise the source/id tie-breaker across pages.
            stamp = datetime.now(UTC) + timedelta(seconds=1)
            for index in range(75):
                db.add(
                    OutboundMessage(
                        tenant_id=tenant,
                        lead_id=event.lead_id,
                        kind="payment_paid",
                        dedup_key=f"timeline:{index}",
                        payload_enc=encrypt_pii(
                            Reply(text=f"Confirmation {index}").model_dump_json()
                        ),
                        status="uncertain" if index == 0 else "sent",
                        created_at=stamp,
                    )
                )
            await db.commit()
            return event.lead_id

    lead_id = asyncio.run(prepare())
    client = journey["client"]
    signin(client)
    path = f"/api/staff/leads/{lead_id}"
    first = client.get(path).json()
    assert len(first["messages"]) == 50 and first["older_cursor"]
    second = client.get(path, params={"cursor": first["older_cursor"]}).json()
    assert len(second["messages"]) == 27 and second["older_cursor"] is None
    all_rows = second["messages"] + first["messages"]
    assert len({row["message_id"] for row in all_rows}) == 77
    assert all_rows[0]["direction"] == "inbound"
    assert any(row["kind"] == "payment_paid" and row["status"] == "uncertain" for row in all_rows)
    assert any(row["kind"] == "bot_reply" for row in all_rows)
    assert client.get(path, params={"cursor": "invalid"}).status_code == 400
    signin(client, "second")
    assert client.get(path, params={"cursor": first["older_cursor"]}).status_code == 404
