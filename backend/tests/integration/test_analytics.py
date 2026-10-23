"""Analytics preserve tenant scope, local dates, real denominators and transactional history."""

import asyncio
from datetime import UTC, datetime

import pytest
from sqlalchemy import select

from src.core.security import encrypt_pii
from src.db.enums import ApplicationStatus, LeadStatus, PaymentStatus
from src.db.models import Application, AuditLog, Course, Lead, PaymentOrder
from tests.integration.test_knowledge_workspace import signin
from tests.integration.test_knowledge_workspace import workspace as workspace

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def analytics_data(workspace):
    async def seed():
        tenant, second = workspace["tenants"]
        async with workspace["sessions"]() as db:
            course = Course(
                tenant_id=tenant, name="Synthetic analytics course", application_fee=10000
            )
            db.add(course)
            leads = [
                Lead(tenant_id=tenant, status=status, created_at=created)
                for status, created in [
                    (LeadStatus.NEW, datetime(2026, 10, 23, 18, 29, 59, tzinfo=UTC)),
                    (LeadStatus.DISCOVERING, datetime(2026, 10, 23, 18, 30, tzinfo=UTC)),
                    (LeadStatus.DISCOVERING, datetime(2026, 10, 24, 12, tzinfo=UTC)),
                    (LeadStatus.UNDER_REVIEW, datetime(2026, 10, 24, 18, 29, 59, tzinfo=UTC)),
                    (LeadStatus.NEW, datetime(2026, 10, 24, 18, 30, tzinfo=UTC)),
                ]
            ]
            db.add_all(leads)
            db.add(Lead(tenant_id=second, created_at=datetime(2026, 10, 24, 12, tzinfo=UTC)))
            await db.flush()
            applications = [
                Application(
                    tenant_id=tenant,
                    lead_id=lead.id,
                    course_id=course.id,
                    full_name_enc=encrypt_pii("Synthetic applicant"),
                    status=status,
                )
                for lead, status in [
                    (leads[2], ApplicationStatus.SUBMITTED),
                    (leads[3], ApplicationStatus.APPROVED),
                ]
            ]
            db.add_all(applications)
            await db.flush()
            db.add_all(
                [
                    PaymentOrder(
                        tenant_id=tenant,
                        lead_id=application.lead_id,
                        application_id=application.id,
                        course_id=course.id,
                        amount=0 if index == 0 else 10000,
                        status=PaymentStatus.WAIVED if index == 0 else PaymentStatus.PAID,
                    )
                    for index, application in enumerate(applications)
                ]
            )
            await db.commit()
            leads[2].status = LeadStatus.ADMISSION_READY
            await db.flush()
            leads[2].status = LeadStatus.QUALIFYING
            leads[3].status = LeadStatus.ENROLLED
            await db.commit()
            return [lead.id for lead in leads]

    return asyncio.run(seed())


def test_local_cohort_counts_conversions_and_observed_stages(workspace, analytics_data):
    client = workspace["client"]
    assert client.get("/api/staff/analytics").status_code == 401
    signin(client)
    result = client.get("/api/staff/analytics?from=2026-10-24&to=2026-10-24").json()
    assert result["totals"] == {
        "inquiries": 3,
        "applicants": 2,
        "fee_paid": 1,
        "fee_waived": 1,
        "fee_satisfied": 2,
        "enrolled_applicants": 1,
    }
    assert result["conversions"]["application"] == {"converted": 2, "of": 3, "percent": 66.67}
    assert result["conversions"]["enrollment"] == {"converted": 1, "of": 2, "percent": 50.0}
    assert result["series"] == [{"period": "2026-10-24", "count": 3}]
    stages = {row["state"]: row for row in result["stages"]}
    assert stages["admission_ready"]["current"] == 0 and stages["admission_ready"]["reached"] == 1
    assert stages["discovering"]["current"] == 1 and stages["discovering"]["reached"] == 2
    assert stages["new"]["reached"] == 3 and stages["new"]["current"] == 0
    assert "Synthetic applicant" not in str(result)
    assert "Earlier transitions are not inferred" in result["coverage"]


