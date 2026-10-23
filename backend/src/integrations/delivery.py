"""Leased at-least-once webhook delivery with stable recipient deduplication IDs."""

import asyncio
import json
import logging
import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy import or_, select, update

from src.core.security import decrypt_pii
from src.db.models import IntegrationEvent, Lead, WebhookDelivery, WebhookEndpoint
from src.db.session import get_sessionmaker
from src.integrations.transport import post_event

logger = logging.getLogger(__name__)
MAX_ATTEMPTS = 6
LEASE_SECONDS = 60


async def deliver(tenant_id: uuid.UUID, delivery_id: uuid.UUID) -> None:
    now = datetime.now(UTC)
    lease = uuid.uuid4()
    sessions = get_sessionmaker()
    async with sessions() as db:
        subject = (
            await db.execute(
                select(IntegrationEvent.lead_id)
                .join(
                    WebhookDelivery,
                    (WebhookDelivery.event_id == IntegrationEvent.id)
                    & (WebhookDelivery.tenant_id == IntegrationEvent.tenant_id),
                )
                .where(WebhookDelivery.id == delivery_id, WebhookDelivery.tenant_id == tenant_id)
            )
        ).first()
        if subject is None:
            return
        if (
            subject.lead_id is not None
            and await db.scalar(
                select(Lead.id)
                .where(Lead.tenant_id == tenant_id, Lead.id == subject.lead_id)
                .with_for_update()
            )
            is None
        ):
            return
        row = await db.scalar(
            select(WebhookDelivery)
            .where(WebhookDelivery.id == delivery_id, WebhookDelivery.tenant_id == tenant_id)
            .with_for_update()
        )
        if (
            row is None
            or row.status != "queued"
            or (row.next_attempt_at and row.next_attempt_at > now)
        ):
            return
        endpoint = await db.scalar(
            select(WebhookEndpoint).where(
                WebhookEndpoint.id == row.endpoint_id, WebhookEndpoint.tenant_id == tenant_id
            )
        )
        event = await db.scalar(
            select(IntegrationEvent).where(
                IntegrationEvent.id == row.event_id, IntegrationEvent.tenant_id == tenant_id
            )
        )
        if (
            not endpoint
            or not endpoint.enabled
            or endpoint.generation != row.generation
            or event is None
        ):
            row.status, row.error_code = "cancelled", "configuration_changed"
            await db.commit()
            return
        if row.attempts >= MAX_ATTEMPTS:
            row.status, row.error_code = "dead", "attempt_limit"
            await db.commit()
            return
        row.status, row.lease_id = "sending", lease
        row.attempts += 1
        attempts = row.attempts
        row.next_attempt_at = now + timedelta(seconds=LEASE_SECONDS)
        url, secret = decrypt_pii(endpoint.url_enc), decrypt_pii(endpoint.secret_enc)
        body = json.dumps(
            {
                "id": str(event.id),
                "type": event.kind,
                "institution_id": str(tenant_id),
                "inquiry_id": str(event.lead_id) if event.lead_id else None,
                "state": event.state,
                "created_at": event.created_at.isoformat(),
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
        await db.commit()
    state = "queued"
    code: str | None = "transport_unavailable"
    try:
        status = await post_event(
            url, secret, str(delivery_id), str(int(datetime.now(UTC).timestamp())), body
        )
        state, code = ("sent", None) if 200 <= status < 300 else ("queued", f"http_{status}")
        if 300 <= status < 500 and status not in {408, 429}:
            state = "dead"  # No redirects or retry of configuration/auth failures.
    except ValueError:
        state, code = "dead", "destination_blocked"
    except Exception:
        # Never log the exception: transport errors can contain URL credentials.
        pass
    if state == "queued" and attempts >= MAX_ATTEMPTS:
        state = "dead"
    async with sessions() as db:
        await db.execute(
            update(WebhookDelivery)
            .where(
                WebhookDelivery.id == delivery_id,
                WebhookDelivery.tenant_id == tenant_id,
                WebhookDelivery.status == "sending",
                WebhookDelivery.lease_id == lease,
            )
            .values(
                status=state,
                error_code=code,
                lease_id=None,
                next_attempt_at=datetime.now(UTC)
                + timedelta(seconds=min(3600, 30 * 2 ** (attempts - 1)))
                if state == "queued"
                else None,
            )
        )
        await db.commit()


async def dispatch_pending() -> None:
    from src.tasks.integrations import send_webhook

    now = datetime.now(UTC)
    async with get_sessionmaker()() as db:
        # A crashed attempt might have reached the receiver. Replay uses the same
        # delivery ID; recipients MUST deduplicate before processing side effects.
        await db.execute(
            update(WebhookDelivery)
            .where(WebhookDelivery.status == "sending", WebhookDelivery.next_attempt_at <= now)
            .values(status="queued", lease_id=None)
        )
        rows = (
            await db.execute(
                select(WebhookDelivery.tenant_id, WebhookDelivery.id)
                .where(
                    WebhookDelivery.status == "queued",
                    or_(
                        WebhookDelivery.next_attempt_at.is_(None),
                        WebhookDelivery.next_attempt_at <= now,
                    ),
                )
                .order_by(WebhookDelivery.created_at)
                .limit(100)
            )
        ).all()
        await db.commit()
    for tenant_id, delivery_id in rows:
        await send_webhook.kiq(str(tenant_id), str(delivery_id))


async def recovery_loop() -> None:
    while True:
        try:
            await dispatch_pending()
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.warning("integration_dispatch_unavailable; durable deliveries retained")
        await asyncio.sleep(3)
