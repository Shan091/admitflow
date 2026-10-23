"""Tenant administrators manage access; shared initial passwords cannot expose PII."""

import asyncio
import uuid

import pytest
from fastapi import HTTPException
from sqlalchemy import delete, select

from src.db.enums import StaffRole
from src.db.models import StaffUser
from src.staff.accounts import EditUser, edit_user
from tests.integration.test_knowledge_workspace import signin
from tests.integration.test_knowledge_workspace import workspace as workspace

pytestmark = pytest.mark.integration
HEADERS = {"X-AdmitFlow-Request": "1"}
TEMP = "synthetic-initial-password"
PRIVATE = "synthetic-private-password"


def test_creation_first_login_password_change_and_session_rotation(workspace):
    client = workspace["client"]
    signin(client)
    created = client.post(
        "/api/staff/users",
        json={"email": "new@example.test", "role": "agent", "password": TEMP},
        headers=HEADERS,
    )
    assert created.status_code == 200, created.text
    user_id = created.json()["id"]
    rows = client.get("/api/staff/users").json()
    assert "hashed_password" not in str(rows) and TEMP not in str(rows)
    assert any(row["id"] == user_id and row["must_change_password"] for row in rows)
    client.cookies.clear()
    assert (
        client.post(
            "/api/staff/login",
            json={"institution": "first", "email": "new@example.test", "password": TEMP},
            headers=HEADERS,
        ).status_code
        == 200
    )
    assert client.get("/api/staff/me").json()["must_change_password"] is True
    assert client.get("/api/staff/leads").status_code == 403
    old_cookie = client.cookies.get("admitflow_staff")
    assert (
        client.post(
            "/api/staff/password",
            json={"current_password": "incorrect", "new_password": PRIVATE},
            headers=HEADERS,
        ).status_code
        == 422
    )
    changed = client.post(
        "/api/staff/password",
        json={"current_password": TEMP, "new_password": PRIVATE},
        headers=HEADERS,
    )
    assert changed.status_code == 200, changed.text
    new_cookie = client.cookies.get("admitflow_staff")
    assert new_cookie != old_cookie and client.get("/api/staff/leads").status_code == 200
    client.cookies.set("admitflow_staff", old_cookie)
    assert client.get("/api/staff/me").status_code == 401
    client.cookies.clear()
    client.cookies.set("admitflow_staff", new_cookie)
    assert client.get("/api/staff/me").json()["must_change_password"] is False


def test_admin_roles_tenant_scope_last_admin_and_reset(workspace):
    client = workspace["client"]
    signin(client, email="agent@example.test")
    assert client.get("/api/staff/users").status_code == 403
    assert (
        client.post(
            "/api/staff/users",
            json={"email": "forbidden@example.test", "role": "admin", "password": TEMP},
            headers=HEADERS,
        ).status_code
        == 403
    )
    signin(client)
    rows = client.get("/api/staff/users").json()
    admin = next(row for row in rows if row["email"] == "admin@example.test")
    target = next(row for row in rows if row["email"] == "new@example.test")
    assert (
        client.put(
            f"/api/staff/users/{admin['id']}",
            json={"role": "agent", "is_active": True},
            headers=HEADERS,
        ).status_code
        == 409
    )
    assert (
        client.put(
            f"/api/staff/users/{uuid.uuid4()}",
            json={"role": "agent", "is_active": False},
            headers=HEADERS,
        ).status_code
        == 404
    )
    assert (
        client.put(
            f"/api/staff/users/{target['id']}",
            json={"role": "agent", "is_active": False},
            headers=HEADERS,
        ).status_code
        == 200
    )
    assert (
        client.post(
            f"/api/staff/users/{target['id']}/reset-password",
            json={"password": TEMP},
            headers=HEADERS,
        ).status_code
        == 200
    )

    async def inspect():
        async with workspace["sessions"]() as db:
            user = await db.get(StaffUser, uuid.UUID(target["id"]))
            assert user.must_change_password and not user.is_active

    asyncio.run(inspect())


def test_concurrent_admin_demotions_preserve_one_capable_administrator(workspace):
    async def exercise():
        tenant = workspace["tenants"][0]
        async with workspace["sessions"]() as db:
            original = await db.scalar(
                select(StaffUser).where(
                    StaffUser.tenant_id == tenant, StaffUser.email == "admin@example.test"
                )
            )
            original_id = original.id
            created = [
                StaffUser(
                    tenant_id=tenant,
                    email=f"race-{uuid.uuid4().hex}@example.test",
                    role=StaffRole.ADMIN,
                    hashed_password=original.hashed_password,
                    is_active=True,
                    must_change_password=False,
                )
                for _ in range(2)
            ]
            db.add_all(created)
            original.role = StaffRole.AGENT
            await db.commit()
            ids = [row.id for row in created]

        async def demote(user_id):
            async with workspace["sessions"]() as db:
                staff = await db.get(StaffUser, user_id)
                return await edit_user(
                    user_id, EditUser(role=StaffRole.AGENT, is_active=True), staff, db
                )

        try:
            results = await asyncio.wait_for(
                asyncio.gather(*(demote(user_id) for user_id in ids), return_exceptions=True), 5
            )
            assert sum(isinstance(result, dict) for result in results) == 1
            assert (
                sum(
                    isinstance(result, HTTPException) and result.status_code == 409
                    for result in results
                )
                == 1
            )
        finally:
            async with workspace["sessions"]() as db:
                original = await db.get(StaffUser, original_id)
                original.role = StaffRole.ADMIN
                await db.execute(delete(StaffUser).where(StaffUser.id.in_(ids)))
                await db.commit()

    asyncio.run(exercise())