def test_zero_filled_weekly_buckets_and_empty_rates(workspace, analytics_data):
    client = workspace["client"]
    signin(client, email="agent@example.test")
    result = client.get("/api/staff/analytics?from=2026-10-21&to=2026-10-29&bucket=week").json()
    assert result["series"] == [
        {"period": "2026-10-19", "count": 5},
        {"period": "2026-10-26", "count": 0},
    ]
    result = client.get("/api/staff/analytics?from=2026-09-01&to=2026-09-02").json()
    assert result["totals"]["inquiries"] == 0
    assert result["conversions"]["application"]["percent"] is None
    assert result["series"] == [
        {"period": "2026-09-01", "count": 0},
        {"period": "2026-09-02", "count": 0},
    ]


def test_tenant_is_derived_from_session_and_period_is_bounded(workspace, analytics_data):
    client = workspace["client"]
    signin(client, "second")
    result = client.get(
        f"/api/staff/analytics?from=2026-10-24&to=2026-10-24&tenant_id={workspace['tenants'][0]}"
    ).json()
    assert result["totals"]["inquiries"] == 1 and result["totals"]["applicants"] == 0
    for query in ("from=2026-10-25&to=2026-10-24", "from=2020-01-01&to=2026-10-24", "bucket=month"):
        assert client.get("/api/staff/analytics?" + query).status_code == 422


def test_stage_audit_is_atomic_and_noop_updates_do_not_create_history(workspace):
    async def exercise():
        async with workspace["sessions"]() as db:
            lead = Lead(
                tenant_id=workspace["tenants"][0],
                status=LeadStatus.DISCOVERING,
                created_at=datetime(2020, 1, 1, tzinfo=UTC),
            )
            db.add(lead)
            await db.commit()
            lead.status = LeadStatus.QUALIFYING
            await db.commit()
            lead_id = lead.id
            lead.status = LeadStatus.QUALIFYING
            await db.commit()
            lead.status = LeadStatus.ADMISSION_READY
            await db.flush()
            await db.rollback()
        async with workspace["sessions"]() as db:
            logs = (
                await db.scalars(
                    select(AuditLog).where(
                        AuditLog.lead_id == lead_id, AuditLog.action == "lead.stage_changed"
                    )
                )
            ).all()
            assert len(logs) == 1 and logs[0].details == {"from": "discovering", "to": "qualifying"}
            assert logs[0].tenant_id == workspace["tenants"][0]
            assert (await db.get(Lead, lead_id)).status == LeadStatus.QUALIFYING

    asyncio.run(exercise())


def test_all_aggregates_share_a_snapshot_during_concurrent_arrivals(
    workspace, analytics_data, monkeypatch
):
    from src.staff import analytics as module

    original = module.count
    injected = False

    async def interleave(db, query):
        nonlocal injected
        if not injected:
            injected = True
            async with workspace["sessions"]() as other:
                tenant = workspace["tenants"][0]
                course_id = await other.scalar(select(Course.id).where(Course.tenant_id == tenant))
                lead = Lead(
                    tenant_id=tenant,
                    status=LeadStatus.PAYMENT_PENDING,
                    created_at=datetime(2026, 10, 24, 14, tzinfo=UTC),
                )
                other.add(lead)
                await other.flush()
                other.add(
                    Application(
                        tenant_id=tenant,
                        lead_id=lead.id,
                        course_id=course_id,
                        full_name_enc=encrypt_pii("Synthetic concurrent applicant"),
                    )
                )
                await other.commit()
        return await original(db, query)

    monkeypatch.setattr(module, "count", interleave)
    client = workspace["client"]
    signin(client)
    first = client.get("/api/staff/analytics?from=2026-10-24&to=2026-10-24").json()
    assert first["totals"]["inquiries"] == 3 and first["totals"]["applicants"] == 2
    assert sum(point["count"] for point in first["series"]) == 3
    second = client.get("/api/staff/analytics?from=2026-10-24&to=2026-10-24").json()
    assert second["totals"]["inquiries"] == 4 and second["totals"]["applicants"] == 3
    assert second["conversions"]["application"]["percent"] == 75.0
