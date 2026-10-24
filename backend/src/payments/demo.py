"""Bounded, read-only Razorpay test checks for explicitly enabled local demos."""

import asyncio
import uuid
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import select, update

from src.core.demo_admissions import demo_fee
from src.core.security import decrypt_pii
from src.core.settings import get_settings
from src.db.enums import PaymentStatus
from src.db.models import Application, Course, Institution, PaymentOrder
from src.db.session import get_sessionmaker
from src.payments.confirmation import settle_payment
from src.payments.provider import Credentials, PaymentProviderError, RazorpayClient


async def check_demo_payment(order_id: uuid.UUID) -> bool:
    sessions = get_sessionmaker()
    async with sessions() as db:
        order = await db.scalar(
            select(PaymentOrder).where(
                PaymentOrder.id == order_id,
                PaymentOrder.is_demo.is_(True),
                PaymentOrder.status.not_in([PaymentStatus.PAID, PaymentStatus.WAIVED]),
            )
        )
        if order is None or not order.razorpay_payment_link_id:
            return False
        course = await db.scalar(
            select(Course).where(
                Course.id == order.course_id,
                Course.tenant_id == order.tenant_id,
            )
        )
        application = await db.scalar(
            select(Application).where(
                Application.id == order.application_id,
                Application.tenant_id == order.tenant_id,
                Application.lead_id == order.lead_id,
                Application.is_demo.is_(True),
            )
        )
        if course is None or application is None or await demo_fee(db, course) is None:
            return False
        institution = await db.get(Institution, order.tenant_id)
        if institution is None or not institution.razorpay_credentials_enc:
            return False
        client = RazorpayClient(
            Credentials.model_validate_json(decrypt_pii(institution.razorpay_credentials_enc))
        )
        tenant_id, amount, link_id = order.tenant_id, order.amount, order.razorpay_payment_link_id
    event = await client.confirm_test_link(link_id, order_id.hex, amount)
    if event is None:
        return False
    raw = ("razorpay-test-lookup:" + event.model_dump_json()).encode()
    async with sessions() as db:
        result = await settle_payment(tenant_id, event, raw, db, test_lookup=True)
        return result["status"] in {"confirmed", "duplicate"}


async def check_demo_payments() -> int:
    settings = get_settings()
    if (
        settings.app_env != "dev"
        or not settings.demo_admissions_enabled
        or settings.payments_live_enabled
    ):
        return 0
    async with get_sessionmaker()() as db:
        ids = list(
            (
                await db.scalars(
                    select(PaymentOrder.id)
                    .where(
                        PaymentOrder.is_demo.is_(True),
                        PaymentOrder.creation_state == "created",
                        PaymentOrder.status.not_in([PaymentStatus.PAID, PaymentStatus.WAIVED]),
                        PaymentOrder.created_at >= datetime.now(UTC) - timedelta(days=7),
                        (PaymentOrder.next_attempt_at.is_(None))
                        | (PaymentOrder.next_attempt_at <= datetime.now(UTC)),
                    )
                    .order_by(PaymentOrder.next_attempt_at.asc().nulls_first(), PaymentOrder.id)
                    .limit(10)
                )
            ).all()
        )
        if ids:
            await db.execute(
                update(PaymentOrder)
                .where(PaymentOrder.id.in_(ids))
                .values(
                    next_attempt_at=datetime.now(UTC) + timedelta(seconds=60),
                )
            )
            await db.commit()

    async def check(order_id: uuid.UUID) -> bool:
        try:
            return await check_demo_payment(order_id)
        except (PaymentProviderError, HTTPException, ValueError):
            return False  # Durable invoice stays unpaid; no provider payload is logged.

    return sum(await asyncio.gather(*(check(order_id) for order_id in ids)))
