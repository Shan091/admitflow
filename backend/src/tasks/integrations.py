"""Integration queue messages contain identifiers only."""

import uuid

from src.integrations.delivery import deliver
from src.tasks.broker import broker


@broker.task
async def send_webhook(tenant_id: str, delivery_id: str) -> None:
    await deliver(uuid.UUID(tenant_id), uuid.UUID(delivery_id))
