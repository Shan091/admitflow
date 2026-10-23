"""Real database CRM lookup, index maintenance, export roles and isolation."""

import asyncio
import csv
import io

import pytest
from openpyxl import load_workbook
from sqlalchemy import select

from src.core.security import encrypt_pii, hash_phone
from src.db.enums import LeadStatus
from src.db.models import Application, AuditLog, Course, Lead, PaymentOrder
from src.scripts.reindex_names import reindex_batch
from src.staff import exports
from tests.integration.test_knowledge_workspace import signin
from tests.integration.test_knowledge_workspace import workspace as workspace

pytestmark = pytest.mark.integration
HEADERS = {"X-AdmitFlow-Request": "1"}


@pytest.fixture(scope="module")
def crm_data(workspace):
    workspace["settings"].phone_hash_key = "synthetic-crm-hash-key"

    async def seed():
        first, second = workspace["tenants"]
        async with workspace["sessions"]() as db:
            course = Course(tenant_id=first, name="Synthetic CRM course")
            db.add(course)
            await db.flush()
            leads = [
                Lead(
                    tenant_id=first,
                    name_enc=encrypt_pii("Asha നായർ"),
                    status=LeadStatus.ENROLLED,
                    current_course_id=course.id,
                    phone_enc=encrypt_pii("+919876543210"),
                    phone_hash=hash_phone("+919876543210"),
                ),
                Lead(tenant_id=first),
                Lead(tenant_id=second, name_enc=encrypt_pii("Asha നായർ")),
            ]
            db.add_all(leads)
            await db.flush()
            application = Application(
                tenant_id=first,
                lead_id=leads[1].id,
                course_id=course.id,
                full_name_enc=encrypt_pii(" \t=FORMULA"),
                form_data_enc=encrypt_pii('{"address":"Synthetic address"}'),
            )
            db.add(application)
            await db.flush()
            db.add(
                PaymentOrder(
                    tenant_id=first,
                    lead_id=leads[1].id,
                    application_id=application.id,
                    course_id=course.id,
                    amount=12345,
                )
            )
            await db.commit()
            return [lead.id for lead in leads], course.id

    return asyncio.run(seed())


def test_search_scope_validation_and_audit(workspace, crm_data):
    client = workspace["client"]
    assert client.post("/api/staff/leads/search", json={}).status_code == 403
    signin(client, email="agent@example.test")
    assert (
        client.post("/api/staff/leads/search", json={"query": "Asha"}, headers=HEADERS).status_code
        == 200
    )
    for query in ["AS നായ", "+91 (98765) 43210"]:
        response = client.post(
            "/api/staff/leads/search",
            json={"query": query, "status": "enrolled", "course_id": str(crm_data[1])},
            headers=HEADERS,
        )
        assert response.status_code == 200, response.text
        assert response.headers["cache-control"] == "no-store"
        assert [row["id"] for row in response.json()] == [str(crm_data[0][0])]
        assert response.json()[0]["name"] == "Asha നായർ"
        assert "phone" not in response.json()[0]
    for payload in [
        {"query": "a"},
        {"query": "Asha", "tenant_id": str(workspace["tenants"][1])},
        {"query": "a" * 201},
        {"status": "invalid"},
    ]:
        assert (
            client.post("/api/staff/leads/search", json=payload, headers=HEADERS).status_code == 422
        )
    assert (
        client.post(
            "/api/staff/leads/search", json={"query": "Asha", "status": "new"}, headers=HEADERS
        ).json()
        == []
    )
    signin(client, "second")
    rows = client.post("/api/staff/leads/search", json={"query": "Asha"}, headers=HEADERS).json()
    assert [row["id"] for row in rows] == [str(crm_data[0][2])]

    async def audit():
        async with workspace["sessions"]() as db:
            details = (
                await db.scalars(
                    select(AuditLog.details).where(AuditLog.action == "staff.leads_searched")
                )
            ).all()
            assert details and all(set(item) == {"result_count"} for item in details)

    asyncio.run(audit())


