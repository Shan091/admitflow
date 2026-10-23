"""Real database tenant ownership, deduplication and migration data-preservation gates."""

import asyncio
from typing import Any

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from src.core.security import encrypt_pii
from src.db.models import Application, Course, Lead, OutboundMessage, PaymentEvent, PaymentOrder
from tests.integration.test_knowledge_workspace import workspace as workspace

pytestmark = pytest.mark.integration


def test_payment_and_delivery_ownership_dedup_and_safe_downgrade(workspace: dict[str, Any]) -> None:
    async def exercise() -> None:
        first, second = workspace["tenants"]
        async with workspace["sessions"]() as db:
            lead = Lead(tenant_id=first)
            course = Course(tenant_id=first, name="Synthetic payment storage course")
            db.add_all([lead, course])
            await db.flush()
            application = Application(
                tenant_id=first,
                lead_id=lead.id,
                course_id=course.id,
                full_name_enc=encrypt_pii("Synthetic applicant"),
            )
            db.add(application)
            await db.flush()
            order = PaymentOrder(
                tenant_id=first,
                lead_id=lead.id,
                course_id=course.id,
                application_id=application.id,
                amount=10000,
                request_key=application.id.hex,
                creation_state="queued",
            )
            db.add(order)
            await db.flush()
            lead_id, order_id = lead.id, order.id
            await db.commit()
        async with workspace["sessions"]() as db:
            db.add(
                OutboundMessage(
                    tenant_id=second,
                    lead_id=lead_id,
                    dedup_key="wrong-owner",
                    kind="payment_link",
                    payload_enc=encrypt_pii("synthetic"),
                )
            )
            with pytest.raises(IntegrityError):
                await db.commit()
            await db.rollback()
            db.add(
                PaymentEvent(
                    tenant_id=second,
                    payment_order_id=order_id,
                    body_digest="0" * 64,
                    kind="payment_link.paid",
                )
            )
            with pytest.raises(IntegrityError):
                await db.commit()
            await db.rollback()
        async with workspace["sessions"]() as db:
            db.add(
                OutboundMessage(
                    tenant_id=first,
                    lead_id=lead_id,
                    dedup_key="payment-ready",
                    kind="payment_link",
                    payload_enc=encrypt_pii("synthetic"),
                )
            )
            db.add(
                PaymentEvent(
                    tenant_id=first,
                    payment_order_id=order_id,
                    body_digest="0" * 64,
                    kind="payment_link.paid",
                )
            )
            await db.commit()
            db.add(
                OutboundMessage(
                    tenant_id=first,
                    lead_id=lead_id,
                    dedup_key="payment-ready",
                    kind="payment_link",
                    payload_enc=encrypt_pii("synthetic"),
                )
            )
            with pytest.raises(IntegrityError):
                await db.commit()
            await db.rollback()
            db.add(
                PaymentEvent(
                    tenant_id=first,
                    payment_order_id=order_id,
                    body_digest="0" * 64,
                    kind="payment_link.paid",
                )
            )
            with pytest.raises(IntegrityError):
                await db.commit()
            await db.rollback()
            assert await db.scalar(select(func.count()).select_from(OutboundMessage)) == 1

    asyncio.run(exercise())
    with pytest.raises(RuntimeError, match="Refusing to discard"):
        command.downgrade(Config("alembic.ini"), "d82c0a75b912")

    async def preserved() -> None:
        async with workspace["sessions"]() as db:
            assert await db.scalar(select(func.count()).select_from(OutboundMessage)) == 1

    asyncio.run(preserved())
