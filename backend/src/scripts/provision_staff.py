"""Manually provision an institution administrator without printing credentials."""

import argparse
import asyncio
import getpass
import re

from sqlalchemy import select

from src.db.enums import StaffRole
from src.db.models import Institution, StaffUser
from src.db.session import get_engine, get_sessionmaker
from src.staff.auth import hash_password


async def provision(code: str, name: str, email: str, password: str) -> None:
    if not re.fullmatch(r"[a-z0-9-]{1,64}", code):
        raise ValueError("Institution code must use lowercase letters, numbers and hyphens")
    try:
        async with get_sessionmaker()() as db:
            institution = await db.scalar(select(Institution).where(Institution.slug == code))
            if institution is None:
                institution = Institution(name=name, slug=code)
                db.add(institution)
                await db.flush()
            existing = await db.scalar(
                select(StaffUser).where(
                    StaffUser.tenant_id == institution.id, StaffUser.email == email.strip().lower()
                )
            )
            if existing:
                raise ValueError("This staff account already exists; it has not been overwritten")
            db.add(
                StaffUser(
                    tenant_id=institution.id,
                    email=email.strip().lower(),
                    hashed_password=hash_password(password),
                    role=StaffRole.ADMIN,
                )
            )
            await db.commit()
        print("Institution administrator provisioned. Sign in through the knowledge workspace.")
    finally:
        await get_engine().dispose()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--institution-code", required=True)
    parser.add_argument("--institution-name", required=True)
    parser.add_argument("--email", required=True)
    args = parser.parse_args()
    password = getpass.getpass("New staff password (at least 12 characters): ")
    if password != getpass.getpass("Confirm password: "):
        raise SystemExit("Passwords did not match; nothing was changed")
    asyncio.run(provision(args.institution_code, args.institution_name, args.email, password))


if __name__ == "__main__":
    main()
