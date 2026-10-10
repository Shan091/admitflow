"""Payment link orchestration and verified webhook application."""

import json
import secrets
from typing import Any

from admitflow.adapters.razorpay import RazorpayAdapter
from admitflow.adapters.sqlite import Repository


class PaymentService:
    def __init__(
        self,
        repository: Repository,
        tenant_id: str,
        razorpay: RazorpayAdapter,
        webhook_secret: str,
    ) -> None:
        self.repository = repository
        self.tenant_id = tenant_id
        self.razorpay = razorpay
        self.webhook_secret = webhook_secret

    async def create_for_qualified_lead(self, lead_id: int) -> tuple[str, int] | None:
        reference_id = f"AF-{lead_id}-{secrets.token_hex(6)}"
        payment, created = self.repository.get_or_create_payment_intent(
            self.tenant_id, lead_id, reference_id
        )
        if payment is None:
            return None
        if not created:
            if payment["status"] == "created" and payment["short_url"]:
                return str(payment["short_url"]), int(payment["amount_paise"])
            return None
        course = self.repository.get_course(self.tenant_id, str(payment["course_id"]))
        if course is None:
            self.repository.fail_payment_creation(int(payment["id"]))
            return None
        try:
            link_id, short_url = await self.razorpay.create_payment_link(
                amount_paise=int(payment["amount_paise"]),
                reference_id=str(payment["reference_id"]),
                description=f"Demo application fee - {course.name}",
                lead_id=lead_id,
                course_id=course.id,
            )
        except Exception:
            self.repository.fail_payment_creation(int(payment["id"]))
            raise
        self.repository.save_payment_link(int(payment["id"]), link_id, short_url)
        return short_url, int(payment["amount_paise"])

    def apply_webhook(self, body: bytes, signature: str, event_id: str) -> str:
        if not self.razorpay.verify_webhook_signature(body, signature, self.webhook_secret):
            raise ValueError("Invalid Razorpay webhook signature")
        try:
            event: Any = json.loads(body)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError("Invalid Razorpay webhook payload") from exc
        if not isinstance(event, dict) or event.get("event") != "payment_link.paid":
            return "ignored"
        return self.repository.apply_razorpay_paid_event(event_id, event)
