from pathlib import Path

import pytest

from admitflow.adapters.sqlite import Repository
from admitflow.adapters.vector_store import VectorStore
from admitflow.services.admissions import AdmissionsService
from admitflow.services.retrieval import RetrievalService


class UnexpectedRouter:
    async def route(self, text: str) -> str:
        raise AssertionError("Fee questions must bypass the intent model")


@pytest.mark.asyncio
async def test_fee_question_uses_structured_course_price_before_router(tmp_path: Path) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
    )
    lead_id, _ = service.start("123", "student")
    service.select_course(lead_id, "foundations-computing")

    reply = await service.free_text(lead_id, "What is the application fee?", UnexpectedRouter())

    assert "₹500" in reply.text
    assert "fictional demo amount" in reply.text


@pytest.mark.asyncio
async def test_hostel_fee_question_does_not_claim_application_fee(tmp_path: Path) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
    )
    lead_id, _ = service.start("123", "student")

    reply = await service.free_text(
        lead_id, "Is hostel accommodation included in the course fee?", UnexpectedRouter()
    )

    assert "only confirms the application fee" in reply.text
    assert "hostel/accommodation charges or inclusions are not confirmed" in reply.text
    assert "₹" not in reply.text


@pytest.mark.asyncio
async def test_refund_question_does_not_claim_fee_or_call_router(tmp_path: Path) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
    )
    lead_id, _ = service.start("123", "student")

    reply = await service.free_text(
        lead_id, "Can I get a refund for the application fee?", UnexpectedRouter()
    )

    assert "Refunds are not supported in this fictional demo" in reply.text
    assert "₹" not in reply.text


def test_qualification_flow_persists_result_and_rejects_malformed_marks(tmp_path: Path) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
    )
    lead_id, _ = service.start("123", "student")
    service.select_course(lead_id, "foundations-computing")
    service.answer_grade12(lead_id, True)

    invalid = service.answer_marks(lead_id, "one hundred")
    assert "number from 0 to 100" in invalid.text
    assert repository.get_lead(lead_id)["eligible"] is None  # type: ignore[index]

    reply = service.answer_marks(lead_id, "50%")
    lead = repository.get_lead(lead_id)
    assert lead is not None
    assert "meet the sample requirements" in reply.text
    assert lead["marks_percent"] == 50
    assert lead["eligible"] == 1
    assert lead["state"] == "qualified"


def test_browse_path_does_not_force_qualification(tmp_path: Path) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
    )
    lead_id, welcome = service.start("123", "student")

    reply = service.browse(lead_id)

    assert welcome.buttons[-1] == ("Just browsing", "browse")
    assert "fictional sample courses" in reply.text
    assert repository.get_lead(lead_id)["state"] == "browsing"  # type: ignore[index]


def test_grade_twelve_no_stops_before_marks_and_records_ineligibility(tmp_path: Path) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
    )
    lead_id, _ = service.start("123", "student")
    service.select_course(lead_id, "foundations-computing")

    reply = service.answer_grade12(lead_id, False)
    lead = repository.get_lead(lead_id)

    assert lead is not None
    assert "do not need to send marks" in reply.text
    assert lead["eligible"] == 0
    assert lead["state"] == "not_eligible"


def test_marks_are_not_accepted_before_course_and_grade_answers(tmp_path: Path) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
    )
    lead_id, _ = service.start("123", "student")

    reply = service.answer_marks(lead_id, "75")

    assert "select a course and answer" in reply.text
