"""Authenticated institution file/folder uploads, status, retry, deletion and search."""

import hashlib
import uuid
from pathlib import PurePosixPath
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from starlette.datastructures import UploadFile

from src.core.rag import JAILBREAK_PATTERN
from src.core.security import EncryptionKeyNotConfiguredError, encrypt_bytes
from src.core.settings import get_settings
from src.db.audit import write_audit_log
from src.db.models import Document, DocumentChunk, KnowledgeUpload
from src.knowledge.extraction import SUPPORTED, ExtractionError, validate_path
from src.knowledge.processing import dispatch_pending, embed_chunks
from src.knowledge.retrieval import retrieval_query
from src.staff.auth import Db, Staff, require_admin, require_browser_write
from src.staff.throttle import consume_limit

router = APIRouter(prefix="/api/knowledge", tags=["institution knowledge"])


class UploadView(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    filename: str
    relative_path: str
    byte_size: int
    status: str
    error_code: str | None
    chunk_count: int
    attempts: int


async def get_upload(db: Db, staff: Staff, upload_id: uuid.UUID) -> KnowledgeUpload:
    upload = await db.scalar(
        select(KnowledgeUpload)
        .where(KnowledgeUpload.id == upload_id, KnowledgeUpload.tenant_id == staff.tenant_id)
        .with_for_update()
    )
    if upload is None:
        raise HTTPException(404, "Document not found.")
    return upload


@router.get("/documents", response_model=list[UploadView])
async def documents(
    staff: Staff,
    db: Db,
    response: Response,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=200),
) -> list[KnowledgeUpload]:
    response.headers["Cache-Control"] = "no-store"
    return list(
        (
            await db.scalars(
                select(KnowledgeUpload)
                .where(KnowledgeUpload.tenant_id == staff.tenant_id)
                .order_by(KnowledgeUpload.created_at.desc(), KnowledgeUpload.id)
                .offset(offset)
                .limit(limit)
            )
        ).all()
    )


@router.post("/documents", dependencies=[Depends(require_browser_write)])
async def upload_documents(request: Request, staff: Staff, db: Db) -> dict[str, Any]:
    require_admin(staff)
    await consume_limit(f"knowledge-upload:{staff.tenant_id}", 30)
    settings = get_settings()
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, str]] = []
    async with request.form(max_files=settings.upload_batch_files, max_fields=0) as form:
        files = form.getlist("files")
        if not files or any(not isinstance(f, UploadFile) for f in files):
            raise HTTPException(422, "Select at least one document using the files field.")
        total = 0
        for file in files:
            if not isinstance(file, UploadFile):
                continue
            name = file.filename or ""
            try:
                path = validate_path(name)
                filename = PurePosixPath(path).name
                if len(filename) > 255:
                    raise ExtractionError("unsafe_path")
                if PurePosixPath(path).suffix.lower() not in SUPPORTED:
                    raise ExtractionError("unsupported_type")
                data = await file.read(settings.upload_max_bytes + 1)
                if len(data) > settings.upload_max_bytes:
                    raise ExtractionError("file_too_large")
                if not data:
                    raise ExtractionError("no_text")
                total += len(data)
                if total > settings.upload_batch_max_bytes:
                    raise ExtractionError("batch_too_large")
                encrypted = encrypt_bytes(data)
                digest = hashlib.sha256(data).hexdigest()
                result = await db.execute(
                    insert(KnowledgeUpload)
                    .values(
                        id=uuid.uuid4(),
                        tenant_id=staff.tenant_id,
                        uploaded_by=staff.id,
                        filename=filename,
                        relative_path=path,
                        content_hash=digest,
                        source_enc=encrypted,
                        byte_size=len(data),
                        status="queued",
                        chunk_count=0,
                        attempts=0,
                    )
                    .on_conflict_do_nothing(constraint="uq_knowledge_upload_content")
                    .returning(KnowledgeUpload.id)
                )
                created_id = result.scalar_one_or_none()
                record = await db.scalar(
                    select(KnowledgeUpload).where(
                        KnowledgeUpload.tenant_id == staff.tenant_id,
                        KnowledgeUpload.content_hash == digest,
                    )
                )
                if record is None:
                    raise RuntimeError("Upload persistence failed")
                if created_id:
                    await write_audit_log(
                        db,
                        tenant_id=staff.tenant_id,
                        actor=str(staff.id),
                        action="knowledge.upload",
                        details={"upload_id": str(record.id)},
                    )
                await db.commit()
                accepted.append(
                    {
                        **UploadView.model_validate(record).model_dump(mode="json"),
                        "duplicate": created_id is None,
                    }
                )
            except ExtractionError as error:
                rejected.append({"filename": name[:255], "error_code": str(error)})
            except EncryptionKeyNotConfiguredError:
                raise HTTPException(503, "Document encryption is not configured.") from None
    # Enqueue failure must not erase accepted jobs; the recovery loop republishes.
    try:
        await dispatch_pending()
    except Exception:
        pass
    return {"accepted": accepted, "rejected": rejected}


