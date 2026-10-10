"""SQLite schema, seed loading, and repositories for the local demo."""

import hashlib
import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from admitflow.domain.models import Course


class Repository:
    """Small synchronous SQLite repository; connections are short-lived per operation."""

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path

    def _connect(self) -> sqlite3.Connection:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.database_path, timeout=10)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self) -> None:
        """Create the demo schema idempotently."""
        with self._connect() as connection:
            connection.executescript(
                """
                PRAGMA journal_mode=WAL;
                CREATE TABLE IF NOT EXISTS institutions (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS courses (
                    id TEXT PRIMARY KEY,
                    tenant_id TEXT NOT NULL REFERENCES institutions(id),
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    minimum_marks_percent REAL NOT NULL,
                    application_fee_paise INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tenant_id TEXT NOT NULL REFERENCES institutions(id),
                    telegram_user_id TEXT NOT NULL,
                    telegram_username TEXT,
                    state TEXT NOT NULL DEFAULT 'browsing',
                    selected_course_id TEXT REFERENCES courses(id),
                    completed_grade12 INTEGER,
                    marks_percent REAL,
                    eligible INTEGER,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE (tenant_id, telegram_user_id)
                );
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lead_id INTEGER NOT NULL REFERENCES leads(id),
                    direction TEXT NOT NULL CHECK (direction IN ('inbound', 'outbound')),
                    body TEXT NOT NULL,
                    telegram_update_id INTEGER UNIQUE,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS knowledge_chunks (
                    id TEXT NOT NULL,
                    tenant_id TEXT NOT NULL REFERENCES institutions(id),
                    title TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    source TEXT NOT NULL,
                    content_hash TEXT NOT NULL,
                    embedding_model TEXT,
                    embedding BLOB,
                    embedding_dimension INTEGER,
                    PRIMARY KEY (tenant_id, id)
                );
                """
            )

    def seed_catalog(self) -> None:
        """Upsert clearly fictional catalog and FAQ content from package seed files."""
        data_dir = Path(__file__).resolve().parents[1] / "seed" / "data"
        catalog = json.loads((data_dir / "demo.json").read_text(encoding="utf-8"))
        faqs = json.loads((data_dir / "faqs.json").read_text(encoding="utf-8"))
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO institutions(id, name) VALUES (?, ?) "
                "ON CONFLICT(id) DO UPDATE SET name=excluded.name",
                (catalog["tenant_id"], catalog["name"]),
            )
            for course in catalog["courses"]:
                connection.execute(
                    """INSERT INTO courses
                    (id, tenant_id, name, description, minimum_marks_percent, application_fee_paise)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                    tenant_id=excluded.tenant_id, name=excluded.name,
                    description=excluded.description,
                    minimum_marks_percent=excluded.minimum_marks_percent,
                    application_fee_paise=excluded.application_fee_paise""",
                    (
                        course["id"],
                        catalog["tenant_id"],
                        course["name"],
                        course["description"],
                        course["minimum_marks_percent"],
                        course["application_fee_paise"],
                    ),
                )
            for faq in faqs:
                content_hash = hashlib.sha256(
                    f"{faq['title']}\n{faq['question']}\n{faq['answer']}".encode()
                ).hexdigest()
                current = connection.execute(
                    "SELECT content_hash FROM knowledge_chunks WHERE tenant_id=? AND id=?",
                    (catalog["tenant_id"], faq["id"]),
                ).fetchone()
                changed = current is None or current["content_hash"] != content_hash
                connection.execute(
                    """INSERT INTO knowledge_chunks
                    (id, tenant_id, title, question, answer, source, content_hash,
                     embedding_model, embedding, embedding_dimension)
                    VALUES (?, ?, ?, ?, ?, ?, ?, NULL, NULL, NULL)
                    ON CONFLICT(tenant_id, id) DO UPDATE SET
                    title=excluded.title, question=excluded.question, answer=excluded.answer,
                    source=excluded.source, content_hash=excluded.content_hash,
                    embedding_model=CASE WHEN ? THEN NULL ELSE knowledge_chunks.embedding_model END,
                    embedding=CASE WHEN ? THEN NULL ELSE knowledge_chunks.embedding END,
                    embedding_dimension=CASE WHEN ? THEN NULL
                    ELSE knowledge_chunks.embedding_dimension END""",
                    (
                        faq["id"],
                        catalog["tenant_id"],
                        faq["title"],
                        faq["question"],
                        faq["answer"],
                        faq["source"],
                        content_hash,
                        changed,
                        changed,
                        changed,
                    ),
                )
        self.tenant_id = str(catalog["tenant_id"])

    @property
    def tenant_id(self) -> str:
        if not hasattr(self, "_tenant_id"):
            raise RuntimeError("seed_catalog must be called before reading the demo tenant")
        return self._tenant_id

    @tenant_id.setter
    def tenant_id(self, value: str) -> None:
        self._tenant_id = value

    def list_courses(self, tenant_id: str) -> list[Course]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM courses WHERE tenant_id=? ORDER BY name", (tenant_id,)
            ).fetchall()
        return [
            Course(
                id=row["id"],
                tenant_id=row["tenant_id"],
                name=row["name"],
                description=row["description"],
                minimum_marks_percent=float(row["minimum_marks_percent"]),
                application_fee_paise=int(row["application_fee_paise"]),
            )
            for row in rows
        ]

    def get_course(self, tenant_id: str, course_id: str) -> Course | None:
        return next(
            (course for course in self.list_courses(tenant_id) if course.id == course_id), None
        )

    def get_fee_paise(self, tenant_id: str, course_id: str) -> int | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT application_fee_paise FROM courses WHERE tenant_id=? AND id=?",
                (tenant_id, course_id),
            ).fetchone()
        return int(row["application_fee_paise"]) if row else None

    def upsert_lead(self, tenant_id: str, telegram_user_id: str, username: str | None) -> int:
        now = datetime.now(UTC).isoformat()
        with self._connect() as connection:
            connection.execute(
                """INSERT INTO leads
                (tenant_id, telegram_user_id, telegram_username, state, created_at, updated_at)
                VALUES (?, ?, ?, 'browsing', ?, ?)
                ON CONFLICT(tenant_id, telegram_user_id) DO UPDATE SET
                telegram_username=excluded.telegram_username, updated_at=excluded.updated_at""",
                (tenant_id, telegram_user_id, username, now, now),
            )
            row = connection.execute(
                "SELECT id FROM leads WHERE tenant_id=? AND telegram_user_id=?",
                (tenant_id, telegram_user_id),
            ).fetchone()
        if row is None:
            raise RuntimeError("Failed to create or load lead")
        return int(row["id"])

    def get_lead(self, lead_id: int) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                """SELECT leads.*, courses.name AS course_name
                FROM leads LEFT JOIN courses ON courses.id=leads.selected_course_id
                WHERE leads.id=?""",
                (lead_id,),
            ).fetchone()
        return dict(row) if row else None

    def update_lead(self, lead_id: int, **fields: object) -> None:
        allowed = {"state", "selected_course_id", "completed_grade12", "marks_percent", "eligible"}
        if not fields or fields.keys() - allowed:
            raise ValueError("Invalid lead fields")
        values = dict(fields)
        values["updated_at"] = datetime.now(UTC).isoformat()
        assignments = ", ".join(f"{name}=?" for name in values)
        with self._connect() as connection:
            connection.execute(
                f"UPDATE leads SET {assignments} WHERE id=?", (*values.values(), lead_id)
            )

    def add_message(
        self,
        lead_id: int,
        direction: str,
        body: str,
        telegram_update_id: int | None = None,
    ) -> None:
        if direction not in {"inbound", "outbound"}:
            raise ValueError("Invalid message direction")
        with self._connect() as connection:
            connection.execute(
                """INSERT OR IGNORE INTO messages
                (lead_id, direction, body, telegram_update_id, created_at)
                VALUES (?, ?, ?, ?, ?)""",
                (lead_id, direction, body, telegram_update_id, datetime.now(UTC).isoformat()),
            )

    def list_leads(self, tenant_id: str) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """SELECT leads.*, courses.name AS course_name
                FROM leads LEFT JOIN courses ON courses.id=leads.selected_course_id
                WHERE leads.tenant_id=? ORDER BY leads.updated_at DESC""",
                (tenant_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def list_messages(self, lead_id: int) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM messages WHERE lead_id=? ORDER BY id", (lead_id,)
            ).fetchall()
        return [dict(row) for row in rows]

    def get_unembedded_faqs(self, tenant_id: str, model: str) -> list[dict[str, str]]:
        with self._connect() as connection:
            rows = connection.execute(
                """SELECT id, question, answer, title FROM knowledge_chunks
                WHERE tenant_id=? AND (embedding IS NULL OR embedding_model != ?)""",
                (tenant_id, model),
            ).fetchall()
        return [dict(row) for row in rows]

    def save_embedding(
        self, tenant_id: str, chunk_id: str, model: str, vector: bytes, dimension: int
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """UPDATE knowledge_chunks SET embedding_model=?, embedding=?,
                embedding_dimension=? WHERE tenant_id=? AND id=?""",
                (model, vector, dimension, tenant_id, chunk_id),
            )

    def ranked_chunks(self, tenant_id: str, model: str) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """SELECT id, title, question, answer, source, embedding, embedding_dimension
                FROM knowledge_chunks
                WHERE tenant_id=? AND embedding IS NOT NULL AND embedding_model=?""",
                (tenant_id, model),
            ).fetchall()
        return [dict(row) for row in rows]
