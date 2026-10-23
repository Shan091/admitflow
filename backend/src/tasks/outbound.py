"""Encrypted outbound-message delivery jobs carry only internal identifiers."""

import uuid

from src.tasks.broker import broker
from src.telegram.outbound import send_outbound


@broker.task
async def send_outbound_message(message_id: str) -> None:
    await send_outbound(uuid.UUID(message_id))
