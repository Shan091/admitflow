"""Razorpay test-mode Payment Links API and webhook signature verification."""

import hashlib
import hmac
from typing import Any
from urllib.parse import urlparse

import httpx


class RazorpayAdapter:
    """Thin API adapter. Test-mode key prefix is required to prevent live requests."""

    def __init__(
        self,
        key_id: str,
        key_secret: str,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        if not key_id.startswith("rzp_test_"):
            raise ValueError("Razorpay test-mode key IDs must start with 'rzp_test_'")
        self.key_id = key_id
        self.key_secret = key_secret
        self.transport = transport

    async def create_payment_link(
        self,
        *,
        amount_paise: int,
        reference_id: str,
        description: str,
        lead_id: int,
        course_id: str,
    ) -> tuple[str, str]:
        if amount_paise <= 0:
            raise ValueError("Payment amount must be positive")
        payload = {
            "amount": amount_paise,
            "currency": "INR",
            "accept_partial": False,
            "reference_id": reference_id,
            "description": description,
            "reminder_enable": False,
            "notify": {"sms": False, "email": False},
            "notes": {"lead_id": str(lead_id), "course_id": course_id},
        }
        async with httpx.AsyncClient(
            auth=(self.key_id, self.key_secret),
            timeout=15,
            transport=self.transport,
        ) as client:
            response = await client.post("https://api.razorpay.com/v1/payment_links", json=payload)
            response.raise_for_status()
        data: Any = response.json()
        link_id = data.get("id") if isinstance(data, dict) else None
        short_url = data.get("short_url") if isinstance(data, dict) else None
        parsed = urlparse(short_url) if isinstance(short_url, str) else None
        if (
            not isinstance(link_id, str)
            or not link_id
            or parsed is None
            or parsed.scheme != "https"
            or parsed.hostname != "rzp.io"
        ):
            raise ValueError("Razorpay returned an invalid Payment Link")
        return link_id, str(short_url)

    @staticmethod
    def verify_webhook_signature(body: bytes, signature: str, secret: str) -> bool:
        expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(signature, expected)
