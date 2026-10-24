"""Explicit local-only reset and atomic publication of sourced reference programmes.

Pause the local API, receiver and workers before --apply. Never run against production.
The default is read-only validation. Admin access, bot credentials and polling offsets survive.
"""

import argparse
import asyncio
import hashlib
import json
from pathlib import Path
from typing import Literal, Self
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from sqlalchemy import delete, func, select
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import encrypt_bytes
from src.core.settings import get_settings
from src.db.audit import write_audit_log
from src.db.models import (
    Base,
    Course,
    Document,
    DocumentChunk,
    Institution,
    KnowledgeUpload,
    PaymentOrder,
    StaffUser,
)
from src.db.session import get_engine, get_sessionmaker
from src.knowledge.processing import embed_chunks

DEFAULT_DATA = Path(__file__).resolve().parents[2] / "data/jain-kochi/catalogue.json"
NAME = "JAIN (Deemed-to-be University), Kochi — public-information demo"
DUMMY_NAMES = {"AdmitFlow Demo Institute", "AdmitFlow Synthetic Demo Institution", NAME}
PRESERVED = {"institutions", "staff_users", "staff_sessions", "telegram_bots"}


class Programme(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=255)
    level: Literal["undergraduate", "postgraduate"]
    degree: str = Field(min_length=1, max_length=200)
    overview: str = Field(min_length=1, max_length=450)
    published_eligibility: str = Field(min_length=1, max_length=500)
    published_duration: str = Field(min_length=1, max_length=100)
    source_url: str
    listing_url: str

    @field_validator("source_url", "listing_url")
    @classmethod
    def official_source(cls, value: str) -> str:
        url = urlsplit(value)
        if (
            url.scheme != "https"
            or url.hostname != "www.jainuniversity.ac.in"
            or not url.path.startswith("/kochi/")
            or url.username
            or url.password
            or url.port not in {None, 443}
            or url.query
            or url.fragment
            or len(value) > 1024
        ):
            raise ValueError("Use a canonical official Kochi source URL")
        return value

    def content(self) -> str:
        return (
            f"{self.name}\n{self.level.capitalize()} programme: {self.degree}.\n"
            f"{self.overview}\nPublished eligibility: {self.published_eligibility}\n"
            f"Published duration: {self.published_duration}\n"
            "Current fees, intakes and seats are unverified. Published reference only; "
            "this demonstration does not process university applications or payments."
        )


class PublicCatalogue(BaseModel):
    model_config = ConfigDict(extra="forbid")
    institution: Literal["JAIN (Deemed-to-be University), Kochi"]
    mode: Literal["published-reference-only"]
    discovery_provider: Literal["SerpAPI"]
    retrieved_on: str
    homepage: Literal["https://www.jainuniversity.ac.in/kochi/"]
    contact: dict[str, str]
    limitations: list[str]
    programmes: list[Programme] = Field(min_length=1, max_length=80)

    @model_validator(mode="after")
    def unique_names(self) -> Self:
        if len({p.name.casefold() for p in self.programmes}) != len(self.programmes):
            raise ValueError("Programme names must be distinct")
        return self

    def campus_content(self) -> str:
        return (
            f"{self.institution}\nOfficial campus contact information:\n"
            + "\n".join(f"{key}: {value}" for key, value in self.contact.items())
            + "\nIndependent public-information demonstration. Not an official university "
            "admissions channel. Published courses can be explored, but current fees, "
            "intakes, entry decisions and seat availability need university confirmation."
        )


async def validate_reset_target(
    db: AsyncSession, code: str
) -> tuple[Institution, StaffUser, list[Institution]]:
    institutions = list((await db.scalars(select(Institution).with_for_update())).all())
    if not institutions or any(i.name not in DUMMY_NAMES for i in institutions):
        raise ValueError("Database contains an institution outside the confirmed dummy-data scope")
    target = next((i for i in institutions if i.slug == code), None)
    staff = list((await db.scalars(select(StaffUser))).all())
    if target is None or len(staff) != 1 or staff[0].tenant_id != target.id:
        raise ValueError("Expected the single local demo administrator")
    if await db.scalar(select(func.count()).select_from(PaymentOrder)):
        raise ValueError("Payment records require an independently reviewed reset scope")
    return target, staff[0], institutions