def test_index_rename_clear_and_legacy_backfill(workspace, crm_data):
    async def exercise():
        async with workspace["sessions"]() as db:
            lead = await db.get(Lead, crm_data[0][0])
            old = list(lead.name_search_tokens)
            lead.name_enc = encrypt_pii("New Person")
            await db.commit()
            assert lead.name_search_tokens != old
            lead.name_enc = None
            await db.commit()
            assert lead.name_search_tokens == []
            await reindex_batch(db)
            legacy = await db.get(Lead, crm_data[0][1])
            await db.refresh(legacy)
            assert legacy.name_enc and legacy.name_search_tokens
            tokens = list(legacy.name_search_tokens)
            await reindex_batch(db)
            await db.refresh(legacy)
            assert legacy.name_search_tokens == tokens

    asyncio.run(exercise())


def test_downloads_roles_datasets_limits_and_tenants(workspace, crm_data, monkeypatch):
    client = workspace["client"]
    monkeypatch.setattr(exports, "get_settings", lambda: workspace["settings"])
    signin(client, email="agent@example.test")
    assert (
        client.post(
            "/api/staff/exports", json={"dataset": "leads", "format": "csv"}, headers=HEADERS
        ).status_code
        == 403
    )
    signin(client)
    filtered = client.post(
        "/api/staff/exports",
        json={"dataset": "leads", "format": "csv", "query": "FORM"},
        headers=HEADERS,
    )
    assert filtered.status_code == 200
    assert len(list(csv.reader(io.StringIO(filtered.content.decode("utf-8-sig"))))) == 2
    assert (
        client.post("/api/staff/exports", json={"dataset": "leads", "format": "csv"}).status_code
        == 403
    )
    for dataset in ("leads", "applications", "payments"):
        for format in ("csv", "xlsx"):
            response = client.post(
                "/api/staff/exports", json={"dataset": dataset, "format": format}, headers=HEADERS
            )
            assert response.status_code == 200, response.text
            assert response.headers["cache-control"] == "no-store"
            if format == "csv":
                rows = list(csv.reader(io.StringIO(response.content.decode("utf-8-sig"))))
            else:
                rows = list(load_workbook(io.BytesIO(response.content)).active.values)
            assert len(rows) == (3 if dataset == "leads" else 2)
            assert str(crm_data[0][2]) not in str(rows)
            assert all(not field.endswith(("_enc", "_tokens", "_hash")) for field in rows[0])
            if dataset == "applications":
                assert rows[1][2] == ("' \t=FORMULA" if format == "csv" else " \t=FORMULA")
            if dataset == "payments":
                assert rows[1][4] == "12345"
    workspace["settings"].staff_export_max_rows = 1
    assert (
        client.post(
            "/api/staff/exports", json={"dataset": "leads", "format": "csv"}, headers=HEADERS
        ).status_code
        == 422
    )
    workspace["settings"].staff_export_max_rows = 10000
    signin(client, "second")
    response = client.post(
        "/api/staff/exports", json={"dataset": "applications", "format": "csv"}, headers=HEADERS
    )
    assert len(list(csv.reader(io.StringIO(response.content.decode("utf-8-sig"))))) == 1


def test_search_pages_are_bounded_and_do_not_drop_or_repeat_records(workspace, crm_data):
    async def seed():
        async with workspace["sessions"]() as db:
            leads = [
                Lead(
                    tenant_id=workspace["tenants"][0], name_enc=encrypt_pii("Pagination synthetic")
                )
                for _ in range(55)
            ]
            db.add_all(leads)
            await db.commit()
            return {str(lead.id) for lead in leads}

    expected = asyncio.run(seed())
    signin(workspace["client"])
    pages = [
        workspace["client"]
        .post(
            "/api/staff/leads/search",
            json={"query": "Pagination", "offset": offset},
            headers=HEADERS,
        )
        .json()
        for offset in (0, 50, 100)
    ]
    assert [len(page) for page in pages] == [50, 5, 0]
    found = [row["id"] for page in pages for row in page]
    assert len(found) == len(set(found)) and set(found) == expected
