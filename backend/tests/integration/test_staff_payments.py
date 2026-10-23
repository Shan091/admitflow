"""Payment monitoring stays scoped; reconciliation cannot create or infer settlement."""

import asyncio
from typing import Any

import pytest
from sqlalchemy import func, select

from src.core.security import decrypt_pii
from src.db.enums import PaymentStatus
from src.db.models import Lead, OutboundMessage, PaymentOrder
from src.payments import service
from src.payments.provider import PaymentLink, RazorpayClient
from tests.integration.test_knowledge_workspace import signin
from tests.integration.test_knowledge_workspace import workspace as workspace
from tests.integration.test_payment_jobs import seed

pytestmark = pytest.mark.integration
HEADERS = {"X-AdmitFlow-Request": "1"}


def test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment(
    workspace: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    from src.staff import payments

    monkeypatch.setattr(payments, "get_settings", lambda: workspace["settings"])
    calls = 0
    provider_status = "created"

    async def find(self: RazorpayClient, reference: str, amount: int) -> PaymentLink | None:
        nonlocal calls
        calls += 1
        return PaymentLink(
            id="plink_reconciled",
            amount=amount,
            currency="INR",
            reference_id=reference,
            short_url="https://rzp.io/reconciled",
            status=provider_status,
        )

    async def create(*args, **kwargs):
        raise AssertionError("Reconciliation must not create a payment")

    monkeypatch.setattr(RazorpayClient, "find_link", find)
    monkeypatch.setattr(RazorpayClient, "create_link", create)

    async def prepare():
        lead_id, application_id = await seed(workspace)
        async with workspace["sessions"]() as db:
            order = await service.request_payment(db, await db.get(Lead, lead_id), application_id)
            order.creation_state = "uncertain"
            order.creation_attempts = 1
            await db.commit()
            return order.id

    order_id = asyncio.run(prepare())
    client = workspace["client"]
    path = f"/api/staff/payments/{order_id}/reconcile"
    assert client.get("/api/staff/payments").status_code == 401
    signin(client, "second")
    assert client.post(path, headers=HEADERS).status_code == 404
    signin(client, email="agent@example.test")
    assert client.get("/api/staff/payments").status_code == 200
    assert client.post(path, headers=HEADERS).status_code == 403
    signin(client)
    assert client.post(path).status_code == 403
    assert calls == 0
    for _ in range(2):
        result = client.post(path, headers=HEADERS)
        assert result.status_code == 200, result.text
        assert result.json()["result"] == "link_recovered"
    provider_status = "paid"
    assert client.post(path, headers=HEADERS).json()["result"] == "awaiting_signed_confirmation"
    assert client.post(f"/api/staff/payments/{order_id}/retry", headers=HEADERS).status_code == 409

    async def verify():
        async with workspace["sessions"]() as db:
            order = await db.get(PaymentOrder, order_id)
            assert order.status == PaymentStatus.CREATED
            assert order.creation_attempts == 1 and not order.payment_link_sent
            assert decrypt_pii(order.payment_url_enc) == "https://rzp.io/reconciled"
            assert (
                await db.scalar(
                    select(func.count())
                    .select_from(OutboundMessage)
                    .where(OutboundMessage.dedup_key == f"payment-link:{order_id}")
                )
                == 1
            )

    asyncio.run(verify())
    listing = client.get("/api/staff/payments").json()
    record = next(row for row in listing if row["id"] == str(order_id))
    assert record["amount"] == 10000 and record["delivery_status"] == "failed"
    assert "payment_url_enc" not in record and "rzp.io" not in str(record)


def test_absent_link_does_not_clear_uncertainty_or_authorize_retry(
    workspace: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    from src.staff import payments

    monkeypatch.setattr(payments, "get_settings", lambda: workspace["settings"])

    async def missing(*args, **kwargs):
        return None

    monkeypatch.setattr(RazorpayClient, "find_link", missing)

    async def prepare():
        lead_id, application_id = await seed(workspace)
        async with workspace["sessions"]() as db:
            order = await service.request_payment(db, await db.get(Lead, lead_id), application_id)
            order.creation_state = "uncertain"
            order.last_error = "network_ambiguous"
            await db.commit()
            return order.id

    order_id = asyncio.run(prepare())
    client = workspace["client"]
    signin(client)
    base = f"/api/staff/payments/{order_id}"
    assert client.post(base + "/reconcile", headers=HEADERS).json()["result"] == "not_found"
    assert client.post(base + "/retry", headers=HEADERS).status_code == 409

    async def verify():
        async with workspace["sessions"]() as db:
            order = await db.get(PaymentOrder, order_id)
            assert order.creation_state == "uncertain" and order.last_error == "network_ambiguous"

    asyncio.run(verify())


def test_known_configuration_failure_can_only_requeue_same_bounded_invoice(
    workspace: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    from src.staff import payments

    monkeypatch.setattr(payments, "get_settings", lambda: workspace["settings"])

    async def prepare():
        lead_id, application_id = await seed(workspace)
        async with workspace["sessions"]() as db:
            order = await service.request_payment(db, await db.get(Lead, lead_id), application_id)
            order.creation_state = "failed"
            order.creation_attempts = 1
            order.last_error = "configuration_unavailable"
            await db.commit()
            return order.id

    order_id = asyncio.run(prepare())
    client = workspace["client"]
    signin(client)
    path = f"/api/staff/payments/{order_id}/retry"
    assert client.post(path, headers=HEADERS).json()["result"] == "queued"
    assert client.post(path, headers=HEADERS).status_code == 409

    async def verify():
        async with workspace["sessions"]() as db:
            order = await db.get(PaymentOrder, order_id)
            assert order.creation_state == "queued" and order.amount == 10000
            assert order.creation_attempts == 1 and order.request_key == order.application_id.hex

    asyncio.run(verify())
