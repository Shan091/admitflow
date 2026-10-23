"""Immutable fee requests, bounded coupon reservations and non-repeating provider jobs."""

import asyncio
import json
import uuid
from typing import Any

import pytest
from sqlalchemy import func, select

from src.core.security import encrypt_pii
from src.db.enums import DiscountType, LeadStatus, PaymentStatus
from src.db.models import (
    Application,
    Batch,
    Course,
    DiscountCode,
    Institution,
    Lead,
    OutboundMessage,
    PaymentOrder,
)
from src.payments import service
from src.payments.provider import PaymentLink, PaymentProviderError, RazorpayClient
from tests.integration.test_knowledge_workspace import workspace as workspace

pytestmark = pytest.mark.integration


async def seed(
    workspace: dict[str, Any], discount: DiscountCode | None = None
) -> tuple[uuid.UUID, uuid.UUID]:
    tenant = workspace["tenants"][0]
    async with workspace["sessions"]() as db:
        institution = await db.get(Institution, tenant)
        institution.razorpay_credentials_enc = encrypt_pii(
            json.dumps(
                {
                    "key_id": "rzp_test_synthetic",
                    "key_secret": "synthetic-provider-secret",
                    "webhook_secret": "synthetic-webhook-secret",
                }
            )
        )
        course = Course(tenant_id=tenant, name="Synthetic payment course", application_fee=10000)
        db.add(course)
        await db.flush()
        batch = Batch(
            tenant_id=tenant, course_id=course.id, name="Morning", capacity=10, seats_remaining=10
        )
        db.add(batch)
        await db.flush()
        lead = Lead(
            tenant_id=tenant,
            current_course_id=course.id,
            current_batch_id=batch.id,
            status=LeadStatus.PAYMENT_PENDING,
        )
        db.add(lead)
        await db.flush()
        application = Application(
            tenant_id=tenant,
            lead_id=lead.id,
            course_id=course.id,
            batch_id=batch.id,
            full_name_enc=encrypt_pii("Synthetic applicant"),
        )
        db.add(application)
        if discount:
            db.add(discount)
        await db.commit()
        return lead.id, application.id


def test_immutable_request_and_concurrent_jobs_create_one_link(
    workspace: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(service, "get_sessionmaker", lambda: workspace["sessions"])
    monkeypatch.setattr(service, "get_settings", lambda: workspace["settings"])
    calls = 0

    async def create(self: RazorpayClient, reference: str, amount: int) -> PaymentLink:
        nonlocal calls
        calls += 1
        assert amount == 9000
        await asyncio.sleep(0.03)
        return PaymentLink(
            id="plink_synthetic",
            amount=amount,
            currency="INR",
            reference_id=reference,
            short_url="https://rzp.io/synthetic",
            status="created",
        )

    monkeypatch.setattr(RazorpayClient, "create_link", create)

    async def exercise() -> None:
        coupon = DiscountCode(
            tenant_id=workspace["tenants"][0],
            code="TEN",
            discount_type=DiscountType.PERCENT,
            amount=10,
            max_uses=1,
        )
        lead_id, application_id = await seed(workspace, coupon)
        async with workspace["sessions"]() as db:
            lead = await db.scalar(select(Lead).where(Lead.id == lead_id).with_for_update())
            order = await service.request_payment(db, lead, application_id, "TEN")
            order_id = order.id
            assert order.amount == 9000
            again = await service.request_payment(db, lead, application_id, None)
            assert again.id == order_id and again.amount == 9000
            await db.commit()
        assert calls == 0  # No provider operation inside the conversation transaction.
        await asyncio.gather(service.process_payment(order_id), service.process_payment(order_id))
        assert calls == 1
        async with workspace["sessions"]() as db:
            order = await db.get(PaymentOrder, order_id)
            assert order.creation_state == "created" and order.creation_attempts == 1
            assert order.payment_url_enc and "https://rzp.io" not in order.payment_url_enc
            assert (
                await db.scalar(
                    select(func.count())
                    .select_from(OutboundMessage)
                    .where(OutboundMessage.dedup_key == f"payment-link:{order_id}")
                )
                == 1
            )

    asyncio.run(exercise())


def test_ambiguous_creation_is_not_repeated(
    workspace: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(service, "get_sessionmaker", lambda: workspace["sessions"])
    monkeypatch.setattr(service, "get_settings", lambda: workspace["settings"])
    calls = 0

    async def fail(self: RazorpayClient, reference: str, amount: int) -> PaymentLink:
        nonlocal calls
        calls += 1
        raise PaymentProviderError("network_ambiguous", uncertain=True)

    monkeypatch.setattr(RazorpayClient, "create_link", fail)

    async def exercise() -> None:
        lead_id, application_id = await seed(workspace)
        async with workspace["sessions"]() as db:
            lead = await db.get(Lead, lead_id)
            order = await service.request_payment(db, lead, application_id)
            order_id = order.id
            await db.commit()
        await service.process_payment(order_id)
        await service.process_payment(order_id)
        assert calls == 1
        async with workspace["sessions"]() as db:
            order = await db.get(PaymentOrder, order_id)
            assert order.creation_state == "uncertain" and order.last_error == "network_ambiguous"

    asyncio.run(exercise())


def test_full_discount_is_recorded_as_waived_without_provider_call(
    workspace: dict[str, Any],
) -> None:
    async def exercise() -> None:
        coupon = DiscountCode(
            tenant_id=workspace["tenants"][0],
            code="WAIVER",
            discount_type=DiscountType.PERCENT,
            amount=100,
            max_uses=1,
        )
        lead_id, application_id = await seed(workspace, coupon)
        async with workspace["sessions"]() as db:
            lead = await db.get(Lead, lead_id)
            order = await service.request_payment(db, lead, application_id, "WAIVER")
            assert order.amount == 0 and order.status == PaymentStatus.WAIVED
            assert lead.status == LeadStatus.UNDER_REVIEW
            assert (
                coupon.uses_count == 0
            )  # Detached seed instance; reload to inspect the transaction.
            used = await db.scalar(
                select(DiscountCode).where(
                    DiscountCode.tenant_id == lead.tenant_id, DiscountCode.code == "WAIVER"
                )
            )
            assert used.uses_count == 1
            await db.commit()

    asyncio.run(exercise())
