"""A student must confirm a fresh code-owned fee quote; retries cannot create another invoice."""

import asyncio
from typing import Any

import pytest
from sqlalchemy import func, select, update

from src.core.security import encrypt_pii
from src.db.enums import PaymentStatus
from src.db.models import Course, Institution, Lead, PaymentOrder, TelegramBot
from src.payments.conversation import payment_action
from src.telegram.callbacks import parse_callback
from tests.integration.test_knowledge_workspace import workspace as workspace
from tests.integration.test_payment_jobs import seed
from tests.integration.test_telegram_journey import journey as journey

pytestmark = pytest.mark.integration


def test_unconfigured_payments_do_not_offer_a_payment_request_or_staff_handoff(journey):
    async def exercise():
        lead_id, application_id = await seed(journey)
        async with journey["sessions"]() as db:
            lead = await db.get(Lead, lead_id)
            institution = await db.get(Institution, lead.tenant_id)
            institution.razorpay_credentials_enc = None
            memory = {"payment_quote": {"nonce": "old"}}
            reply = await payment_action(
                db, lead, TelegramBot(), memory, f"review-{application_id.hex}"
            )
            assert "not available yet" in reply.text and "100.00" in reply.text
            assert not reply.buttons and "payment_quote" not in memory
            assert "staff" not in reply.text.lower()
            assert await db.scalar(select(func.count()).select_from(PaymentOrder)) == 0

    asyncio.run(exercise())


def test_fee_changes_require_another_tap_and_legacy_paid_orders_are_not_charged_again(
    journey: dict[str, Any],
) -> None:
    async def exercise() -> None:
        lead_id, application_id = await seed(journey)
        async with journey["sessions"]() as db:
            lead = await db.get(Lead, lead_id)
            bot = TelegramBot(
                tenant_id=lead.tenant_id,
                telegram_bot_id=873,
                token_enc=encrypt_pii("synthetic-token"),
            )
            db.add(bot)
            await db.flush()
            memory: dict[str, Any] = {}
            preview = await payment_action(db, lead, bot, memory, f"review-{application_id.hex}")
            assert "100.00" in preview.text
            assert await db.scalar(select(func.count()).select_from(PaymentOrder)) == 0
            _, old_target = parse_callback(preview.buttons[0].data, lead.id, bot.id)
            await db.execute(
                update(Course)
                .where(Course.id == lead.current_course_id)
                .values(application_fee=12000)
            )
            changed = await payment_action(db, lead, bot, memory, old_target)
            assert "changed" in changed.text and "120.00" in changed.text
            assert await db.scalar(select(func.count()).select_from(PaymentOrder)) == 0
            stale = await payment_action(db, lead, bot, memory, old_target)
            assert "expired" in stale.text
            _, current_target = parse_callback(changed.buttons[0].data, lead.id, bot.id)
            reply = await payment_action(db, lead, bot, memory, current_target)
            assert "being prepared" in reply.text
            await payment_action(db, lead, bot, memory, current_target)
            assert await db.scalar(select(func.count()).select_from(PaymentOrder)) == 1
            order = await db.scalar(
                select(PaymentOrder).where(PaymentOrder.application_id == application_id)
            )
            assert order.amount == 12000
            order.status = PaymentStatus.PAID
            order.request_key = None
            await db.flush()
            receipt = await payment_action(db, lead, bot, memory, f"review-{application_id.hex}")
            assert "confirmed" in receipt.text
            assert await db.scalar(select(func.count()).select_from(PaymentOrder)) == 1
            await db.commit()

    asyncio.run(exercise())
