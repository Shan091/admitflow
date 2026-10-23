"""WhatsApp message sending service (Task 6).

Uses httpx2 to call the Meta Graph API to send outbound messages.
Supports text, interactive buttons, interactive lists, and template messages.
"""

from __future__ import annotations

from typing import Any

import httpx2

from src.core.settings import get_settings


class WhatsAppAPIError(RuntimeError):
    """Raised when the Meta Cloud API returns an error response."""


class WhatsAppSender:
    """Service for sending messages via Meta WhatsApp Cloud API."""

    def __init__(self) -> None:
        settings = get_settings()
        if not settings.whatsapp_access_token:
            raise RuntimeError("WHATSAPP_ACCESS_TOKEN is not configured")
        if not settings.whatsapp_phone_number_id:
            raise RuntimeError("WHATSAPP_PHONE_NUMBER_ID is not configured")

        self.access_token = settings.whatsapp_access_token
        self.phone_number_id = settings.whatsapp_phone_number_id
        version = settings.meta_graph_api_version

        self.base_url = f"https://graph.facebook.com/{version}/{self.phone_number_id}"

        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    async def _post(self, payload: dict[str, Any]) -> str:
        """Post the payload to Meta and extract the created message ID."""
        async with httpx2.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/messages",
                headers=self.headers,
                json=payload,
                timeout=10.0,
            )

            try:
                response.raise_for_status()
            except httpx2.HTTPStatusError as exc:
                # Try to extract the Meta error message if available
                error_msg = exc.response.text
                try:
                    data = exc.response.json()
                    if "error" in data and "message" in data["error"]:
                        error_msg = data["error"]["message"]
                except Exception:
                    pass
                raise WhatsAppAPIError(error_msg) from exc

            data = response.json()
            return str(data["messages"][0]["id"])

    def _strip_plus(self, phone: str) -> str:
        """Meta API expects the phone number without the leading '+'."""
        return phone.lstrip("+")

    async def send_text(self, to: str, text: str) -> str:
        """Send a simple text message.

        Returns the Meta message ID.
        """
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": self._strip_plus(to),
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
        return await self._post(payload)

    async def send_buttons(self, to: str, text: str, buttons: list[dict[str, str]]) -> str:
        """Send an interactive message with up to 3 buttons.

        `buttons` should be a list of dicts with 'id' and 'title'.
        """
        action_buttons = [
            {"type": "reply", "reply": {"id": btn["id"], "title": btn["title"]}} for btn in buttons
        ]

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": self._strip_plus(to),
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": text},
                "action": {"buttons": action_buttons},
            },
        }
        return await self._post(payload)

    async def send_list(
        self, to: str, text: str, button_text: str, sections: list[dict[str, Any]]
    ) -> str:
        """Send an interactive list message.

        `sections` is a list of section dicts conforming to the Meta API schema.
        """
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": self._strip_plus(to),
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {"text": text},
                "action": {"button": button_text, "sections": sections},
            },
        }
        return await self._post(payload)

    async def send_template(self, to: str, template_name: str, language_code: str = "en") -> str:
        """Send a pre-approved template message."""
        payload = {
            "messaging_product": "whatsapp",
            "to": self._strip_plus(to),
            "type": "template",
            "template": {"name": template_name, "language": {"code": language_code}},
        }
        return await self._post(payload)