async def replace(
    db: AsyncSession, code: str, catalogue: PublicCatalogue, vectors: list[list[float]]
) -> dict[str, int]:
    """One transaction; callers commit only after counts/config preservation are checked."""
    if len(vectors) != len(catalogue.programmes) + 1 or any(len(v) != 1536 for v in vectors):
        raise ValueError("A complete embedding set is required before any deletion")
    target, admin, institutions = await validate_reset_target(db, code)
    counts = {}
    for table in reversed(Base.metadata.sorted_tables):
        if table.name not in PRESERVED:
            counts[table.name] = int(await db.scalar(select(func.count()).select_from(table)) or 0)
            await db.execute(delete(table))
    for other in institutions:
        if other.id != target.id:
            await db.delete(other)
    target.name = NAME
    admin.full_name = "shan"
    await db.flush()
    texts = [catalogue.campus_content(), *(p.content() for p in catalogue.programmes)]
    for index, (content, vector) in enumerate(zip(texts, vectors, strict=True)):
        course = None
        url: str = catalogue.homepage
        if index:
            programme = catalogue.programmes[index - 1]
            course = Course(
                tenant_id=target.id,
                name=programme.name,
                description=content,
                is_active=True,
                is_reference=True,
                reference_url=programme.source_url,
                application_fee=0,
            )
            db.add(course)
            await db.flush()
            url = programme.source_url
        raw = content.encode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()
        filename = f"jain-kochi-{index:02d}.txt"
        path = f"public/jain-kochi/{filename}"
        metadata = {"source": "official-public-reference", "path": path, "source_url": url}
        if course:
            metadata["course_id"] = str(course.id)
        doc = Document(
            tenant_id=target.id,
            title=filename,
            content_hash=digest,
            source_url=url,
            metadata_json=metadata,
        )
        db.add(doc)
        await db.flush()
        db.add(
            DocumentChunk(
                tenant_id=target.id,
                document_id=doc.id,
                chunk_index=0,
                content=content,
                embedding=vector,
                embedding_model=get_settings().llm_embedding_model,
            )
        )
        db.add(
            KnowledgeUpload(
                tenant_id=target.id,
                uploaded_by=admin.id,
                filename=filename,
                relative_path=path,
                content_hash=digest,
                source_enc=encrypt_bytes(raw),
                byte_size=len(raw),
                status="ready",
                document_id=doc.id,
                chunk_count=1,
                attempts=1,
            )
        )
    await write_audit_log(
        db,
        tenant_id=target.id,
        actor="local-catalogue-import",
        action="demo.replaced_with_public_reference",
        details={"programmes": len(catalogue.programmes)},
    )
    await db.flush()
    return counts


async def run(args: argparse.Namespace) -> None:
    settings = get_settings()
    url = make_url(settings.database_url or "")
    if settings.app_env == "prod" or url.host not in {"localhost", "127.0.0.1", "::1"}:
        raise ValueError("This command is limited to a loopback development database")
    if args.confirm_database != url.database:
        raise ValueError("Confirm the exact local database name")
    catalogue = PublicCatalogue.model_validate_json(args.dataset.read_text(encoding="utf-8"))
    async with get_sessionmaker()() as db:
        _, _, institutions = await validate_reset_target(db, args.institution_code)
        ids = [i.id for i in institutions]
        await db.rollback()
    if not args.apply:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "programmes": len(catalogue.programmes),
                    "institutions_in_reset_scope": len(ids),
                }
            )
        )
        return
    # No database data is removed until the complete external embedding request succeeds.
    vectors = await embed_chunks(
        [catalogue.campus_content(), *(p.content() for p in catalogue.programmes)]
    )
    async with get_sessionmaker()() as db:
        counts = await replace(db, args.institution_code, catalogue, vectors)
        await db.commit()
    # Clear only these tenants' dashboard budget counters; never flush shared Redis.
    if settings.redis_url:
        from redis.asyncio import Redis

        redis = Redis.from_url(settings.redis_url)
        try:
            for tenant_id in ids:
                keys = [
                    key async for key in redis.scan_iter(match=f"telegram-budget:{{{tenant_id}}}:*")
                ]
                if keys:
                    await redis.delete(*keys)
        finally:
            await redis.aclose()
    print(
        json.dumps(
            {
                "reset_committed": True,
                "removed_rows": counts,
                "reference_programmes": len(catalogue.programmes),
                "knowledge_documents": len(vectors),
                "admin_and_bot_configuration_preserved": True,
            }
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--institution-code", default="demo")
    parser.add_argument("--confirm-database", required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    async def execute() -> None:
        try:
            await run(args)
        finally:
            await get_engine().dispose()

    try:
        asyncio.run(execute())
    except Exception as error:
        print(
            f"Import stopped: {type(error).__name__}. No secret or applicant values were printed."
        )
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
