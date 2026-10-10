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
