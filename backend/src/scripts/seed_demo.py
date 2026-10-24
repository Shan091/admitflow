"""Idempotent synthetic institution/catalog/staff seed; no real applicant data."""

import asyncio
import json
import os
import secrets

from sqlalchemy import select

from src.core.settings import get_settings
from src.db.audit import write_audit_log
from src.db.enums import RuleOperator, StaffRole
from src.db.models import Batch, Course, Institution, QualificationRule, StaffUser
from src.db.session import get_engine, get_sessionmaker
from src.staff.auth import hash_password


async def seed() -> None:
    code = get_settings().telegram_institution_code
    async with get_sessionmaker()() as db:
        institution = await db.scalar(select(Institution).where(Institution.slug == code))
        if institution and await db.scalar(
            select(Course.id)
            .where(Course.tenant_id == institution.id, Course.is_reference.is_(True))
            .limit(1)
        ):
            await db.rollback()
            await get_engine().dispose()
            print("Published reference catalogue exists; synthetic seeding was skipped.")
            return
        if institution is None:
            institution = Institution(name="AdmitFlow Demo Institute", slug=code)
            db.add(institution)
            await db.flush()
        email = "demo@admitflow.test"
        staff = await db.scalar(
            select(StaffUser).where(StaffUser.tenant_id == institution.id, StaffUser.email == email)
        )
        credential_path = get_settings().demo_credentials_path
        if staff is None:
            if await asyncio.to_thread(credential_path.exists):
                raise ValueError(
                    "Resolve the existing demo credential file before creating an account"
                )
            password = secrets.token_urlsafe(24)
            staff = StaffUser(
                tenant_id=institution.id,
                email=email,
                role=StaffRole.ADMIN,
                full_name="Synthetic demo administrator",
                hashed_password=hash_password(password),
            )
            db.add(staff)
            # Exclusive file creation prevents overwriting an existing operator credential.
            descriptor = os.open(credential_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                json.dump(
                    {"institution": code, "email": email, "password": password}, stream, indent=2
                )
                stream.write("\n")
        for name, description in [
            (
                "Digital Skills Foundation",
                "A synthetic introductory programme for the admissions demonstration.",
            ),
            (
                "Healthcare Office Skills",
                "A synthetic office-skills programme; not a licensed clinical qualification.",
            ),
        ]:
            course = await db.scalar(
                select(Course).where(Course.tenant_id == institution.id, Course.name == name)
            )
            if course is not None:
                continue
            course = Course(
                tenant_id=institution.id, name=name, description=description, application_fee=50000
            )
            db.add(course)
            await db.flush()
            db.add_all(
                [
                    Batch(
                        tenant_id=institution.id,
                        course_id=course.id,
                        name=label,
                        capacity=20,
                        seats_remaining=20,
                    )
                    for label in ("Morning", "Evening")
                ]
            )
            db.add_all(
                [
                    QualificationRule(
                        tenant_id=institution.id,
                        course_id=course.id,
                        field=field,
                        operator=RuleOperator.GTE,
                        value=value,
                    )
                    for field, value in (("age", 18), ("marks_percentage", 50))
                ]
            )
        await write_audit_log(
            db, tenant_id=institution.id, actor="local-provisioner", action="demo.seeded"
        )
        await db.commit()
    await get_engine().dispose()
    print(
        "Synthetic catalog ready. Staff credentials are in the private configured "
        "DEMO_CREDENTIALS_PATH (default .demo-credentials.json); no password was printed."
    )


def main() -> None:
    try:
        asyncio.run(seed())
    except Exception as error:
        print(f"Demo seed failed: {type(error).__name__}. No credentials were printed.")
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
