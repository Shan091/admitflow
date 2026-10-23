"""Administrator-only destination management and bounded delivery monitoring."""

import secrets
import uuid
from typing import Any
from urllib.parse import urlunsplit

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import func, select, update

from src.core.security import encrypt_pii
from src.db.audit import write_audit_log
from src.db.models import Institution, WebhookDelivery, WebhookEndpoint
from src.integrations.transport import destination, resolve_public
from src.staff.auth import Db, Staff, require_admin, require_browser_write

router = APIRouter(prefix="/api/staff/integrations", tags=["institution integrations"])


class EndpointInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    url: str | None = Field(default=None, min_length=1, max_length=2048, repr=False)
    enabled: bool
    rotate_secret: bool = False


@router.get("")
async def configuration(staff: Staff, db: Db, response: Response) -> dict[str, Any]:
    require_admin(staff)
    response.headers["Cache-Control"] = "no-store"
    endpoint = await db.scalar(
        select(WebhookEndpoint).where(WebhookEndpoint.tenant_id == staff.tenant_id)
    )
    deliveries = (
        await db.scalars(
            select(WebhookDelivery)
            .where(WebhookDelivery.tenant_id == staff.tenant_id)
            .order_by(WebhookDelivery.created_at.desc(), WebhookDelivery.id)
            .limit(50)
        )
    ).all()
    counts = dict(
        (
            await db.execute(
                select(WebhookDelivery.status, func.count())
                .where(WebhookDelivery.tenant_id == staff.tenant_id)
                .group_by(WebhookDelivery.status)
            )
        ).all()
    )
    return {
        "configured": endpoint is not None,
        "enabled": bool(endpoint and endpoint.enabled),
        "host": endpoint.display_host if endpoint else None,
        "counts": counts,
        "deliveries": [
            {
                "id": str(row.id),
                "event_id": str(row.event_id),
                "status": row.status,
                "attempts": row.attempts,
                "error_code": row.error_code,
                "created_at": row.created_at.isoformat(),
            }
            for row in deliveries
        ],
    }


@router.put("", dependencies=[Depends(require_browser_write)])
async def configure(
    payload: EndpointInput, staff: Staff, db: Db, response: Response
) -> dict[str, Any]:
    require_admin(staff)
    response.headers["Cache-Control"] = "no-store"
    await db.scalar(
        select(Institution.id).where(Institution.id == staff.tenant_id).with_for_update()
    )
    endpoint = await db.scalar(
        select(WebhookEndpoint)
        .where(WebhookEndpoint.tenant_id == staff.tenant_id)
        .with_for_update()
    )
    target = None
    if payload.url:
        try:
            target = destination(payload.url)
            await resolve_public(target.hostname or "")
        except Exception:
            raise HTTPException(
                422, "Use a reachable public HTTPS destination on port 443."
            ) from None
    if endpoint is None and target is None:
        raise HTTPException(422, "Set the destination before enabling a webhook.")
    created = endpoint is None
    secret = secrets.token_urlsafe(32) if created or payload.rotate_secret else None
    if endpoint is None:
        assert target is not None and secret is not None
        endpoint = WebhookEndpoint(
            tenant_id=staff.tenant_id,
            url_enc=encrypt_pii(urlunsplit(target)),
            secret_enc=encrypt_pii(secret),
            display_host=target.hostname,
            enabled=payload.enabled,
        )
        db.add(endpoint)
    else:
        if target:
            endpoint.url_enc, endpoint.display_host = (
                encrypt_pii(urlunsplit(target)),
                target.hostname or "",
            )
        if secret:
            endpoint.secret_enc = encrypt_pii(secret)
        endpoint.enabled = payload.enabled
        # Any saved configuration invalidates older executable work. No backlog
        # replay to a new destination, including disable/re-enable operations.
        endpoint.generation = uuid.uuid4()
        await db.execute(
            update(WebhookDelivery)
            .where(
                WebhookDelivery.tenant_id == staff.tenant_id,
                WebhookDelivery.endpoint_id == endpoint.id,
                WebhookDelivery.status.in_(["queued", "sending"]),
            )
            .values(
                status="cancelled",
                error_code="configuration_changed",
                lease_id=None,
                next_attempt_at=None,
            )
        )
    await write_audit_log(
        db,
        tenant_id=staff.tenant_id,
        actor=str(staff.id),
        action="institution.webhook_configured",
        details={"enabled": payload.enabled, "secret_rotated": secret is not None},
    )
    await db.commit()
    return {"status": "saved", "signing_secret": secret}