@router.post(
    "/documents/{upload_id}/retry",
    response_model=UploadView,
    dependencies=[Depends(require_browser_write)],
)
async def retry(upload_id: uuid.UUID, staff: Staff, db: Db) -> KnowledgeUpload:
    require_admin(staff)
    await consume_limit(f"knowledge-upload:{staff.tenant_id}", 30)
    record = await get_upload(db, staff, upload_id)
    if record.status != "failed":
        raise HTTPException(409, "Only failed documents can be retried.")
    record.status = "queued"
    record.error_code = None
    record.attempt_id = None
    await write_audit_log(
        db,
        tenant_id=staff.tenant_id,
        actor=str(staff.id),
        action="knowledge.retry",
        details={"upload_id": str(record.id)},
    )
    await db.commit()
    try:
        await dispatch_pending()
    except Exception:
        pass
    return record


@router.delete("/documents/{upload_id}", dependencies=[Depends(require_browser_write)])
async def remove(upload_id: uuid.UUID, staff: Staff, db: Db) -> dict[str, str]:
    require_admin(staff)
    record = await get_upload(db, staff, upload_id)
    document_id = record.document_id
    await db.delete(record)
    await db.flush()
    if document_id:
        await db.execute(
            delete(Document).where(
                Document.id == document_id, Document.tenant_id == staff.tenant_id
            )
        )
    await write_audit_log(
        db,
        tenant_id=staff.tenant_id,
        actor=str(staff.id),
        action="knowledge.delete",
        details={"upload_id": str(upload_id)},
    )
    await db.commit()
    return {"status": "deleted"}


class Search(BaseModel):
    query: str = Field(min_length=2, max_length=1000)


@router.post("/search", dependencies=[Depends(require_browser_write)])
async def search(payload: Search, staff: Staff, db: Db, response: Response) -> dict[str, Any]:
    await consume_limit(f"knowledge-search:{staff.tenant_id}", 60)
    query = payload.query.strip()
    if len(query) < 2:
        raise HTTPException(422, "Enter a question or a few words to search.")
    ready = await db.scalar(
        select(KnowledgeUpload.id)
        .where(KnowledgeUpload.tenant_id == staff.tenant_id, KnowledgeUpload.status == "ready")
        .limit(1)
    )
    if ready is None:
        return {"matches": [], "message": "Upload and index a document before searching."}
    try:
        vector = (await embed_chunks([await retrieval_query(query)]))[0]
    except Exception:
        raise HTTPException(503, "Search is temporarily unavailable. Try again shortly.") from None
    distance = DocumentChunk.embedding.cosine_distance(vector)
    rows = (
        await db.execute(
            select(DocumentChunk, KnowledgeUpload, distance.label("distance"))
            .join(
                KnowledgeUpload,
                (KnowledgeUpload.document_id == DocumentChunk.document_id)
                & (KnowledgeUpload.tenant_id == DocumentChunk.tenant_id),
            )
            .where(
                DocumentChunk.tenant_id == staff.tenant_id,
                KnowledgeUpload.tenant_id == staff.tenant_id,
                KnowledgeUpload.status == "ready",
                DocumentChunk.embedding_model == get_settings().llm_embedding_model,
            )
            .order_by(distance)
            .limit(10)
        )
    ).all()
    matches = []
    for chunk, upload, score in rows:
        similarity = max(0.0, min(1.0, 1 - float(score)))
        if similarity < get_settings().knowledge_min_similarity or JAILBREAK_PATTERN.search(
            chunk.content
        ):
            continue
        matches.append(
            {
                "text": chunk.content,
                "source": upload.relative_path,
                "document_id": str(upload.id),
                "chunk": chunk.chunk_index + 1,
                "similarity": round(similarity, 3),
            }
        )
    await write_audit_log(
        db,
        tenant_id=staff.tenant_id,
        actor=str(staff.id),
        action="knowledge.search",
        details={"matches": len(matches[:5])},
    )
    await db.commit()
    response.headers["Cache-Control"] = "no-store"
    return {
        "matches": matches[:5],
        "message": "" if matches else "No supporting passage found. Try a more specific question.",
    }
