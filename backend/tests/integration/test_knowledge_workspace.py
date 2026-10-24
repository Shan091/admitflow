"""Real PostgreSQL acceptance for authenticated uploads and atomic semantic indexing."""

import asyncio
import io
import json
import uuid
from collections.abc import AsyncIterator, Iterator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from alembic import command
from alembic.config import Config
from cryptography.fernet import Fernet
from docx import Document as WordDocument
from fastapi.testclient import TestClient
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject
from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from testcontainers.community.postgres import PostgresContainer

from src.core.security import decrypt_bytes
from src.core.settings import Settings
from src.db.enums import StaffRole
from src.db.models import (
    Document,
    DocumentChunk,
    Institution,
    KnowledgeUpload,
    StaffSession,
    StaffUser,
)
from src.db.session import get_session
from src.knowledge import processing
from src.knowledge.extraction import ExtractionError
from src.knowledge.pdf_parser import parse_pdf as real_parse_pdf
from src.knowledge.pdf_worker import preflight_pdf
from src.staff.auth import hash_password

pytestmark = pytest.mark.integration
PASSWORD = "synthetic-workspace-password"
HEAD = "b627da2f7e11"


async def fake_embeddings(texts: list[str]) -> list[list[float]]:
    # Two orthogonal topics exercise actual pgvector distance and abstention.
    return [
        [1.0, 0.0] + [0.0] * 1534 if "fee" in text.lower() else [0.0, 1.0] + [0.0] * 1534
        for text in texts
    ]


@pytest.fixture(scope="module")
def workspace() -> Iterator[dict[str, Any]]:
    with PostgresContainer("pgvector/pgvector:pg16", driver="asyncpg") as container:
        with pytest.MonkeyPatch.context() as mp:
            settings = Settings(
                _env_file=None,
                database_url=container.get_connection_url(),
                redis_url=None,
                pii_encryption_key=Fernet.generate_key().decode(),
                knowledge_recovery_enabled=False,
                integration_recovery_enabled=False,
            )
            for module in (
                "src.core.settings",
                "src.core.security",
                "src.main",
                "src.staff.auth",
                "src.staff.throttle",
                "src.knowledge.api",
                "src.knowledge.processing",
                "src.knowledge.limits",
            ):
                mp.setattr(f"{module}.get_settings", lambda: settings)
            command.upgrade(Config("alembic.ini"), "head")
            engine = create_async_engine(settings.database_url, poolclass=NullPool)
            sessions = async_sessionmaker(engine, expire_on_commit=False)
            mp.setattr(processing, "get_sessionmaker", lambda: sessions)
            mp.setattr(processing, "embed_chunks", fake_embeddings)

            async def basic_pdf(data: bytes) -> str:
                from pypdf import PdfReader

                try:
                    preflight_pdf(data)
                except ExtractionError:
                    raise
                except Exception:
                    raise ExtractionError("invalid_document") from None
                return "\n\n".join(
                    p.extract_text() or "" for p in PdfReader(io.BytesIO(data)).pages
                )

            mp.setattr(processing, "parse_pdf", basic_pdf)
            mp.setattr("src.knowledge.api.embed_chunks", fake_embeddings)

            ranking_inputs: list[list[str]] = []

            async def rank(messages: list[dict[str, str]], **kwargs: Any) -> Any:
                passages = json.loads(messages[-1]["content"])["passages"]
                ranking_inputs.append([p["text"] for p in passages])
                return SimpleNamespace(
                    choices=[
                        SimpleNamespace(
                            message=SimpleNamespace(
                                content=json.dumps(
                                    {"ordered_ids": [p["id"] for p in passages[::-1]]}
                                )
                            )
                        )
                    ]
                )

            mp.setattr("src.decision.generate_completion", rank)

            async def unavailable_queue() -> None:
                raise ConnectionError("synthetic queue outage")

            mp.setattr("src.knowledge.api.dispatch_pending", unavailable_queue)

            async def db_dependency() -> AsyncIterator[AsyncSession]:
                async with sessions() as session:
                    yield session

            async def seed() -> tuple[uuid.UUID, uuid.UUID]:
                async with sessions() as db:
                    first = Institution(name="First synthetic", slug="first")
                    second = Institution(name="Second synthetic", slug="second")
                    db.add_all([first, second])
                    await db.flush()
                    for tenant in (first, second):
                        db.add(
                            StaffUser(
                                tenant_id=tenant.id,
                                email="admin@example.test",
                                hashed_password=hash_password(PASSWORD),
                                full_name="Synthetic admin",
                                role=StaffRole.ADMIN,
                            )
                        )
                    db.add(
                        StaffUser(
                            tenant_id=first.id,
                            email="agent@example.test",
                            hashed_password=hash_password(PASSWORD),
                            full_name="Synthetic agent",
                            role=StaffRole.AGENT,
                        )
                    )
                    await db.commit()
                    return first.id, second.id

            tenants = asyncio.run(seed())
            from src.main import create_app

            app = create_app()
            app.dependency_overrides[get_session] = db_dependency
            with TestClient(app) as client:
                yield {
                    "client": client,
                    "sessions": sessions,
                    "tenants": tenants,
                    "settings": settings,
                    "app": app,
                    "ranking_inputs": ranking_inputs,
                }

            async def clean() -> None:
                async with sessions() as db:
                    await db.execute(delete(KnowledgeUpload))
                    await db.execute(delete(Document))
                    await db.execute(delete(Institution))
                    await db.commit()
                await engine.dispose()

            asyncio.run(clean())
            # Exercise the new revision's down/up path, then the full migration chain.
            command.downgrade(Config("alembic.ini"), "8f4b1c2d3e60")
            command.upgrade(Config("alembic.ini"), HEAD)
            command.downgrade(Config("alembic.ini"), "base")


