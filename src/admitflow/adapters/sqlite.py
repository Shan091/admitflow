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
                    application_fee_paise INTEGER NOT NULL,
                    education_level TEXT NOT NULL DEFAULT 'undergraduate',
                    field TEXT NOT NULL DEFAULT '',
                    interests TEXT NOT NULL DEFAULT '[]',
                    activities TEXT NOT NULL DEFAULT '[]',
                    prerequisites TEXT NOT NULL DEFAULT '[]',
                    medium TEXT NOT NULL DEFAULT 'English',
                    language_support TEXT NOT NULL DEFAULT '[]'
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
                    lifecycle_stage TEXT NOT NULL DEFAULT 'new',
                    readiness_status TEXT NOT NULL DEFAULT 'unknown',
                    discovery_path TEXT,
                    discovery_step TEXT,
                    education_level TEXT,
                    preferred_language TEXT NOT NULL DEFAULT 'en',
                    handoff_status TEXT NOT NULL DEFAULT 'none',
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
                    search_queries TEXT NOT NULL DEFAULT '[]',
                    answer TEXT NOT NULL,
                    source TEXT NOT NULL,
                    content_hash TEXT NOT NULL,
                    embedding_model TEXT,
                    embedding BLOB,
                    embedding_dimension INTEGER,
                    PRIMARY KEY (tenant_id, id)
                );
                CREATE TABLE IF NOT EXISTS payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tenant_id TEXT NOT NULL REFERENCES institutions(id),
                    lead_id INTEGER NOT NULL UNIQUE REFERENCES leads(id),
                    course_id TEXT NOT NULL REFERENCES courses(id),
                    reference_id TEXT NOT NULL UNIQUE,
                    razorpay_link_id TEXT UNIQUE,
                    amount_paise INTEGER NOT NULL,
                    currency TEXT NOT NULL DEFAULT 'INR',
                    status TEXT NOT NULL CHECK (
                        status IN ('creating', 'created', 'paid', 'failed')
                    ),
                    short_url TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS razorpay_webhook_events (
                    event_id TEXT PRIMARY KEY,
                    received_at TEXT NOT NULL
                );
                """
            )
            chunk_columns = {
                row["name"] for row in connection.execute("PRAGMA table_info(knowledge_chunks)")
            }
            if "search_queries" not in chunk_columns:
                connection.execute(
                    "ALTER TABLE knowledge_chunks ADD COLUMN "
                    "search_queries TEXT NOT NULL DEFAULT '[]'"
                )
            course_columns = {
                row["name"] for row in connection.execute("PRAGMA table_info(courses)")
            }
            course_migrations = {
                "education_level": "TEXT NOT NULL DEFAULT 'undergraduate'",
                "field": "TEXT NOT NULL DEFAULT ''",
                "interests": "TEXT NOT NULL DEFAULT '[]'",
                "activities": "TEXT NOT NULL DEFAULT '[]'",
                "prerequisites": "TEXT NOT NULL DEFAULT '[]'",
                "medium": "TEXT NOT NULL DEFAULT 'English'",
                "language_support": "TEXT NOT NULL DEFAULT '[]'",
                "learning_goals": "TEXT NOT NULL DEFAULT '[]'",
            }
            for column, declaration in course_migrations.items():
                if column not in course_columns:
                    connection.execute(f"ALTER TABLE courses ADD COLUMN {column} {declaration}")
            lead_columns = {row["name"] for row in connection.execute("PRAGMA table_info(leads)")}
            lead_migrations = {
                "lifecycle_stage": "TEXT NOT NULL DEFAULT 'new'",
                "readiness_status": "TEXT NOT NULL DEFAULT 'unknown'",
                "discovery_path": "TEXT",
                "discovery_step": "TEXT",
                "education_level": "TEXT",
                "preferred_language": "TEXT NOT NULL DEFAULT 'en'",
                "handoff_status": "TEXT NOT NULL DEFAULT 'none'",
            }
            for column, declaration in lead_migrations.items():
                if column not in lead_columns:
                    connection.execute(f"ALTER TABLE leads ADD COLUMN {column} {declaration}")
            connection.execute(
                """CREATE TABLE IF NOT EXISTS lead_facts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lead_id INTEGER NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
                    fact_key TEXT NOT NULL,
                    fact_value TEXT NOT NULL,
                    speaker TEXT NOT NULL CHECK (speaker IN ('student', 'parent', 'unknown')),
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE (lead_id, fact_key)
                )"""
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
                    (id, tenant_id, name, description, minimum_marks_percent, application_fee_paise,
                     education_level, field, interests, activities, prerequisites, medium,
                     language_support, learning_goals)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                    tenant_id=excluded.tenant_id, name=excluded.name,
                    description=excluded.description,
                    minimum_marks_percent=excluded.minimum_marks_percent,
                    application_fee_paise=excluded.application_fee_paise,
                    education_level=excluded.education_level, field=excluded.field,
                    interests=excluded.interests, activities=excluded.activities,
                    prerequisites=excluded.prerequisites, medium=excluded.medium,
                    language_support=excluded.language_support,
                    learning_goals=excluded.learning_goals""",
                    (
                        course["id"],
                        catalog["tenant_id"],
                        course["name"],
                        course["description"],
                        course["minimum_marks_percent"],
                        course["application_fee_paise"],
                        course["education_level"],
                        course["field"],
                        json.dumps(course["interests"], ensure_ascii=False),
                        json.dumps(course["activities"], ensure_ascii=False),
                        json.dumps(course["prerequisites"], ensure_ascii=False),
                        course["medium"],
                        json.dumps(course["language_support"], ensure_ascii=False),
                        json.dumps(course["learning_goals"], ensure_ascii=False),
                    ),
                )
            for faq in faqs:
                search_queries = json.dumps(
                    faq.get("search_queries", []), ensure_ascii=False, separators=(",", ":")
                )
                content_hash = hashlib.sha256(
                    json.dumps(
                        [faq["question"], faq.get("search_queries", [])], ensure_ascii=False
                    ).encode()
                ).hexdigest()
                current = connection.execute(
                    "SELECT content_hash FROM knowledge_chunks WHERE tenant_id=? AND id=?",
                    (catalog["tenant_id"], faq["id"]),
                ).fetchone()
                changed = current is None or current["content_hash"] != content_hash
                connection.execute(
                    """INSERT INTO knowledge_chunks
                    (id, tenant_id, title, question, search_queries, answer, source, content_hash,
                     embedding_model, embedding, embedding_dimension)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL, NULL)
                    ON CONFLICT(tenant_id, id) DO UPDATE SET
                    title=excluded.title, question=excluded.question, answer=excluded.answer,
                    search_queries=excluded.search_queries,
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
                        search_queries,
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
                education_level=str(row["education_level"]),
                field=str(row["field"]),
                interests=tuple(json.loads(row["interests"])),
                activities=tuple(json.loads(row["activities"])),
                prerequisites=tuple(json.loads(row["prerequisites"])),
                medium=str(row["medium"]),
                language_support=tuple(json.loads(row["language_support"])),
                learning_goals=tuple(json.loads(row["learning_goals"])),
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
        allowed = {
            "state",
            "selected_course_id",
            "completed_grade12",
            "marks_percent",
            "eligible",
            "lifecycle_stage",
            "readiness_status",
            "discovery_path",
            "discovery_step",
            "education_level",
            "preferred_language",
            "handoff_status",
        }
        if not fields or fields.keys() - allowed:
            raise ValueError("Invalid lead fields")
        values = dict(fields)
        values["updated_at"] = datetime.now(UTC).isoformat()
        assignments = ", ".join(f"{name}=?" for name in values)
        with self._connect() as connection:
            connection.execute(
                f"UPDATE leads SET {assignments} WHERE id=?", (*values.values(), lead_id)
            )

    def save_fact(
        self, lead_id: int, fact_key: str, fact_value: str, speaker: str = "student"
    ) -> None:
        if speaker not in {"student", "parent", "unknown"}:
            raise ValueError("Invalid fact speaker")
        if not fact_key.strip() or not fact_value.strip():
            raise ValueError("Fact key and value must not be empty")
        now = datetime.now(UTC).isoformat()
        with self._connect() as connection:
            connection.execute(
                """INSERT INTO lead_facts
                (lead_id, fact_key, fact_value, speaker, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(lead_id, fact_key) DO UPDATE SET
                fact_value=excluded.fact_value, speaker=excluded.speaker,
                updated_at=excluded.updated_at""",
                (lead_id, fact_key, fact_value, speaker, now, now),
            )

    def list_facts(self, lead_id: int) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM lead_facts WHERE lead_id=? ORDER BY id", (lead_id,)
            ).fetchall()
        return [dict(row) for row in rows]

    def delete_fact(self, lead_id: int, fact_key: str) -> None:
        with self._connect() as connection:
            connection.execute(
                "DELETE FROM lead_facts WHERE lead_id=? AND fact_key=?", (lead_id, fact_key)
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

    def get_or_create_payment_intent(
        self, tenant_id: str, lead_id: int, reference_id: str
    ) -> tuple[dict[str, Any] | None, bool]:
        """Reserve a one-time application payment for a qualified lead."""
        now = datetime.now(UTC).isoformat()
        with self._connect() as connection:
            lead = connection.execute(
                """SELECT selected_course_id, eligible FROM leads
                WHERE id=? AND tenant_id=?""",
                (lead_id, tenant_id),
            ).fetchone()
            if lead is None or lead["eligible"] != 1 or not lead["selected_course_id"]:
                return None, False
            course = connection.execute(
                "SELECT application_fee_paise FROM courses WHERE id=? AND tenant_id=?",
                (lead["selected_course_id"], tenant_id),
            ).fetchone()
            if course is None:
                return None, False
            connection.execute(
                """INSERT OR IGNORE INTO payments
                (tenant_id, lead_id, course_id, reference_id, amount_paise, status,
                 created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, 'creating', ?, ?)""",
                (
                    tenant_id,
                    lead_id,
                    lead["selected_course_id"],
                    reference_id,
                    int(course["application_fee_paise"]),
                    now,
                    now,
                ),
            )
            created = connection.execute("SELECT changes() AS changed").fetchone()["changed"] == 1
            row = connection.execute(
                "SELECT * FROM payments WHERE tenant_id=? AND lead_id=?", (tenant_id, lead_id)
            ).fetchone()
        return (dict(row), created) if row else (None, False)

    def save_payment_link(self, payment_id: int, razorpay_link_id: str, short_url: str) -> None:
        with self._connect() as connection:
            connection.execute(
                """UPDATE payments SET razorpay_link_id=?, short_url=?, status='created',
                updated_at=? WHERE id=? AND status='creating'""",
                (razorpay_link_id, short_url, datetime.now(UTC).isoformat(), payment_id),
            )

    def fail_payment_creation(self, payment_id: int) -> None:
        with self._connect() as connection:
            connection.execute(
                "UPDATE payments SET status='failed', updated_at=? "
                "WHERE id=? AND status='creating'",
                (datetime.now(UTC).isoformat(), payment_id),
            )

    def get_payment_for_lead(self, tenant_id: str, lead_id: int) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM payments WHERE tenant_id=? AND lead_id=?", (tenant_id, lead_id)
            ).fetchone()
        return dict(row) if row else None

    def get_telegram_user_for_payment_link(self, link_id: str) -> str | None:
        with self._connect() as connection:
            row = connection.execute(
                """SELECT leads.telegram_user_id FROM payments
                JOIN leads ON leads.id=payments.lead_id AND leads.tenant_id=payments.tenant_id
                WHERE payments.razorpay_link_id=?""",
                (link_id,),
            ).fetchone()
        return str(row["telegram_user_id"]) if row else None

    def delete_all_demo_data(self) -> None:
        """Clear student, conversation, and payment records while preserving seeded knowledge."""
        with self._connect() as connection:
            connection.execute("DELETE FROM payments")
            connection.execute("DELETE FROM razorpay_webhook_events")
            connection.execute("DELETE FROM messages")
            connection.execute("DELETE FROM lead_facts")
            connection.execute("DELETE FROM leads")

    def delete_lead(self, lead_id: int, tenant_id: str) -> bool:
        """Delete one lead and its local message, discovery, and payment records."""
        with self._connect() as connection:
            exists = connection.execute(
                "SELECT 1 FROM leads WHERE id=? AND tenant_id=?", (lead_id, tenant_id)
            ).fetchone()
            if exists is None:
                return False
            connection.execute("DELETE FROM messages WHERE lead_id=?", (lead_id,))
            connection.execute("DELETE FROM lead_facts WHERE lead_id=?", (lead_id,))
            connection.execute("DELETE FROM payments WHERE lead_id=?", (lead_id,))
            connection.execute("DELETE FROM leads WHERE id=? AND tenant_id=?", (lead_id, tenant_id))
        return True

    def apply_razorpay_paid_event(self, event_id: str, event: dict[str, Any]) -> str:
        """Apply a validated event once, only when link, reference, and full amount match."""
        payload = event.get("payload")
        link_wrap = payload.get("payment_link") if isinstance(payload, dict) else None
        link = link_wrap.get("entity") if isinstance(link_wrap, dict) else None
        if not isinstance(link, dict) or link.get("status") != "paid":
            return "ignored"
        link_id = link.get("id")
        reference_id = link.get("reference_id")
        amount = link.get("amount")
        amount_paid = link.get("amount_paid")
        currency = link.get("currency")
        now = datetime.now(UTC).isoformat()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM payments WHERE razorpay_link_id=?", (link_id,)
            ).fetchone()
            if (
                row is None
                or row["reference_id"] != reference_id
                or row["amount_paise"] != amount
                or row["amount_paise"] != amount_paid
                or row["currency"] != currency
            ):
                return "ignored"
            inserted = connection.execute(
                "INSERT OR IGNORE INTO razorpay_webhook_events(event_id, received_at) "
                "VALUES (?, ?)",
                (event_id, now),
            ).rowcount
            if inserted == 0:
                return "duplicate"
            connection.execute(
                "UPDATE payments SET status='paid', updated_at=? WHERE id=?",
                (now, row["id"]),
            )
            connection.execute(
                "UPDATE leads SET lifecycle_stage='under_review', updated_at=? "
                "WHERE id=? AND tenant_id=?",
                (now, row["lead_id"], row["tenant_id"]),
            )
        return "applied"

    def get_unembedded_faqs(self, tenant_id: str, model: str) -> list[dict[str, str]]:
        with self._connect() as connection:
            rows = connection.execute(
                """SELECT id, question, search_queries FROM knowledge_chunks
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
