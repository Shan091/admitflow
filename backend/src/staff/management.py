"""Tenant-scoped administrator catalog and institution configuration."""

import math
import uuid
from datetime import datetime, time
from typing import Any, Literal, Self
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field, model_validator
from sqlalchemy import delete, func, select, update
from sqlalchemy.exc import IntegrityError

from src.core.demo_admissions import demo_fee
from src.db.audit import write_audit_log
from src.db.enums import DiscountType, RuleOperator
from src.db.models import (
    Batch,
    ConversationReply,
    Course,
    DiscountCode,
    Institution,
    OutboundMessage,
    QualificationRule,
)
from src.staff.auth import Db, Staff, require_admin, require_browser_write

router = APIRouter(prefix="/api/staff", tags=["institution management"])


class BatchInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    id: uuid.UUID | None = None
    name: str = Field(min_length=1, max_length=255)
    capacity: int = Field(ge=1, le=1000000, strict=True)
    seats_remaining: int = Field(ge=0, strict=True)
    is_active: bool = True

    @model_validator(mode="after")
    def valid_capacity(self) -> Self:
        if self.seats_remaining > self.capacity:
            raise ValueError("Available seats cannot exceed capacity")
        return self


class RuleInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    field: str = Field(pattern=r"^[a-z][a-z0-9_]{0,63}$")
    operator: RuleOperator
    value: Any

    @model_validator(mode="after")
    def valid_value(self) -> Self:
        def scalar(value: Any) -> bool:
            return (
                isinstance(value, (str, bool, int, float))
                and not (isinstance(value, float) and not math.isfinite(value))
                and len(str(value)) <= 1000
            )

        if self.operator in {RuleOperator.IN, RuleOperator.NOT_IN}:
            if not isinstance(self.value, list) or not 1 <= len(self.value) <= 50:
                raise ValueError("Membership rules need a nonempty list of at most 50 values")
            if not all(scalar(value) for value in self.value):
                raise ValueError("Rule values must be text, numbers or booleans")
        elif self.operator in {
            RuleOperator.GT,
            RuleOperator.GTE,
            RuleOperator.LT,
            RuleOperator.LTE,
        }:
            if type(self.value) not in {int, float} or not scalar(self.value):
                raise ValueError("Comparison rules require a finite number")
        elif not scalar(self.value):
            raise ValueError("Rule value must be text, a number or a boolean")
        return self


class CourseInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=255)
    description: str = Field(default="", max_length=10000)
    application_fee: int = Field(ge=0, le=1000000000, strict=True)
    is_active: bool = True
    batches: list[BatchInput] = Field(default_factory=list, max_length=100)
    rules: list[RuleInput] = Field(default_factory=list, max_length=100)

    @model_validator(mode="after")
    def unique_batches(self) -> Self:
        ids = [batch.id for batch in self.batches if batch.id is not None]
        if len(ids) != len(set(ids)):
            raise ValueError("A batch may appear only once")
        return self


async def owned_course(db: Db, staff: Staff, course_id: uuid.UUID) -> Course:
    course = await db.scalar(
        select(Course)
        .where(Course.id == course_id, Course.tenant_id == staff.tenant_id)
        .with_for_update()
    )
    if course is None:
        raise HTTPException(404, "Course not found.")
    return course


async def course_view(db: Db, course: Course) -> dict[str, Any]:
    batches = list(
        (
            await db.scalars(
                select(Batch)
                .where(Batch.tenant_id == course.tenant_id, Batch.course_id == course.id)
                .order_by(Batch.name, Batch.id)
            )
        ).all()
    )
    rules = list(
        (
            await db.scalars(
                select(QualificationRule)
                .where(
                    QualificationRule.tenant_id == course.tenant_id,
                    QualificationRule.course_id == course.id,
                )
                .order_by(QualificationRule.field, QualificationRule.id)
            )
        ).all()
    )
    return {
        "id": str(course.id),
        "name": course.name,
        "description": course.description or "",
        "application_fee": course.application_fee,
        "is_active": course.is_active,
        "is_reference": course.is_reference,
        "reference_url": course.reference_url,
        "demo_application_fee": await demo_fee(db, course),
        "batches": [
            {
                "id": str(batch.id),
                "name": batch.name,
                "capacity": batch.capacity,
                "seats_remaining": batch.seats_remaining,
                "is_active": batch.is_active,
            }
            for batch in batches
        ],
        "rules": [
            {"field": rule.field, "operator": rule.operator.value, "value": rule.value}
            for rule in rules
        ],
    }