def signin(
    client: TestClient, institution: str = "first", email: str = "admin@example.test"
) -> None:
    client.cookies.clear()
    response = client.post(
        "/api/staff/login",
        headers={"X-AdmitFlow-Request": "1"},
        json={"institution": institution, "email": email, "password": PASSWORD},
    )
    assert response.status_code == 200, response.text
    assert "HttpOnly" in response.headers["set-cookie"]
    assert "SameSite=strict" in response.headers["set-cookie"]


def send(client: TestClient, files: list[tuple[str, bytes]]) -> dict[str, Any]:
    response = client.post(
        "/api/knowledge/documents",
        headers={"X-AdmitFlow-Request": "1"},
        files=[("files", (name, data)) for name, data in files],
    )
    assert response.status_code == 200, response.text
    return response.json()


def readable_pdf() -> bytes:
    writer = PdfWriter()
    page = writer.add_blank_page(width=400, height=200)
    font = DictionaryObject(
        {
            NameObject("/Type"): NameObject("/Font"),
            NameObject("/Subtype"): NameObject("/Type1"),
            NameObject("/BaseFont"): NameObject("/Helvetica"),
        }
    )
    page[NameObject("/Resources")] = DictionaryObject(
        {NameObject("/Font"): DictionaryObject({NameObject("/F1"): writer._add_object(font)})}
    )
    stream = DecodedStreamObject()
    stream.set_data(b"BT /F1 12 Tf 10 100 Td (Annual fees are INR 45000.) Tj ET")
    page[NameObject("/Contents")] = writer._add_object(stream)
    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()


