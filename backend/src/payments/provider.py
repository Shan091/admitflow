"""Bounded Razorpay requests; ambiguous link creation is never blindly retried."""

import re
from typing import Literal
from urllib.parse import urlsplit

import httpx2
from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator


class Credentials(BaseModel):
    model_config = ConfigDict(extra="forbid")
    key_id: str = Field(pattern=r"^rzp_(test|live)_[A-Za-z0-9]+$")
    key_secret: SecretStr = Field(min_length=8)
    webhook_secret: SecretStr = Field(min_length=8)


class PaymentLink(BaseModel):
    id: str = Field(pattern=r"^plink_[A-Za-z0-9]+$")
    amount: int = Field(ge=100, strict=True)
    currency: Literal["INR"]
    reference_id: str = Field(min_length=1, max_length=40)
    short_url: str = Field(max_length=2048)
    status: Literal["created", "paid", "partially_paid", "cancelled", "expired"]

    @field_validator("short_url")
    @classmethod
    def provider_url(cls, value: str) -> str:
        parsed = urlsplit(value)
        if (
            parsed.scheme != "https"
            or parsed.hostname not in {"rzp.io", "rzp.in"}
            or parsed.username
            or parsed.password
            or parsed.port not in {None, 443}
        ):
            raise ValueError("Unexpected payment link host")
        return value


class PaymentProviderError(Exception):
    def __init__(self, code: str, *, uncertain: bool) -> None:
        self.code = code
        self.uncertain = uncertain
        super().__init__(code)


class RazorpayClient:
    def __init__(
        self,
        credentials: Credentials,
        *,
        allow_live: bool = False,
        transport: httpx2.AsyncBaseTransport | None = None,
    ) -> None:
        if credentials.key_id.startswith("rzp_live_") and not allow_live:
            raise ValueError("Live payment creation is not enabled")
        self.credentials = credentials
        self.transport = transport

    async def find_link(self, reference: str, amount: int) -> PaymentLink | None:
        """Read an existing exact reference; absence never authorizes another creation."""
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,40}", reference):
            raise ValueError("Invalid payment reference")
        try:
            async with httpx2.AsyncClient(
                base_url="https://api.razorpay.com/v1/",
                timeout=20,
                auth=(self.credentials.key_id, self.credentials.key_secret.get_secret_value()),
                follow_redirects=False,
                transport=self.transport,
            ) as client:
                response = await client.get(
                    "payment_links/", params={"reference_id": reference, "count": 2}
                )
        except httpx2.HTTPError:
            raise PaymentProviderError("lookup_unavailable", uncertain=True) from None
        if response.status_code != 200:
            raise PaymentProviderError(f"provider_{response.status_code}", uncertain=True)
        try:
            value = response.json()
            links = value["payment_links"]
            if not isinstance(links, list) or len(links) > 1:
                raise ValueError("Ambiguous payment reference")
            if not links:
                return None
            link = PaymentLink.model_validate(links[0])
            if link.amount != amount or link.reference_id != reference:
                raise ValueError("Unexpected payment link details")
            return link
        except (KeyError, ValueError, TypeError):
            raise PaymentProviderError("invalid_lookup_response", uncertain=True) from None

    async def create_link(self, reference: str, amount: int) -> PaymentLink:
        if type(amount) is not int or not 100 <= amount <= 1000000000:
            raise ValueError("Payment amount must be integer paise of at least INR 1")
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,40}", reference):
            raise ValueError("Invalid payment reference")
        try:
            async with httpx2.AsyncClient(
                base_url="https://api.razorpay.com/v1/",
                timeout=20,
                auth=(self.credentials.key_id, self.credentials.key_secret.get_secret_value()),
                follow_redirects=False,
                transport=self.transport,
            ) as client:
                response = await client.post(
                    "payment_links",
                    json={
                        "amount": amount,
                        "currency": "INR",
                        "accept_partial": False,
                        "reference_id": reference,
                        "description": "Institution application fee",
                        "notify": {"sms": False, "email": False},
                        "reminder_enable": False,
                    },
                )
        except httpx2.HTTPError:
            raise PaymentProviderError("network_ambiguous", uncertain=True) from None
        if response.status_code not in {200, 201}:
            raise PaymentProviderError(
                f"provider_{response.status_code}", uncertain=response.status_code >= 500
            )
        try:
            link = PaymentLink.model_validate(response.json())
            if link.amount != amount or link.reference_id != reference or link.status != "created":
                raise ValueError("Unexpected payment link details")
        except (ValueError, TypeError):
            raise PaymentProviderError("invalid_response", uncertain=True) from None
        return link