@router.get("/catalog")
async def catalog(staff: Staff, db: Db) -> list[dict[str, Any]]:
    courses = (
        await db.scalars(
            select(Course)
            .where(Course.tenant_id == staff.tenant_id)
            .order_by(Course.name, Course.id)
            .limit(200)
        )
    ).all()
    return [await course_view(db, course) for course in courses]


@router.get("/catalog/{course_id}")
async def catalog_detail(course_id: uuid.UUID, staff: Staff, db: Db) -> dict[str, Any]:
    return await course_view(db, await owned_course(db, staff, course_id))


async def save_course(db: Db, staff: Staff, course: Course, body: CourseInput) -> dict[str, Any]:
    if course.is_reference:
        raise HTTPException(
            409, "Published reference programmes cannot become admissions offerings here."
        )
    # Check every supplied batch ID before mutating anything. Never re-parent a batch.
    existing = {
        batch.id: batch
        for batch in (
            await db.scalars(
                select(Batch)
                .where(Batch.tenant_id == staff.tenant_id, Batch.course_id == course.id)
                .with_for_update()
            )
        ).all()
    }
    if any(batch.id is not None and batch.id not in existing for batch in body.batches):
        raise HTTPException(404, "Batch not found in this course.")
    course.name, course.description = body.name, body.description
    course.application_fee, course.is_active = body.application_fee, body.is_active
    supplied = {batch.id for batch in body.batches if batch.id}
    # Omitted batches are archived so saved conversations keep their historical selection.
    for batch_id, previous_batch in existing.items():
        if batch_id not in supplied:
            previous_batch.is_active = False
    for item in body.batches:
        batch = existing.get(item.id) if item.id else None
        if batch is None:
            batch = Batch(tenant_id=staff.tenant_id, course_id=course.id)
            db.add(batch)
        batch.name, batch.capacity = item.name, item.capacity
        batch.seats_remaining, batch.is_active = item.seats_remaining, item.is_active
    await db.execute(
        delete(QualificationRule).where(
            QualificationRule.tenant_id == staff.tenant_id, QualificationRule.course_id == course.id
        )
    )
    db.add_all(
        [
            QualificationRule(tenant_id=staff.tenant_id, course_id=course.id, **rule.model_dump())
            for rule in body.rules
        ]
    )
    await write_audit_log(
        db,
        tenant_id=staff.tenant_id,
        actor=str(staff.id),
        action="catalog.saved",
        details={"course_id": str(course.id)},
    )
    await db.flush()
    result = await course_view(db, course)
    await db.commit()
    return result


@router.post("/catalog", status_code=201, dependencies=[Depends(require_browser_write)])
async def create_course(body: CourseInput, staff: Staff, db: Db) -> dict[str, Any]:
    require_admin(staff)
    if any(batch.id for batch in body.batches):
        raise HTTPException(422, "New courses require new batches.")
    course = Course(tenant_id=staff.tenant_id, name=body.name)
    db.add(course)
    await db.flush()
    return await save_course(db, staff, course, body)


@router.put("/catalog/{course_id}", dependencies=[Depends(require_browser_write)])
async def edit_course(
    course_id: uuid.UUID, body: CourseInput, staff: Staff, db: Db
) -> dict[str, Any]:
    require_admin(staff)
    return await save_course(db, staff, await owned_course(db, staff, course_id), body)