@pytest.mark.skipif(
    not Path(".runtime/document-models/.ready.json").is_file(),
    reason="Prepare offline document models for the real layout acceptance check",
)
def test_complex_pdf_upload_preserves_table_and_programme_context(workspace, monkeypatch):
    client = workspace["client"]
    signin(client)
    data = Path("tests/fixtures/structured-prospectus.pdf").read_bytes()
    row = send(client, [("structured/prospectus.pdf", data)])["accepted"][0]
    upload_id = uuid.UUID(row["id"])
    tenant = workspace["tenants"][0]
    monkeypatch.setattr(processing, "parse_pdf", real_parse_pdf)

    async def index_and_read():
        await processing.process_upload(tenant, upload_id)
        async with workspace["sessions"]() as db:
            upload = await db.get(KnowledgeUpload, upload_id)
            assert upload.status == "ready", upload.error_code
            return list(
                await db.scalars(
                    select(DocumentChunk.content)
                    .where(
                        DocumentChunk.document_id == upload.document_id,
                        DocumentChunk.tenant_id == tenant,
                    )
                    .order_by(DocumentChunk.chunk_index)
                )
            )

    chunks = asyncio.run(index_and_read())
    nursing = [text for text in chunks if "### Nursing Programme" in text]
    commerce = [text for text in chunks if "### Commerce Programme" in text]
    assert nursing and commerce
    for section, programme, tuition, hostel in (
        (nursing, "Nursing Programme", "45000", "11000"),
        (commerce, "Commerce Programme", "35000", "9000"),
    ):
        table = next(text for text in section if "| Tuition" in text)
        rows = [
            [cell.strip() for cell in line.strip("|").split("|")]
            for line in table.splitlines()
            if line.startswith("|")
        ]
        assert [programme, "Tuition", f"INR {tuition}"] in rows
        assert [programme, "Hostel", f"INR {hostel}"] in rows
        assert "Printed tuition examples do not set the application or registration fee." in table
        assert any("Eligibility" in text for text in section)
        assert any("Facilities" in text for text in section)
    assert all("Commerce Programme" not in text for text in nursing)
    assert all("Nursing Programme" not in text for text in commerce)
    joined = "\n".join(chunks)
    assert "School marks must be at least 60 percent." in joined
    assert "The library is open from 9 AM to 5 PM." in joined
    assert joined.index("Applicants must be at least 18") < joined.index("School marks")
    assert joined.index("Hostel accommodation") < joined.index("The library")
    assert "No real institution or applicant data." in joined

    # Remove this fixture's published evidence so other workspace tests remain independent.
    response = client.delete(
        f"/api/knowledge/documents/{upload_id}", headers={"X-AdmitFlow-Request": "1"}
    )
    assert response.status_code in (200, 204)
    client.cookies.clear()


