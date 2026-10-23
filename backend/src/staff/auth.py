"""Opaque database-backed staff sessions; no client-provided tenant authority."""

import asyncio
import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, Field
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import get_settings
from src.db.audit import write_audit_log
from src.db.enums import StaffRole
from src.db.models import Institution, StaffSession, StaffUser
from src.db.session import get_session

router = APIRouter(prefix="/api/staff", tags=["staff"])
Db = Annotated[AsyncSession, Depends(get_session)]
COOKIE = "admitflow_staff"


def hash_password(password: str) -> str:
    if not 12 <= len(password) <= 1024:
        raise ValueError("Use a password between 12 and 1024 characters")
    salt = secrets.token_hex(16)
    digest = hashlib.scrypt(
        password.encode(), salt=salt.encode(), n=32768, r=8, p=1, maxmem=64 * 1024 * 1024
    ).hex()
    return f"scrypt${salt}${digest}"


def verify_password(password: str, stored: str) -> bool:
    if len(password) > 1024:
        return False
    try:
        algorithm, salt, expected = stored.split("$")
        if algorithm != "scrypt" or len(salt) != 32 or len(expected) != 128:
            return False
        actual = hashlib.scrypt(
            password.encode(), salt=salt.encode(), n=32768, r=8, p=1, maxmem=64 * 1024 * 1024
        ).hex()
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def token_hash(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def require_browser_write(request: Request) -> None:
    """Custom header + strict cookies prevent cross-origin simple-request CSRF."""
    if request.headers.get("x-admitflow-request") != "1":
        raise HTTPException(403, "Request verification failed. Reload and try again.")
    origin = request.headers.get("origin")
    if origin and origin not in get_settings().staff_allowed_origins:
        raise HTTPException(403, "Request origin is not allowed.")


async def require_staff(request: Request, db: Db) -> StaffUser:
    token = request.cookies.get(COOKIE, "")
    if not token or len(token) > 200:
        raise HTTPException(401, "Sign in to your institution workspace.")
    staff = await db.scalar(
        select(StaffUser)
        .join(
            StaffSession,
            (StaffSession.user_id == StaffUser.id)
            & (StaffSession.tenant_id == StaffUser.tenant_id),
        )
        .where(
            StaffSession.token_hash == token_hash(token),
            StaffSession.expires_at > datetime.now(UTC),
            StaffUser.is_active.is_(True),
        )
    )
    if staff is None:
        raise HTTPException(401, "Your session has expired. Sign in again.")
    return staff


Staff = Annotated[StaffUser, Depends(require_staff)]


def require_admin(staff: StaffUser) -> None:
    if staff.role != StaffRole.ADMIN:
        raise HTTPException(403, "Only institution administrators can change documents.")


class Login(BaseModel):
    institution: str = Field(min_length=1, max_length=64, pattern=r"^[a-z0-9-]+$")
    email: str = Field(min_length=3, max_length=320)
    password: str = Field(min_length=1, max_length=1024, repr=False)


@router.post("/login", dependencies=[Depends(require_browser_write)])
async def login(payload: Login, request: Request, response: Response, db: Db) -> dict[str, str]:
    from src.staff.throttle import check_login_limit

    await check_login_limit(request, payload.institution, payload.email)
    staff = await db.scalar(
        select(StaffUser)
        .join(Institution)
        .where(
            Institution.slug == payload.institution,
            StaffUser.email == payload.email.strip().lower(),
            StaffUser.is_active.is_(True),
        )
    )
    # Always run the expensive KDF to avoid a cheap user-existence timing signal.
    stored = staff.hashed_password if staff else "scrypt$" + "0" * 32 + "$" + "0" * 128
    valid = await asyncio.to_thread(verify_password, payload.password, stored)
    if not valid or staff is None:
        raise HTTPException(401, "Institution, email or password is incorrect.")
    token = secrets.token_urlsafe(32)
    db.add(
        StaffSession(
            tenant_id=staff.tenant_id,
            user_id=staff.id,
            token_hash=token_hash(token),
            expires_at=datetime.now(UTC) + timedelta(hours=get_settings().staff_session_hours),
        )
    )
    await write_audit_log(db, tenant_id=staff.tenant_id, action="staff.login", actor=str(staff.id))
    await db.commit()
    response.set_cookie(
        COOKIE,
        token,
        httponly=True,
        secure=get_settings().app_env == "prod",
        samesite="strict",
        max_age=get_settings().staff_session_hours * 3600,
        path="/",
    )
    response.headers["Cache-Control"] = "no-store"
    return {"status": "signed_in"}


@router.get("/me")
async def me(staff: Staff, db: Db, response: Response) -> dict[str, str]:
    institution = await db.get(Institution, staff.tenant_id)
    response.headers["Cache-Control"] = "no-store"
    return {
        "email": staff.email,
        "role": staff.role.value,
        "institution": institution.name if institution else "Institution",
    }


@router.post("/logout", dependencies=[Depends(require_browser_write)])
async def logout(request: Request, response: Response, db: Db) -> dict[str, str]:
    await db.execute(
        delete(StaffSession).where(
            StaffSession.token_hash == token_hash(request.cookies.get(COOKIE, ""))
        )
    )
    await db.commit()
    response.delete_cookie(COOKIE, path="/")
    return {"status": "signed_out"}
