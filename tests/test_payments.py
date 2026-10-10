import hashlib
import hmac
import json
from pathlib import Path

import httpx
import pytest

from admitflow.adapters.razorpay import RazorpayAdapter
from admitflow.adapters.sqlite import Repository
from admitflow.services.payments import PaymentService


def make_qualified_lead(repository: Repository) -> int:
    lead_id = repository.upsert_lead(repository.tenant_id, "999", "demo-student")
    repository.update_lead(
        lead_id,
        selected_course_id="foundations-computing",
        completed_grade12=True,
        marks_percent=75,
        eligible=True,
        state="qualified",
    )
    return lead_id


@pytest.mark.asyncio
async def test_payment_link_uses_server_fee_and_stores_razorpay_result(tmp_path: Path) -> None:
    repository = Repository(tmp_path / "payments.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    lead_id = make_qualified_lead(repository)
    requested: list[httpx.Request] = []

    def respond(request: httpx.Request) -> httpx.Response:
        requested.append(request)
        return httpx.Response(
            200,
            json={"id": "plink_test_123", "short_url": "https://rzp.io/i/test123"},
        )

    adapter = RazorpayAdapter("rzp_test_key", "secret", transport=httpx.MockTransport(respond))
    service = PaymentService(repository, repository.tenant_id, adapter, "webhook-secret")

    offer = await service.create_for_qualified_lead(lead_id)

    assert offer == ("https://rzp.io/i/test123", 50000)
    payload = json.loads(requested[0].content)
    assert payload["amount"] == 50000
    assert payload["currency"] == "INR"
    assert payload["accept_partial"] is False
    assert payload["notes"] == {"lead_id": str(lead_id), "course_id": "foundations-computing"}
    payment = repository.get_payment_for_lead(repository.tenant_id, lead_id)
    assert payment is not None
    assert payment["status"] == "created"
    assert payment["razorpay_link_id"] == "plink_test_123"


@pytest.mark.asyncio
async def test_link_creation_failure_does_not_change_qualification(tmp_path: Path) -> None:
    repository = Repository(tmp_path / "payments.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    lead_id = make_qualified_lead(repository)

    def fail_request(request: httpx.Request) -> httpx.Response:
        return httpx.Response(502, json={"error": {"description": "test provider failure"}})

    adapter = RazorpayAdapter("rzp_test_key", "secret", transport=httpx.MockTransport(fail_request))
    service = PaymentService(repository, repository.tenant_id, adapter, "webhook-secret")

    with pytest.raises(httpx.HTTPStatusError):
        await service.create_for_qualified_lead(lead_id)

    payment = repository.get_payment_for_lead(repository.tenant_id, lead_id)
    assert payment is not None
    assert payment["status"] == "failed"
    assert repository.get_lead(lead_id)["eligible"] == 1  # type: ignore[index]


def test_paid_webhook_requires_signature_link_reference_and_full_amount(tmp_path: Path) -> None:
    repository = Repository(tmp_path / "payments.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    lead_id = make_qualified_lead(repository)
    payment, created = repository.get_or_create_payment_intent(
        repository.tenant_id, lead_id, "AF-test-reference"
    )
    assert created and payment is not None
    repository.save_payment_link(payment["id"], "plink_test_123", "https://rzp.io/i/test123")
    adapter = RazorpayAdapter("rzp_test_key", "secret")
    service = PaymentService(repository, repository.tenant_id, adapter, "webhook-secret")
    event = {
        "event": "payment_link.paid",
        "payload": {
            "payment_link": {
                "entity": {
                    "id": "plink_test_123",
                    "reference_id": "AF-test-reference",
                    "status": "paid",
                    "amount": 50000,
                    "amount_paid": 50000,
                    "currency": "INR",
                }
            }
        },
    }
    body = json.dumps(event).encode()
    signature = hmac.new(b"webhook-secret", body, hashlib.sha256).hexdigest()

    with pytest.raises(ValueError, match="signature"):
        service.apply_webhook(body, "wrong", "event-invalid")
    assert repository.get_payment_for_lead(repository.tenant_id, lead_id)["status"] == "created"  # type: ignore[index]
    partial_event = json.loads(body)
    partial_event["payload"]["payment_link"]["entity"]["amount_paid"] = 10000
    partial_body = json.dumps(partial_event).encode()
    partial_signature = hmac.new(b"webhook-secret", partial_body, hashlib.sha256).hexdigest()
    assert service.apply_webhook(partial_body, partial_signature, "event-partial") == "ignored"
    assert repository.get_payment_for_lead(repository.tenant_id, lead_id)["status"] == "created"  # type: ignore[index]
    assert service.apply_webhook(body, signature, "event-1") == "applied"
    assert service.apply_webhook(body, signature, "event-1") == "duplicate"
    assert repository.get_payment_for_lead(repository.tenant_id, lead_id)["status"] == "paid"  # type: ignore[index]


def test_live_mode_key_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="test-mode"):
        RazorpayAdapter("rzp_live_key", "secret")