def test_upload_formats_search_duplicates_and_tenant_isolation(workspace: dict[str, Any]) -> None:
    client = workspace["client"]
    assert client.get("/api/knowledge/documents").status_code == 401
    signin(client)
    assert client.get("/api/staff/me").json()["institution"] == "First synthetic"
    assert (
        client.post("/api/knowledge/documents", files={"files": ("a.txt", b"fees")}).status_code
        == 403
    )
    assert (
        client.post(
            "/api/knowledge/search",
            headers={"X-AdmitFlow-Request": "1", "Origin": "https://attacker.test"},
            json={"query": "fees"},
        ).status_code
        == 403
    )
    word = WordDocument()
    word.add_paragraph("Hostel accommodation is available.")
    data = io.BytesIO()
    word.save(data)
    result = send(
        client,
        [
            ("courses/fees.txt", b"The course fee is INR 30000."),
            ("courses/hostel.docx", data.getvalue()),
            ("courses/annual.pdf", readable_pdf()),
            ("run.exe", b"bad"),
            ("../escape.txt", b"bad"),
        ],
    )
    accepted = result["accepted"]
    assert len(accepted) == 3
    assert {r["error_code"] for r in result["rejected"]} == {"unsafe_path", "unsupported_type"}
    assert all(row["status"] == "queued" for row in accepted)  # Queue outage is durable.
    duplicate = send(client, [("renamed.txt", b"The course fee is INR 30000.")])
    assert duplicate["accepted"][0]["duplicate"] is True
    assert duplicate["accepted"][0]["id"] == accepted[0]["id"]
    first_id = uuid.UUID(accepted[0]["id"])
    tenant = workspace["tenants"][0]

    async def index() -> None:
        async with workspace["sessions"]() as db:
            encrypted = await db.scalar(
                select(KnowledgeUpload.source_enc).where(KnowledgeUpload.id == first_id)
            )
            assert encrypted != b"The course fee is INR 30000."
            assert decrypt_bytes(encrypted) == b"The course fee is INR 30000."
        for row in accepted:
            await processing.process_upload(tenant, uuid.UUID(row["id"]))
        # Duplicate delivery cannot publish duplicate chunks.
        await processing.process_upload(tenant, first_id)
        async with workspace["sessions"]() as db:
            assert await db.scalar(select(func.count()).select_from(DocumentChunk)) == 3

    asyncio.run(index())
    assert all(row["status"] == "ready" for row in client.get("/api/knowledge/documents").json())
    matches = client.post(
        "/api/knowledge/search",
        headers={"X-AdmitFlow-Request": "1"},
        json={"query": "What are the fees?"},
    ).json()["matches"]
    assert {row["source"] for row in matches} == {"courses/fees.txt", "courses/annual.pdf"}
    assert [row["text"] for row in matches] == workspace["ranking_inputs"][-1][::-1]
    signin(client, "second")
    assert client.get("/api/knowledge/documents").json() == []
    assert (
        client.post(
            "/api/knowledge/search", headers={"X-AdmitFlow-Request": "1"}, json={"query": "fees"}
        ).json()["matches"]
        == []
    )
    for method, path in (
        ("delete", f"/api/knowledge/documents/{first_id}"),
        ("post", f"/api/knowledge/documents/{first_id}/retry"),
    ):
        assert (
            getattr(client, method)(path, headers={"X-AdmitFlow-Request": "1"}).status_code == 404
        )
    signin(client, email="agent@example.test")
    assert client.get("/api/knowledge/documents").status_code == 200
    assert (
        client.delete(
            f"/api/knowledge/documents/{first_id}", headers={"X-AdmitFlow-Request": "1"}
        ).status_code
        == 403
    )
    assert (
        client.post(
            "/api/knowledge/documents",
            headers={"X-AdmitFlow-Request": "1"},
            files={"files": ("agent.txt", b"fees")},
        ).status_code
        == 403
    )
    signin(client)
    assert (
        client.delete(
            f"/api/knowledge/documents/{first_id}", headers={"X-AdmitFlow-Request": "1"}
        ).status_code
        == 200
    )
    assert client.post("/api/staff/logout", headers={"X-AdmitFlow-Request": "1"}).status_code == 200
    assert client.get("/api/staff/me").status_code == 401


