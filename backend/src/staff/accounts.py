"""Institution-owned staff provisioning, role changes and forced password setup."""

import asyncio
import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import delete, func, select
from sqlalchemy.exc import IntegrityError

from src.db.audit import write_audit_log
from src.db.enums import StaffRole
from src.db.models import Institution, StaffSession, StaffUser
from src.staff.auth import Db, Staff, hash_password, require_admin, require_browser_write

router = APIRouter(prefix="/api/staff/users", tags=["institution staff"])


class CreateUser(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: str = Field(min_length=3, max_length=320, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    full_name: str | None = Field(default=None, max_length=255)
    role: StaffRole = StaffRole.AGENT
    password: str = Field(min_length=12, max_length=1024, repr=False)


class EditUser(BaseModel):
    model_config = ConfigDict(extra="forbid")
    role: StaffRole
    is_active: bool = Field(strict=True)


class ResetPassword(BaseModel):
    model_config = ConfigDict(extra="forbid")
    password: str = Field(min_length=12, max_length=1024, repr=False)


async def admin_scope(db: Db, staff: Staff) -> None:
    # Serialize tenant access mutations without blocking FK key-share checks from
    # a concurrent login/password change that already owns the staff row lock.
    await db.scalar(
        select(Institution.id)
        .where(Institution.id == staff.tenant_id)
        .with_for_update(key_share=True)
    )
    await db.refresh(staff, with_for_update=True)
    if not staff.is_active or staff.must_change_password:
        raise HTTPException(401, "Sign in again to manage institution access.")
    require_admin(staff)


async def target_user(db: Db, staff: Staff, user_id: uuid.UUID) -> StaffUser:
    user = await db.scalar(
        select(StaffUser)
        .where(StaffUser.tenant_id == staff.tenant_id, StaffUser.id == user_id)
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if user is None:
        raise HTTPException(404, "Staff account not found.")
    return user


@router.get("")
async def users(
    staff: Staff, db: Db, response: Response, offset: int = Query(default=0, ge=0, le=1_000_000)
) -> list[dict[str, Any]]:
    require_admin(staff)
    response.headers["Cache-Control"] = "no-store"
    rows = (
        await db.scalars(
            select(StaffUser)
            .where(StaffUser.tenant_id == staff.tenant_id)
            .order_by(StaffUser.email, StaffUser.id)
            .offset(offset)
            .limit(50)
        )
    ).all()
    result = [
        {
            "id": str(row.id),
            "email": row.email,
            "full_name": row.full_name,
            "role": row.role.value,
            "is_active": row.is_active,
            "must_change_password": row.must_change_password,
            "is_you": row.id == staff.id,
        }
        for row in rows
    ]
    await write_audit_log(
        db, tenant_id=staff.tenant_id, actor=str(staff.id), action="staff.users_viewed"
    )
    await db.commit()
    return result


@router.post("", dependencies=[Depends(require_browser_write)])
async def create_user(payload: CreateUser, staff: Staff, db: Db) -> dict[str, str]:
    require_admin(staff)
    password_hash = await asyncio.to_thread(hash_password, payload.password)
    await admin_scope(db, staff)
    user = StaffUser(
        tenant_id=staff.tenant_id,
        email=payload.email.lower(),
        full_name=payload.full_name or None,
        hashed_password=password_hash,
        role=payload.role,
        is_active=True,
        must_change_password=True,
    )
    db.add(user)
    try:
        await db.flush()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            409, "A staff account with that email already exists in this institution."
        ) from None
    await write_audit_log(
        db,
        tenant_id=staff.tenant_id,
        actor=str(staff.id),
        action="staff.created",
        details={"user_id": str(user.id), "role": user.role.value},
    )
    await db.commit()
    return {"id": str(user.id), "status": "created"}


@router.put("/{user_id}", dependencies=[Depends(require_browser_write)])
async def edit_user(user_id: uuid.UUID, payload: EditUser, staff: Staff, db: Db) -> dict[str, str]:
    await admin_scope(db, staff)
    user = await target_user(db, staff, user_id)
    removing_admin = (
        user.role == StaffRole.ADMIN
        and user.is_active
        and not user.must_change_password
        and (payload.role != StaffRole.ADMIN or not payload.is_active)
    )
    if removing_admin:
        remaining = await db.scalar(
            select(func.count())
            .select_from(StaffUser)
            .where(
                StaffUser.tenant_id == staff.tenant_id,
                StaffUser.role == StaffRole.ADMIN,
                StaffUser.is_active.is_(True),
                StaffUser.must_change_password.is_(False),
            )
        )
        if (remaining or 0) <= 1:
            raise HTTPException(
                409, "Keep at least one active administrator with a private password."
            )
    if (user.role, user.is_active) != (payload.role, payload.is_active):
        user.role, user.is_active = payload.role, payload.is_active
        await db.execute(
            delete(StaffSession).where(
                StaffSession.tenant_id == staff.tenant_id, StaffSession.user_id == user.id
            )
        )
        await write_audit_log(
            db,
            tenant_id=staff.tenant_id,
            actor=str(staff.id),
            action="staff.access_changed",
            details={
                "user_id": str(user.id),
                "role": payload.role.value,
                "active": payload.is_active,
            },
        )
    await db.commit()
    return {"status": "saved"}


@router.post("/{user_id}/reset-password", dependencies=[Depends(require_browser_write)])
async def reset_password(
    user_id: uuid.UUID, payload: ResetPassword, staff: Staff, db: Db
) -> dict[str, str]:
    require_admin(staff)
    if user_id == staff.id:
        raise HTTPException(409, "Use your account password form to change your own password.")
    password_hash = await asyncio.to_thread(hash_password, payload.password)
    await admin_scope(db, staff)
    user = await target_user(db, staff, user_id)
    user.hashed_password, user.must_change_password = password_hash, True
    await db.execute(
        delete(StaffSession).where(
            StaffSession.tenant_id == staff.tenant_id, StaffSession.user_id == user.id
        )
    )
    await write_audit_log(
        db,
        tenant_id=staff.tenant_id,
        actor=str(staff.id),
        action="staff.password_reset",
        details={"user_id": str(user.id)},
    )
    await db.commit()
    return {"status": "password_reset"}
