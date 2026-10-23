"""Money stays integer/code-owned; signatures use exact bytes; creation never retries blindly."""

import hashlib
import hmac

import httpx2
import pytest

from src.payments.provider import Credentials, PaymentProviderError, RazorpayClient
from src.payments.rules import discounted_amount, verify_webhook


def test_discounts_use_minor_units_and_boundaries() -> None:
    assert discounted_amount(10025, "percent", 10) == 9023
    assert discounted_amount(10025, "flat", 1500) == 8525
    assert discounted_amount(10025, "percent", 100) == 0
    assert discounted_amount(10025, "flat", 20000) == 0
    for amount, kind, value in [
        (100, "percent", 101),
        (-1, "flat", 10),
        (True, "flat", 1),
        (100, "flat", -1),
    ]:
        with pytest.raises(ValueError):
            discounted_amount(amount, kind, value)


def test_webhook_signature_uses_raw_body_and_rejects_tampering() -> None:
    body = b'{"event":"payment_link.paid"}'
    signature = hmac.new(b"synthetic-webhook-secret", body, hashlib.sha256).hexdigest()
    assert verify_webhook(body, signature, "synthetic-webhook-secret")
    assert not verify_webhook(body + b" ", signature, "synthetic-webhook-secret")
    assert not verify_webhook(body, signature, "another-secret")
    assert not verify_webhook(body, "", "synthetic-webhook-secret")


async def test_payment_creation_does_not_retry_ambiguous_network_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = 0

    async def fail(request: httpx2.Request) -> httpx2.Response:
        nonlocal calls
        calls += 1
        raise httpx2.ReadTimeout("synthetic timeout", request=request)

    client = RazorpayClient(
        Credentials(
            key_id="rzp_test_synthetic",
            key_secret="synthetic-secret",
            webhook_secret="synthetic-webhook-secret",
        ),
        transport=httpx2.MockTransport(fail),
    )
    with pytest.raises(PaymentProviderError) as caught:
        await client.create_link("a" * 32, 10000)
    assert caught.value.uncertain is True and calls == 1
    assert "synthetic-secret" not in str(caught.value)


async def test_payment_link_amount_reference_and_host_are_validated() -> None:
    async def response(request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(
            200,
            json={
                "id": "plink_synthetic",
                "amount": 10000,
                "currency": "INR",
                "reference_id": "a" * 32,
                "short_url": "https://attacker.example/payment",
                "status": "created",
            },
        )

    client = RazorpayClient(
        Credentials(
            key_id="rzp_test_synthetic",
            key_secret="synthetic-secret",
            webhook_secret="synthetic-webhook-secret",
        ),
        transport=httpx2.MockTransport(response),
    )
    with pytest.raises(PaymentProviderError) as caught:
        await client.create_link("a" * 32, 10000)
    assert caught.value.uncertain is True


async def test_reconciliation_only_reads_one_exact_reference() -> None:
    reference = "b" * 32
    calls = []

    async def response(request: httpx2.Request) -> httpx2.Response:
        calls.append(request.method)
        assert request.url.params["reference_id"] == reference
        assert request.url.params["count"] == "2"
        return httpx2.Response(
            200,
            json={
                "payment_links": [
                    {
                        "id": "plink_recovered",
                        "amount": 10000,
                        "currency": "INR",
                        "reference_id": reference,
                        "short_url": "https://rzp.io/recovered",
                        "status": "created",
                    }
                ]
            },
        )

    client = RazorpayClient(
        Credentials(
            key_id="rzp_test_synthetic",
            key_secret="synthetic-secret",
            webhook_secret="synthetic-webhook-secret",
        ),
        transport=httpx2.MockTransport(response),
    )
    assert (await client.find_link(reference, 10000)).id == "plink_recovered"
    assert calls == ["GET"]
    with pytest.raises(PaymentProviderError):
        await client.find_link(reference, 9000)


@pytest.mark.parametrize("links", [[], [{}, {}]])
async def test_reconciliation_missing_or_ambiguous_reference_never_creates(links) -> None:
    async def response(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "GET"
        return httpx2.Response(200, json={"payment_links": links})

    client = RazorpayClient(
        Credentials(
            key_id="rzp_test_synthetic",
            key_secret="synthetic-secret",
            webhook_secret="synthetic-webhook-secret",
        ),
        transport=httpx2.MockTransport(response),
    )
    if not links:
        assert await client.find_link("a" * 32, 10000) is None
    else:
        with pytest.raises(PaymentProviderError):
            await client.find_link("a" * 32, 10000)
