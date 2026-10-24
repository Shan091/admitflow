"""Document jobs must not occupy the interactive admissions queue."""

from src.tasks.broker import broker, knowledge_broker
from src.tasks.knowledge import ingest_upload


def test_document_jobs_use_a_separate_broker():
    assert knowledge_broker is not broker
    assert ingest_upload.broker is knowledge_broker
    assert ingest_upload.task_name not in broker.get_all_tasks()
