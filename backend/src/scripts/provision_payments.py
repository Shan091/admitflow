"""Read-only credential probe, then encrypted institution-owned Razorpay provisioning."""

import argparse
import asyncio
import json

import httpx2
from sqlalchemy import select

from src.core.security import encrypt_pii
from src.core.settings import get_settings
from src.db.audit import write_audit_log
from src.db.models import Institution
from src.db.session import get_engine, get_sessionmaker
from src.payments.provider import Credentials, RazorpayClient


async def provision(code: str) -> None:
    settings = get_settings()
    if not (
        settings.razorpay_key_id
        and settings.razorpay_key_secret
        and settings.razorpay_webhook_secret
    ):
        raise ValueError("Set the three RAZORPAY credential settings locally first")
    credentials = Credentials(
        key_id=settings.razorpay_key_id.get_secret_value(),
        key_secret=settings.razorpay_key_secret,
        webhook_secret=settings.razorpay_webhook_secret,
    )
    # This enforces the explicit live-mode guard even though the probe creates nothing.
    RazorpayClient(
        credentials, allow_live=settings.app_env == "prod" and settings.payments_live_enabled
    )
    async with httpx2.AsyncClient(
        timeout=20,
        follow_redirects=False,
        auth=(credentials.key_id, credentials.key_secret.get_secret_value()),
    ) as client:
        result = await client.get("https://api.razorpay.com/v1/payment_links", params={"count": 1})
        if result.status_code != 200:
            raise ValueError("Razorpay read-only credential probe did not pass")
    async with get_sessionmaker()() as db:
        institution = await db.scalar(
            select(Institution).where(Institution.slug == code).with_for_update()
        )
        if institution is None:
            raise ValueError("Institution code not found")
        institution.razorpay_credentials_enc = encrypt_pii(
            json.dumps(
                {
                    "key_id": credentials.key_id,
                    "key_secret": credentials.key_secret.get_secret_value(),
                    "webhook_secret": credentials.webhook_secret.get_secret_value(),
                }
            )
        )
        await write_audit_log(
            db,
            tenant_id=institution.id,
            actor="local-provisioning",
            action="payments.credentials_provisioned",
        )
        await db.commit()
    print(
        "Payment credentials verified read-only and saved encrypted. No payment link was created."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--institution-code", required=True)
    args = parser.parse_args()

    async def run() -> None:
        try:
            await provision(args.institution_code)
        finally:
            await get_engine().dispose()

    try:
        asyncio.run(run())
    except Exception as error:
        print(
            f"Payment provisioning failed: {type(error).__name__}. "
            "Check local settings and provider access."
        )
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
