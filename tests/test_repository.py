import sqlite3
from pathlib import Path

from admitflow.adapters.sqlite import Repository


def make_repository(tmp_path: Path) -> Repository:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    return repository


def test_catalog_seeding_is_idempotent_and_fees_are_structured(tmp_path: Path) -> None:
    repository = make_repository(tmp_path)
    before = repository.list_courses(repository.tenant_id)
    repository.seed_catalog()
    after = repository.list_courses(repository.tenant_id)
    assert before == after
    assert repository.get_fee_paise(repository.tenant_id, "foundations-computing") == 50000
    assert {course.education_level for course in after} >= {
        "vocational_certificate",
        "diploma",
        "undergraduate",
        "postgraduate",
    }
    assert all(
        course.field
        and course.prerequisites
        and course.medium
        and course.learning_goals
        and course.delivery_modes
        for course in after
    )


def test_catalog_has_broad_fictional_options_with_complete_sample_facts(
    tmp_path: Path,
) -> None:
    repository = make_repository(tmp_path)
    courses = repository.list_courses(repository.tenant_id)

    assert len(courses) == 50
    assert len({course.id for course in courses}) == len(courses)
    assert {course.education_level for course in courses} == {
        "vocational_certificate",
        "diploma",
        "undergraduate",
        "postgraduate",
    }
    by_field = {course.field for course in courses}
    assert by_field == {
        "tech/data",
        "business/accounting",
        "design/media",
        "hospitality/tourism",
        "vocational-skills",
    }
    assert all(sum(course.field == field for course in courses) == 10 for field in by_field)
    assert all(
        set(course.language_support)
        <= {
            "English support sessions",
            "Hindi discussion support",
            "Malayalam discussion support",
        }
        for course in courses
    )
    assert all(
        course.description
        and "fictional" in course.description.casefold()
        and course.interests
        and course.activities
        and course.prerequisites
        and course.medium
        and course.delivery_modes
        and course.learning_goals
        and course.application_fee_paise > 0
        for course in courses
    )


def test_lead_facts_preserve_attribution_and_update_in_place(tmp_path: Path) -> None:
    repository = make_repository(tmp_path)
    lead_id = repository.upsert_lead(repository.tenant_id, "123", "student")
    repository.save_fact(lead_id, "interest_field", "tech/data", "student")
    repository.save_fact(lead_id, "interest_field", "design/media", "parent")

    facts = repository.list_facts(lead_id)

    assert len(facts) == 1
    assert facts[0]["fact_value"] == "design/media"
    assert facts[0]["speaker"] == "parent"


def test_initialize_adds_discovery_columns_without_replacing_existing_rows(tmp_path: Path) -> None:
    path = tmp_path / "legacy.sqlite3"
    with sqlite3.connect(path) as connection:
        connection.executescript(
            """CREATE TABLE institutions (id TEXT PRIMARY KEY, name TEXT NOT NULL);
            CREATE TABLE courses (
                id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL, name TEXT NOT NULL,
                description TEXT NOT NULL, minimum_marks_percent REAL NOT NULL,
                application_fee_paise INTEGER NOT NULL
            );
            CREATE TABLE leads (
                id INTEGER PRIMARY KEY, tenant_id TEXT NOT NULL, telegram_user_id TEXT NOT NULL,
                telegram_username TEXT, state TEXT NOT NULL DEFAULT 'browsing',
                selected_course_id TEXT, completed_grade12 INTEGER, marks_percent REAL,
                eligible INTEGER, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
            );
            CREATE TABLE messages (
                id INTEGER PRIMARY KEY, lead_id INTEGER NOT NULL, direction TEXT NOT NULL,
                body TEXT NOT NULL, telegram_update_id INTEGER UNIQUE, created_at TEXT NOT NULL
            );
            CREATE TABLE payments (
                id INTEGER PRIMARY KEY, tenant_id TEXT NOT NULL, lead_id INTEGER NOT NULL UNIQUE,
                course_id TEXT NOT NULL, reference_id TEXT NOT NULL UNIQUE, razorpay_link_id TEXT,
                amount_paise INTEGER NOT NULL, currency TEXT NOT NULL, status TEXT NOT NULL,
                short_url TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
            );
            CREATE TABLE razorpay_webhook_events (
                event_id TEXT PRIMARY KEY, received_at TEXT NOT NULL
            );
            INSERT INTO courses VALUES
            ('legacy-course', 'demo', 'Legacy Course', 'sample', 50, 100);
            INSERT INTO institutions VALUES ('demo', 'Legacy Demo');
            INSERT INTO leads (id, tenant_id, telegram_user_id, created_at, updated_at)
            VALUES (7, 'demo', '123', 'old', 'old');
            INSERT INTO messages VALUES (8, 7, 'inbound', 'hello', 90, 'old');
            INSERT INTO payments VALUES
            (9, 'demo', 7, 'legacy-course', 'AF-legacy', NULL, 100, 'INR',
             'created', NULL, 'old', 'old');"""
        )

    repository = Repository(path)
    repository.initialize()
    lead = repository.get_lead(7)

    assert lead is not None
    assert lead["telegram_user_id"] == "123"
    assert lead["lifecycle_stage"] == "new"
    assert repository.list_messages(7)[0]["body"] == "hello"
    assert repository.get_payment_for_lead("demo", 7)["reference_id"] == "AF-legacy"  # type: ignore[index]
    with sqlite3.connect(path) as connection:
        columns = {row[1] for row in connection.execute("PRAGMA table_info(courses)")}
    assert "education_level" in columns
    assert "learning_goals" in columns
    assert "delivery_modes" in columns


def test_lead_and_messages_persist_and_duplicate_update_is_ignored(tmp_path: Path) -> None:
    repository = make_repository(tmp_path)
    lead_id = repository.upsert_lead(repository.tenant_id, "123", "student")
    assert repository.upsert_lead(repository.tenant_id, "123", "student") == lead_id
    repository.add_message(lead_id, "inbound", "/start", 77)
    repository.add_message(lead_id, "inbound", "/start", 77)
    assert len(repository.list_messages(lead_id)) == 1
    assert repository.get_lead(lead_id)["telegram_username"] == "student"  # type: ignore[index]


def test_embedding_is_reused_for_same_model_and_reembedded_for_new_model(
    tmp_path: Path,
) -> None:
    repository = make_repository(tmp_path)
    pending = repository.get_unembedded_faqs(repository.tenant_id, "model-v1")
    chunk_id = pending[0]["id"]
    repository.save_embedding(repository.tenant_id, chunk_id, "model-v1", b"vector", 1)
    assert chunk_id not in {
        item["id"] for item in repository.get_unembedded_faqs(repository.tenant_id, "model-v1")
    }

    # Re-seeding unchanged content must retain the saved embedding.
    repository.seed_catalog()
    assert chunk_id not in {
        item["id"] for item in repository.get_unembedded_faqs(repository.tenant_id, "model-v1")
    }
    assert chunk_id in {
        item["id"] for item in repository.get_unembedded_faqs(repository.tenant_id, "model-v2")
    }

    with sqlite3.connect(repository.database_path) as connection:
        connection.execute(
            "UPDATE knowledge_chunks SET content_hash='outdated' WHERE tenant_id=? AND id=?",
            (repository.tenant_id, chunk_id),
        )
    repository.seed_catalog()
    assert chunk_id in {
        item["id"] for item in repository.get_unembedded_faqs(repository.tenant_id, "model-v1")
    }
