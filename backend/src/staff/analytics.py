"""Tenant-scoped creation cohorts with explicit, observed conversion evidence."""

from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from typing import Annotated, Any, Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import Date, Select, and_, exists, func, or_, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.audit import write_audit_log
from src.db.enums import ApplicationStatus, LeadStatus, PaymentStatus
from src.db.models import Application, AuditLog, Institution, Lead, PaymentOrder
from src.staff.auth import Db, Staff

router = APIRouter(prefix="/api/staff", tags=["institution analytics"])
Bucket = Literal["day", "week"]


@dataclass(frozen=True)
class Period:
    start: date
    end: date
    timezone: str
    start_at: datetime
    end_at: datetime


def period_window(timezone: str, start: date | None = None, end: date | None = None) -> Period:
    try:
        zone = ZoneInfo(timezone)
    except (ValueError, ZoneInfoNotFoundError):
        raise ValueError(
            "Configure a valid institution timezone before loading analytics."
        ) from None
    end = end or datetime.now(UTC).astimezone(zone).date()
    start = start or end - timedelta(days=29)
    if end < start or (end - start).days >= 366:
        raise ValueError("Choose an ordered period of at most 366 days.")
    try:
        return Period(
            start,
            end,
            timezone,
            datetime.combine(start, time.min, zone).astimezone(UTC),
            datetime.combine(end + timedelta(days=1), time.min, zone).astimezone(UTC),
        )
    except OverflowError:
        raise ValueError("Choose a period within supported calendar dates.") from None


def bucket_dates(start: date, end: date, bucket: Bucket) -> list[date]:
    value = start - timedelta(days=start.weekday()) if bucket == "week" else start
    step = timedelta(days=7 if bucket == "week" else 1)
    values = []
    while value <= end:
        values.append(value)
        if end - value < step:
            break
        value += step
    return values


def percent(converted: int, denominator: int) -> float | None:
    if not 0 <= converted <= denominator:
        raise ValueError("A conversion must be a subset of its denominator.")
    return round(converted * 100 / denominator, 2) if denominator else None


async def count(db: AsyncSession, query: Select[Any]) -> int:
    return int(await db.scalar(select(func.count()).select_from(query.subquery())) or 0)


@router.get("/analytics")
async def analytics(
    staff: Staff,
    db: Db,
    start: Annotated[date | None, Query(alias="from")] = None,
    end: Annotated[date | None, Query(alias="to")] = None,
    bucket: Bucket = "day",
) -> dict[str, Any]:
    # Release auth's read transaction, then read every aggregate from one snapshot.
    # Concurrent arrivals cannot make a numerator exceed an earlier denominator.
    await db.commit()
    await db.execute(text("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"))
    institution = await db.scalar(
        select(Institution)
        .where(Institution.id == staff.tenant_id)
        .execution_options(populate_existing=True)
    )
    if institution is None:
        raise HTTPException(404, "Institution not found.")
    try:
        period = period_window(institution.timezone, start, end)
    except ValueError as error:
        raise HTTPException(422, str(error)) from None
    cohort = and_(
        Lead.tenant_id == staff.tenant_id,
        Lead.created_at >= period.start_at,
        Lead.created_at < period.end_at,
    )
    current = {
        status.value: int(total)
        for status, total in (
            await db.execute(select(Lead.status, func.count()).where(cohort).group_by(Lead.status))
        ).all()
    }
    total = sum(current.values())
    expressions = []
    for stage in LeadStatus:
        observed = exists(
            select(AuditLog.id).where(
                AuditLog.tenant_id == staff.tenant_id,
                AuditLog.lead_id == Lead.id,
                AuditLog.action == "lead.stage_changed",
                or_(
                    AuditLog.details["to"].astext == stage.value,
                    AuditLog.details["from"].astext == stage.value,
                ),
            )
        ).correlate(Lead)
        expressions.append(
            func.count().filter(or_(Lead.status == stage, observed)).label(stage.value)
        )
    reached = (
        (await db.execute(select(*expressions).select_from(Lead).where(cohort))).one()._mapping
    )
    stages = []
    for stage in LeadStatus:
        observed_count = total if stage == LeadStatus.NEW else int(reached[stage.value])
        stages.append(
            {
                "state": stage.value,
                "current": current.get(stage.value, 0),
                "reached": observed_count,
                "percent": percent(observed_count, total),
            }
        )
    lead_ids = select(Lead.id).where(cohort).correlate(None)
    applied = (
        select(Application.lead_id)
        .where(Application.tenant_id == staff.tenant_id, Application.lead_id.in_(lead_ids))
        .distinct()
    )
    applications = await count(db, applied)
    fee = applied.join(
        PaymentOrder,
        (PaymentOrder.application_id == Application.id)
        & (PaymentOrder.tenant_id == Application.tenant_id),
    )
    paid = await count(db, fee.where(PaymentOrder.status == PaymentStatus.PAID))
    waived = await count(db, fee.where(PaymentOrder.status == PaymentStatus.WAIVED))
    satisfied = await count(
        db, fee.where(PaymentOrder.status.in_([PaymentStatus.PAID, PaymentStatus.WAIVED]))
    )
    enrolled = await count(
        db,
        applied.join(
            Lead, (Lead.id == Application.lead_id) & (Lead.tenant_id == Application.tenant_id)
        ).where(
            or_(
                Application.status == ApplicationStatus.APPROVED, Lead.status == LeadStatus.ENROLLED
            )
        ),
    )
    day_bucket = func.date_trunc(bucket, func.timezone(period.timezone, Lead.created_at)).cast(Date)
    grouped = (
        await db.execute(
            select(
                day_bucket,
                func.count(),
            )
            .where(cohort)
            .group_by(day_bucket)
            .order_by(day_bucket)
        )
    ).all()
    counts = {day: int(value) for day, value in grouped}
    result = {
        "period": {
            "from": period.start.isoformat(),
            "to": period.end.isoformat(),
            "bucket": bucket,
            "timezone": period.timezone,
        },
        "as_of": datetime.now(UTC).isoformat(),
        "totals": {
            "inquiries": total,
            "applicants": applications,
            "fee_paid": paid,
            "fee_waived": waived,
            "fee_satisfied": satisfied,
            "enrolled_applicants": enrolled,
        },
        "conversions": {
            "application": {
                "converted": applications,
                "of": total,
                "percent": percent(applications, total),
            },
            "fee_satisfied": {
                "converted": satisfied,
                "of": applications,
                "percent": percent(satisfied, applications),
            },
            "enrollment": {
                "converted": enrolled,
                "of": applications,
                "percent": percent(enrolled, applications),
            },
        },
        "stages": stages,
        "series": [
            {"period": day.isoformat(), "count": counts.get(day, 0)}
            for day in bucket_dates(period.start, period.end, bucket)
        ],
        "coverage": "Inquiries created in the selected period; progress as of now. "
        "Stage reach includes recorded transitions and current states. "
        "Earlier transitions are not inferred; stages may be skipped.",
    }
    await write_audit_log(
        db,
        tenant_id=staff.tenant_id,
        actor=str(staff.id),
        action="staff.analytics_viewed",
        details={"from": period.start.isoformat(), "to": period.end.isoformat(), "bucket": bucket},
    )
    await db.commit()
    return result
