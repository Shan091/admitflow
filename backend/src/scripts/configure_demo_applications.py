"""Opt a local reference catalogue into test-only demo applications without changing real fees."""

import argparse
import asyncio
from urllib.parse import urlsplit

from sqlalchemy import select

from src.core.demo_admissions import demo_fee
from src.core.settings import get_settings
from src.db.audit import write_audit_log
from src.db.models import Course, Institution
from src.db.session import get_engine, get_sessionmaker


async def configure(code: str, fee_paise: int, expected_courses: int) -> None:
    settings = get_settings()
    if not 100 <= fee_paise <= 1000000000:
        raise ValueError("The demo fee must be integer paise between INR 1 and INR 10000000")
    if urlsplit(settings.database_url or "").hostname not in {"localhost", "127.0.0.1", "::1"}:
        raise ValueError("This script only configures a loopback development database")
    async with get_sessionmaker()() as db:
        institution = await db.scalar(select(Institution).where(Institution.slug == code))
        if institution is None:
            raise ValueError("Institution not found")
        courses = list(
            (
                await db.scalars(
                    select(Course)
                    .where(
                        Course.tenant_id == institution.id,
                        Course.is_reference.is_(True),
                    )
                    .with_for_update()
                )
            ).all()
        )
        if len(courses) != expected_courses or not any(c.is_active for c in courses):
            raise ValueError("The reference catalogue count changed; inspect before configuration")
        for course in courses:
            course.demo_application_fee = fee_paise
            if course.is_active and await demo_fee(db, course) != fee_paise:
                raise ValueError(
                    "Enable development demo mode with institution-owned test credentials first"
                )
        await write_audit_log(
            db,
            tenant_id=institution.id,
            actor="local-owner-configuration",
            action="demo_applications.configured",
            details={"course_count": len(courses), "fee_paise": fee_paise},
        )
        await db.commit()
        print(
            f"Configured {len(courses)} demo courses at INR {fee_paise / 100:.2f}. "
            "Real fees, seats and archived status unchanged."
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--institution-code", required=True)
    parser.add_argument("--fee-paise", required=True, type=int)
    parser.add_argument("--expected-courses", required=True, type=int)
    args = parser.parse_args()

    async def run() -> None:
        try:
            await configure(args.institution_code, args.fee_paise, args.expected_courses)
        finally:
            await get_engine().dispose()

    try:
        asyncio.run(run())
    except Exception as error:
        print(
            f"Demo configuration failed: {type(error).__name__}. "
            "Check local mode, catalogue and test credentials."
        )
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
