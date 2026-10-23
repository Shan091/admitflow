"""Signed payment events cannot change amounts, leak tenants or repeat confirmations."""

import asyncio
import hashlib
import hmac
import json
import uuid
from typing import Any

import pytest
from sqlalchemy import func, select

from src.db.enums import ApplicationStatus, LeadStatus, PaymentStatus
from src.db.models import Application, Lead, OutboundMessage, PaymentEvent, PaymentOrder
from src.engine.contracts import Reply
from src.payments.service import request_payment
from src.telegram.outbound import enqueue_outbound
from tests.integration.test_knowledge_workspace import workspace as workspace
from tests.integration.test_payment_jobs import seed

pytestmark = pytest.mark.integration


def test_signed_full_payment_is_atomic_replay_safe_and_amount_checked(
    workspace: dict[str, Any],
) -> None:
    async def prepare() -> tuple[uuid.UUID, uuid.UUID, uuid.UUID]:
        lead_id, application_id = await seed(workspace)
        async with workspace["sessions"]() as db:
            lead = await db.get(Lead, lead_id)
            order = await request_payment(db, lead, application_id)
            order.creation_state = "uncertain"
            await enqueue_outbound(
                db,
                tenant_id=lead.tenant_id,
                lead_id=lead.id,
                kind="payment_link",
                dedup_key=f"payment-link:{order.id}",
                reply=Reply(text="Old payable link"),
            )
            await db.commit()
            return lead_id, application_id, order.id

    lead_id, application_id, order_id = asyncio.run(prepare())
    tenant = workspace["tenants"][0]
    path = f"/api/payments/webhook/{tenant}"
    client = workspace["client"]

    def payload(amount: int = 10000, status: str = "captured") -> bytes:
        return json.dumps(
            {
                "event": "payment_link.paid",
                "payload": {
                    "payment_link": {
                        "entity": {
                            "id": "plink_verified",
                            "reference_id": order_id.hex,
                            "amount": amount,
                            "amount_paid": amount,
                            "currency": "INR",
                            "status": "paid",
                        }
                    },
                    "payment": {
                        "entity": {
                            "id": "pay_verified",
                            "amount": amount,
                            "currency": "INR",
                            "status": status,
                        }
                    },
                },
            },
            separators=(",", ":"),
        ).encode()

    def send(body: bytes, signature: str | None = None) -> Any:
        if signature is None:
            signature = hmac.new(b"synthetic-webhook-secret", body, hashlib.sha256).hexdigest()
        return client.post(
            path,
            content=body,
            headers={"X-Razorpay-Signature": signature, "Content-Type": "application/json"},
        )

    assert send(payload(), "0" * 64).status_code == 401
    assert send(payload(1)).status_code in {400, 409}
    assert send(payload(status="authorized")).status_code == 400
    assert send(b"x" * 300000).status_code == 413
    accepted = send(payload())
    assert accepted.status_code == 200, accepted.text
    assert send(payload()).status_code == 200

    async def verify() -> None:
        async with workspace["sessions"]() as db:
            order = await db.get(PaymentOrder, order_id)
            assert order.status == PaymentStatus.PAID and order.amount == 10000
            assert order.razorpay_payment_id == "pay_verified"
            application = await db.get(Application, application_id)
            lead = await db.get(Lead, lead_id)
            assert (
                application.status == ApplicationStatus.UNDER_REVIEW
                and lead.status == LeadStatus.UNDER_REVIEW
            )
            assert (
                await db.scalar(
                    select(func.count())
                    .select_from(PaymentEvent)
                    .where(PaymentEvent.payment_order_id == order_id)
                )
                == 1
            )
            assert (
                await db.scalar(
                    select(func.count())
                    .select_from(OutboundMessage)
                    .where(OutboundMessage.dedup_key == f"payment-paid:{order_id}")
                )
                == 1
            )
            assert "email" not in json.dumps(order.webhook_event)
            old_link = await db.scalar(
                select(OutboundMessage).where(
                    OutboundMessage.dedup_key == f"payment-link:{order.id}"
                )
            )
            assert old_link.status == "failed" and old_link.error_code == "payment_already_settled"

    asyncio.run(verify())
