"""Audited institution exports, with explicit limits and spreadsheet-safe text."""

import asyncio
import csv
import io
import json
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Response
from openpyxl import Workbook
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE, WriteOnlyCell
from sqlalchemy import select

from src.core.security import decrypt_pii
from src.core.settings import get_settings
from src.db.audit import write_audit_log
from src.db.models import Application, Course, PaymentOrder
from src.staff.auth import Db, Staff, require_admin, require_browser_write
from src.staff.crm import LeadFilters, lead_statement

router = APIRouter(prefix="/api/staff", tags=["staff exports"])


class ExportRequest(LeadFilters):
    dataset: Literal["leads", "applications", "payments"]
    format: Literal["csv", "xlsx"]


def clean(value: str) -> str:
    return ILLEGAL_CHARACTERS_RE.sub("", value)


def render_csv(rows: list[list[str]]) -> bytes:
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    for row in rows:
        safe = []
        for value in row:
            value = clean(value)
            safe.append("'" + value if value.lstrip().startswith(("=", "+", "-", "@")) else value)
        writer.writerow(safe)
    return output.getvalue().encode("utf-8-sig")


def render_xlsx(rows: list[list[str]]) -> bytes:
    workbook = Workbook(write_only=True)
    sheet = workbook.create_sheet("Export")
    for row in rows:
        cells = []
        for value in row:
            cell = WriteOnlyCell(sheet, value=clean(value))
            cell.data_type = "s"
            cells.append(cell)
        sheet.append(cells)
    output = io.BytesIO()
    workbook.save(output)
    return output.getvalue()


def text(value: object) -> str:
    return "" if value is None else str(value)


async def export_rows(payload: ExportRequest, staff: Staff, db: Db) -> list[list[str]]:
    limit = get_settings().staff_export_max_rows
    if payload.dataset == "leads":
        records = (
            await db.execute(lead_statement(staff.tenant_id, payload).limit(limit + 1))
        ).all()
        rows = [
            ["inquiry_id", "name", "phone", "status", "course", "readiness_score", "created_at"]
        ]
        for lead, course in records:
            rows.append(
                [
                    str(lead.id),
                    decrypt_pii(lead.name_enc) if lead.name_enc else "",
                    decrypt_pii(lead.phone_enc) if lead.phone_enc else "",
                    lead.status.value,
                    course or "",
                    text(lead.readiness_score),
                    lead.created_at.isoformat(),
                ]
            )
    else:
        # Inquiry filters deliberately do not apply to application/payment exports.
        if payload.query or payload.status or payload.course_id:
            raise HTTPException(422, "Inquiry filters apply only to inquiry exports.")
        if payload.dataset == "applications":
            applications = (
                await db.execute(
                    select(Application, Course.name)
                    .join(
                        Course,
                        (Course.id == Application.course_id)
                        & (Course.tenant_id == Application.tenant_id),
                    )
                    .where(Application.tenant_id == staff.tenant_id)
                    .order_by(Application.submitted_at.desc(), Application.id)
                    .limit(limit + 1)
                )
            ).all()
            fields = ["dob", "parent_name", "address", "previous_school"]
            rows = [
                [
                    "application_id",
                    "inquiry_id",
                    "full_name",
                    "course",
                    "batch_id",
                    "status",
                    "submitted_at",
                    *fields,
                ]
            ]
            for application, course in applications:
                form = (
                    json.loads(decrypt_pii(application.form_data_enc))
                    if application.form_data_enc
                    else {
                        "dob": text(application.dob),
                        "parent_name": decrypt_pii(application.parent_name_enc)
                        if application.parent_name_enc
                        else "",
                        "address": decrypt_pii(application.address_enc)
                        if application.address_enc
                        else "",
                        "previous_school": application.previous_school,
                    }
                )
                rows.append(
                    [
                        str(application.id),
                        str(application.lead_id),
                        decrypt_pii(application.full_name_enc),
                        course,
                        text(application.batch_id),
                        application.status.value,
                        application.submitted_at.isoformat(),
                        *(text(form.get(key)) for key in fields),
                    ]
                )
        else:
            payments = (
                await db.scalars(
                    select(PaymentOrder)
                    .where(PaymentOrder.tenant_id == staff.tenant_id)
                    .order_by(PaymentOrder.created_at.desc(), PaymentOrder.id)
                    .limit(limit + 1)
                )
            ).all()
            rows = [
                [
                    "payment_id",
                    "inquiry_id",
                    "application_id",
                    "course_id",
                    "amount_minor_units",
                    "currency",
                    "status",
                    "creation_state",
                    "provider_order_id",
                    "provider_payment_id",
                    "created_at",
                ]
            ]
            for payment in payments:
                rows.append(
                    [
                        str(payment.id),
                        str(payment.lead_id),
                        str(payment.application_id),
                        str(payment.course_id),
                        str(payment.amount),
                        payment.currency,
                        payment.status.value,
                        payment.creation_state,
                        text(payment.razorpay_order_id),
                        text(payment.razorpay_payment_id),
                        payment.created_at.isoformat(),
                    ]
                )
    if len(rows) - 1 > limit:
        raise HTTPException(
            422,
            f"Export exceeds the {limit:,} row limit. Narrow inquiry filters or "
            "contact your administrator for a managed export.",
        )
    if any(len(value) > 32767 for row in rows for value in row):
        raise HTTPException(
            422, "A value exceeds the spreadsheet cell limit. Request a managed export."
        )
    return rows


@router.post("/exports", dependencies=[Depends(require_browser_write)])
async def download(payload: ExportRequest, staff: Staff, db: Db) -> Response:
    require_admin(staff)
    rows = await export_rows(payload, staff, db)
    output = await asyncio.to_thread(render_csv if payload.format == "csv" else render_xlsx, rows)
    await write_audit_log(
        db,
        tenant_id=staff.tenant_id,
        actor=str(staff.id),
        action="staff.data_exported",
        details={"dataset": payload.dataset, "format": payload.format, "row_count": len(rows) - 1},
    )
    await db.commit()
    return Response(
        content=output,
        media_type="text/csv; charset=utf-8"
        if payload.format == "csv"
        else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": (
                f'attachment; filename="admitflow-{payload.dataset}.{payload.format}"'
            ),
            "Cache-Control": "no-store",
            "X-Content-Type-Options": "nosniff",
        },
    )