def test_failure_retry_and_delete_during_indexing(
    workspace: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    client = workspace["client"]
    signin(client)
    tenant = workspace["tenants"][0]
    bad = send(client, [("broken.pdf", b"not a pdf")])["accepted"][0]
    asyncio.run(processing.process_upload(tenant, uuid.UUID(bad["id"])))
    row = next(r for r in client.get("/api/knowledge/documents").json() if r["id"] == bad["id"])
    assert row["status"] == "failed" and row["error_code"] == "invalid_document"
    good = send(client, [("retry.txt", b"Fees are INR 5000 for this module.")])["accepted"][0]
    upload_id = uuid.UUID(good["id"])

    async def unavailable(texts: list[str]) -> list[list[float]]:
        raise ConnectionError("synthetic provider failure, never log source content")

    monkeypatch.setattr(processing, "embed_chunks", unavailable)
    asyncio.run(processing.process_upload(tenant, upload_id))
    response = client.post(
        f"/api/knowledge/documents/{upload_id}/retry", headers={"X-AdmitFlow-Request": "1"}
    )
    assert response.status_code == 200 and response.json()["status"] == "queued"
    monkeypatch.setattr(processing, "embed_chunks", fake_embeddings)
    asyncio.run(processing.process_upload(tenant, upload_id))
    row = next(
        r for r in client.get("/api/knowledge/documents").json() if r["id"] == str(upload_id)
    )
    assert row["status"] == "ready" and row["attempts"] == 2

    pending = send(client, [("deleted.txt", b"Fees for a deleted document.")])["accepted"][0]
    pending_id = uuid.UUID(pending["id"])

    async def delete_while_embedding(texts: list[str]) -> list[list[float]]:
        async with workspace["sessions"]() as db:
            await db.execute(delete(KnowledgeUpload).where(KnowledgeUpload.id == pending_id))
            await db.commit()
        return await fake_embeddings(texts)

    monkeypatch.setattr(processing, "embed_chunks", delete_while_embedding)
    asyncio.run(processing.process_upload(tenant, pending_id))

    async def verify() -> None:
        async with workspace["sessions"]() as db:
            assert await db.get(KnowledgeUpload, pending_id) is None
            assert (
                await db.scalar(
                    select(func.count())
                    .select_from(Document)
                    .where(Document.title == "deleted.txt")
                )
                == 0
            )

    asyncio.run(verify())
    with pytest.raises(RuntimeError, match="uploaded knowledge"):
        command.downgrade(Config("alembic.ini"), "8f4b1c2d3e60")


def test_duplicate_claim_and_abandoned_attempt_recovery(
    workspace: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    client = workspace["client"]
    signin(client)
    tenant = workspace["tenants"][0]
    item = send(client, [("claims.txt", b"Fees for the recovery test.")])["accepted"][0]
    upload_id = uuid.UUID(item["id"])

    async def claims() -> None:
        entered, release = asyncio.Event(), asyncio.Event()
        calls = 0

        async def paused(texts: list[str]) -> list[list[float]]:
            nonlocal calls
            calls += 1
            entered.set()
            await release.wait()
            return await fake_embeddings(texts)

        monkeypatch.setattr(processing, "embed_chunks", paused)
        first = asyncio.create_task(processing.process_upload(tenant, upload_id))
        await asyncio.wait_for(entered.wait(), 5)
        await processing.process_upload(tenant, upload_id)
        release.set()
        await first
        assert calls == 1

    asyncio.run(claims())
    pending = send(client, [("lease.txt", b"Recover this abandoned fee document.")])["accepted"][0]
    pending_id = uuid.UUID(pending["id"])
    publications: list[tuple[str, str]] = []
    from src.tasks.knowledge import ingest_upload

    async def publish(tenant_id: str, record_id: str) -> None:
        publications.append((tenant_id, record_id))

    monkeypatch.setattr(ingest_upload, "kiq", publish)

    async def recover() -> None:
        async with workspace["sessions"]() as db:
            await db.execute(
                update(KnowledgeUpload)
                .where(KnowledgeUpload.id == pending_id)
                .values(
                    status="processing",
                    attempt_id=uuid.uuid4(),
                    updated_at=datetime.now(UTC) - timedelta(minutes=20),
                )
            )
            await db.commit()
        await processing.dispatch_pending()
        assert (str(tenant), str(pending_id)) in publications
        async with workspace["sessions"]() as db:
            row = await db.get(KnowledgeUpload, pending_id)
            assert row.status == "queued" and row.attempt_id is None
        monkeypatch.setattr(processing, "embed_chunks", fake_embeddings)
        await processing.process_upload(tenant, pending_id)

    asyncio.run(recover())


def test_expired_session_rejected(workspace: dict[str, Any]) -> None:
    client = workspace["client"]
    signin(client)

    async def expire() -> None:
        async with workspace["sessions"]() as db:
            await db.execute(
                update(StaffSession).values(expires_at=datetime.now(UTC) - timedelta(seconds=1))
            )
            await db.commit()

    asyncio.run(expire())
    assert client.get("/api/staff/me").status_code == 401