@router.delete("/catalog/{course_id}", dependencies=[Depends(require_browser_write)])
async def archive_course(course_id: uuid.UUID, staff: Staff, db: Db) -> dict[str, str]:
    require_admin(staff)
    course = await owned_course(db, staff, course_id)
    course.is_active = False
    await write_audit_log(
        db,
        tenant_id=staff.tenant_id,
        actor=str(staff.id),
        action="catalog.archived",
        details={"course_id": str(course.id)},
    )
    await db.commit()
    return {"status": "archived"}


class Hours(BaseModel):
    model_config = ConfigDict(extra="forbid")
    start: str = Field(pattern=r"^\d{2}:\d{2}$")
    end: str = Field(pattern=r"^\d{2}:\d{2}$")

    @model_validator(mode="after")
    def valid_hours(self) -> Self:
        if time.fromisoformat(self.start) >= time.fromisoformat(self.end):
            raise ValueError("Closing time must follow opening time")
        return self


class SettingsInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=255)
    timezone: str = Field(max_length=100)
    business_hours: dict[Literal["mon", "tue", "wed", "thu", "fri", "sat", "sun"], Hours]
    reengagement_delay_days: int = Field(ge=1, le=365, strict=True)
    telegram_daily_send_limit: int = Field(default=1000, ge=0, le=100000, strict=True)
    retention_days: int | None = Field(default=None, ge=1, le=3650, strict=True)

    @model_validator(mode="after")
    def valid_timezone(self) -> Self:
        try:
            ZoneInfo(self.timezone)
        except (ZoneInfoNotFoundError, ValueError):
            raise ValueError("Choose a valid IANA timezone") from None
        return self


@router.get("/settings")
async def institution_settings(staff: Staff, db: Db) -> dict[str, Any]:
    institution = await db.get(Institution, staff.tenant_id)
    if institution is None:
        raise HTTPException(404, "Institution not found.")
    return {
        "name": institution.name,
        "timezone": institution.timezone,
        "business_hours": institution.business_hours or {},
        "reengagement_delay_days": institution.reengagement_delay_days,
        "telegram_daily_send_limit": institution.telegram_daily_send_limit,
        "retention_days": institution.retention_days,
    }


@router.put("/settings", dependencies=[Depends(require_browser_write)])
async def save_settings(body: SettingsInput, staff: Staff, db: Db) -> dict[str, Any]:
    require_admin(staff)
    institution = await db.scalar(
        select(Institution).where(Institution.id == staff.tenant_id).with_for_update()
    )
    if institution is None:
        raise HTTPException(404, "Institution not found.")
    for key, value in body.model_dump().items():
        if key == "telegram_daily_send_limit" and key not in body.model_fields_set:
            continue  # Older clients must preserve a configured budget.
        setattr(institution, key, value)
    if {"telegram_daily_send_limit", "timezone"} & body.model_fields_set:
        # An administrator can raise a cap or change local days without leaving
        # already-deferred messages asleep until the old reset time.
        for delivery in (ConversationReply, OutboundMessage):
            await db.execute(
                update(delivery)
                .where(
                    delivery.tenant_id == staff.tenant_id,
                    delivery.status == "queued",
                    delivery.error_code == "daily_send_budget",
                )
                .values(next_attempt_at=None)
            )
    await write_audit_log(
        db, tenant_id=staff.tenant_id, actor=str(staff.id), action="institution.settings_updated"
    )
    await db.commit()
    return await institution_settings(staff, db)


@router.get("/delivery-budget")
async def delivery_budget(staff: Staff, db: Db) -> dict[str, Any]:
    from src.telegram.budget import usage

    institution = await db.get(Institution, staff.tenant_id)
    if institution is None:
        raise HTTPException(404, "Institution not found.")
    result = await usage(institution)
    start = datetime.fromisoformat(result["day"]).replace(tzinfo=ZoneInfo(result["timezone"]))
    reset = datetime.fromisoformat(result["resets_at"])
    deferred = 0
    confirmed = 0
    for delivery in (ConversationReply, OutboundMessage):
        deferred += int(
            await db.scalar(
                select(func.count())
                .select_from(delivery)
                .where(
                    delivery.tenant_id == staff.tenant_id,
                    delivery.status == "queued",
                    delivery.error_code.in_(["daily_send_budget", "send_budget_unavailable"]),
                )
            )
            or 0
        )
        confirmed += int(
            await db.scalar(
                select(func.count())
                .select_from(delivery)
                .where(
                    delivery.tenant_id == staff.tenant_id,
                    delivery.status == "sent",
                    delivery.updated_at >= start,
                    delivery.updated_at < reset,
                )
            )
            or 0
        )
    # Durable completion records remain authoritative if a Redis stats write was lost.
    return {**result, "confirmed_sent": confirmed, "deferred": deferred}


class DiscountInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    code: str = Field(pattern=r"^[A-Za-z0-9_-]{1,64}$")
    discount_type: DiscountType
    amount: int = Field(ge=1, le=1000000000, strict=True)
    max_uses: int | None = Field(default=None, ge=1, le=1000000000, strict=True)
    is_active: bool = True

    @model_validator(mode="after")
    def valid_discount(self) -> Self:
        if self.discount_type == DiscountType.PERCENT and self.amount > 100:
            raise ValueError("Percentage discounts cannot exceed 100")
        self.code = self.code.upper()
        return self


def discount_view(discount: DiscountCode) -> dict[str, Any]:
    return {
        "id": str(discount.id),
        "code": discount.code,
        "discount_type": discount.discount_type.value,
        "amount": discount.amount,
        "max_uses": discount.max_uses,
        "uses_count": discount.uses_count,
        "is_active": discount.is_active,
    }


async def owned_discount(db: Db, staff: Staff, discount_id: uuid.UUID) -> DiscountCode:
    discount = await db.scalar(
        select(DiscountCode)
        .where(DiscountCode.id == discount_id, DiscountCode.tenant_id == staff.tenant_id)
        .with_for_update()
    )
    if discount is None:
        raise HTTPException(404, "Discount not found.")
    return discount


@router.get("/discounts")
async def discounts(staff: Staff, db: Db) -> list[dict[str, Any]]:
    records = (
        await db.scalars(
            select(DiscountCode)
            .where(DiscountCode.tenant_id == staff.tenant_id)
            .order_by(DiscountCode.code, DiscountCode.id)
            .limit(200)
        )
    ).all()
    return [discount_view(record) for record in records]


async def save_discount(
    db: Db, staff: Staff, record: DiscountCode, body: DiscountInput
) -> dict[str, Any]:
    if body.max_uses is not None and body.max_uses < (record.uses_count or 0):
        raise HTTPException(422, "Maximum uses cannot be below the number already used.")
    for key, value in body.model_dump().items():
        setattr(record, key, value)
    try:
        await write_audit_log(
            db,
            tenant_id=staff.tenant_id,
            actor=str(staff.id),
            action="discount.saved",
            details={"discount_id": str(record.id)},
        )
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(409, "A discount with that code already exists.") from None
    return discount_view(record)


@router.post("/discounts", status_code=201, dependencies=[Depends(require_browser_write)])
async def create_discount(body: DiscountInput, staff: Staff, db: Db) -> dict[str, Any]:
    require_admin(staff)
    record = DiscountCode(id=uuid.uuid4(), tenant_id=staff.tenant_id, uses_count=0)
    db.add(record)
    return await save_discount(db, staff, record, body)


@router.put("/discounts/{discount_id}", dependencies=[Depends(require_browser_write)])
async def edit_discount(
    discount_id: uuid.UUID, body: DiscountInput, staff: Staff, db: Db
) -> dict[str, Any]:
    require_admin(staff)
    return await save_discount(db, staff, await owned_discount(db, staff, discount_id), body)


@router.delete("/discounts/{discount_id}", dependencies=[Depends(require_browser_write)])
async def archive_discount(discount_id: uuid.UUID, staff: Staff, db: Db) -> dict[str, str]:
    require_admin(staff)
    record = await owned_discount(db, staff, discount_id)
    record.is_active = False
    await write_audit_log(
        db,
        tenant_id=staff.tenant_id,
        actor=str(staff.id),
        action="discount.archived",
        details={"discount_id": str(record.id)},
    )
    await db.commit()
    return {"status": "archived"}
