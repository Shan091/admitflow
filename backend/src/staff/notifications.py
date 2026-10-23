"""Authenticated live event snapshots with per-user durable read receipts."""

import asyncio
import uuid
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException, Response, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from sqlalchemy import exists, func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import get_settings
from src.db.audit import write_audit_log
from src.db.models import IntegrationEvent, NotificationReceipt, StaffUser
from src.staff.auth import COOKIE, Db, Staff, require_browser_write, session_user

router = APIRouter(prefix="/api/staff/notifications", tags=["staff notifications"])


class Acknowledge(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: Literal["acknowledge"] = "acknowledge"
    ids: list[uuid.UUID] = Field(max_length=50)


async def snapshot(db: AsyncSession, staff: StaffUser) -> dict[str, Any]:
    unread = ~exists(
        select(NotificationReceipt.event_id).where(
            NotificationReceipt.tenant_id == staff.tenant_id,
            NotificationReceipt.user_id == staff.id,
            NotificationReceipt.event_id == IntegrationEvent.id,
        )
    )
    predicate = (
        IntegrationEvent.tenant_id == staff.tenant_id
    ) & IntegrationEvent.notification.is_not(None)
    count = await db.scalar(
        select(func.count()).select_from(IntegrationEvent).where(predicate, unread)
    )
    rows = (
        await db.execute(
            select(IntegrationEvent, unread.label("unread"))
            .where(predicate)
            .order_by(unread.desc(), IntegrationEvent.created_at.desc(), IntegrationEvent.id)
            .limit(50)
        )
    ).all()
    return {
        "unread_count": count or 0,
        "items": [
            {
                "id": str(row.id),
                "kind": row.notification,
                "lead_id": str(row.lead_id) if row.lead_id else None,
                "created_at": row.created_at.isoformat(),
                "unread": is_unread,
            }
            for row, is_unread in rows
        ],
    }


async def acknowledge(db: AsyncSession, staff: StaffUser, payload: Acknowledge) -> None:
    ids = (
        await db.scalars(
            select(IntegrationEvent.id).where(
                IntegrationEvent.tenant_id == staff.tenant_id,
                IntegrationEvent.notification.is_not(None),
                IntegrationEvent.id.in_(payload.ids),
            )
        )
    ).all()
    if ids:
        await db.execute(
            insert(NotificationReceipt)
            .values(
                [
                    {"tenant_id": staff.tenant_id, "user_id": staff.id, "event_id": event_id}
                    for event_id in ids
                ]
            )
            .on_conflict_do_nothing(index_elements=["user_id", "event_id"])
        )
        await write_audit_log(
            db,
            tenant_id=staff.tenant_id,
            actor=str(staff.id),
            action="staff.notifications_read",
            details={"count": len(ids)},
        )
    await db.commit()


@router.get("")
async def current(staff: Staff, db: Db, response: Response) -> dict[str, Any]:
    response.headers["Cache-Control"] = "no-store"
    return await snapshot(db, staff)


@router.post("/read", dependencies=[Depends(require_browser_write)])
async def read(payload: Acknowledge, staff: Staff, db: Db) -> dict[str, str]:
    await acknowledge(db, staff, payload)
    return {"status": "read"}


@router.websocket("/ws")
async def live(websocket: WebSocket, db: Db) -> None:
    if websocket.headers.get("origin") not in get_settings().staff_allowed_origins:
        await websocket.close(code=4403)
        return
    token = websocket.cookies.get(COOKIE, "")
    try:
        staff = await session_user(db, token)
    except HTTPException:
        await websocket.close(code=4401)
        return
    await websocket.accept()
    await write_audit_log(
        db, tenant_id=staff.tenant_id, actor=str(staff.id), action="staff.notifications_connected"
    )
    await db.commit()
    try:
        while True:
            try:
                staff = await session_user(db, token)
            except HTTPException:
                await websocket.close(code=4401)
                return
            await websocket.send_json(await snapshot(db, staff))
            await db.rollback()  # Release the transaction/connection while idle.
            try:
                raw = await asyncio.wait_for(websocket.receive_text(), timeout=2)
            except TimeoutError:
                continue
            if len(raw) > 8000:
                await websocket.close(code=4400)
                return
            try:
                payload = Acknowledge.model_validate_json(raw)
            except ValidationError:
                await websocket.close(code=4400)
                return
            staff = await session_user(db, token)
            await acknowledge(db, staff, payload)
    except WebSocketDisconnect:
        return
    except HTTPException:
        await websocket.close(code=4401)
