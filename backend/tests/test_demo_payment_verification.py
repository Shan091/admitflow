"""Only provider-authenticated, captured test payments can settle a local demo."""

import copy

import httpx2
import pytest

from src.payments.provider import Credentials, PaymentProviderError, RazorpayClient


@pytest.mark.parametrize(
    "change",
    [
        "none",
        "reference",
        "amount",
        "partial",
        "authorized",
        "payment",
        "currency",
        "refunded",
        "link_association",
    ],
)
async def test_test_confirmation_requires_exact_paid_link_and_captured_payment(change: str) -> None:
    reference = "a" * 32
    link = {
        "id": "plink_demo",
        "reference_id": reference,
        "amount": 300000,
        "amount_paid": 300000,
        "currency": "INR",
        "status": "paid",
        "payments": [
            {
                "payment_id": "pay_demo",
                "plink_id": "plink_demo",
                "amount": 300000,
                "status": "captured",
            }
        ],
    }
    payment = {
        "id": "pay_demo",
        "amount": 300000,
        "currency": "INR",
        "status": "captured",
        "captured": True,
        "amount_refunded": 0,
    }
    if change == "reference":
        link["reference_id"] = "b" * 32
    if change == "amount":
        link["amount_paid"] = 200000
    if change == "partial":
        link["status"] = "partially_paid"
    if change == "authorized":
        payment["status"] = "authorized"
        payment["captured"] = False
    if change == "payment":
        payment["id"] = "pay_other"
    if change == "currency":
        payment["currency"] = "USD"
    if change == "refunded":
        payment["amount_refunded"] = 300000
    if change == "link_association":
        link["payments"][0]["plink_id"] = "plink_other"
    if change == "none":
        # Exact fetched link/reference and its embedded payment ID bind the payment,
        # including provider responses that omit the optional inner plink_id.
        del link["payments"][0]["plink_id"]
    calls = []

    async def response(request: httpx2.Request) -> httpx2.Response:
        assert request.method == "GET"
        calls.append(request.url.path)
        return httpx2.Response(
            200, json=copy.deepcopy(link if "payment_links" in request.url.path else payment)
        )

    client = RazorpayClient(
        Credentials(
            key_id="rzp_test_synthetic",
            key_secret="synthetic-secret",
            webhook_secret="synthetic-webhook-secret",
        ),
        transport=httpx2.MockTransport(response),
    )
    if change == "none":
        event = await client.confirm_test_link("plink_demo", reference, 300000)
        assert event.payload.payment.entity.id == "pay_demo" and len(calls) == 2
    elif change == "partial":
        assert await client.confirm_test_link("plink_demo", reference, 300000) is None
    else:
        with pytest.raises(PaymentProviderError):
            await client.confirm_test_link("plink_demo", reference, 300000)


async def test_live_credentials_never_support_local_test_confirmation() -> None:
    client = RazorpayClient(
        Credentials(
            key_id="rzp_live_synthetic",
            key_secret="synthetic-secret",
            webhook_secret="synthetic-webhook-secret",
        ),
        allow_live=True,
    )
    with pytest.raises(ValueError):
        await client.confirm_test_link("plink_demo", "a" * 32, 300000)
