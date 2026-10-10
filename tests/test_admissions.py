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
async def test_hostel_availability_is_handed_to_staff_when_not_confirmed(tmp_path: Path) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
    )
    lead_id, _ = service.start("123", "student")

    reply = await service.free_text(lead_id, "Is hostel accommodation available?", None)

    assert "actual availability" in reply.text
    assert "Live contact and response-time details are not configured" in reply.text
    assert repository.get_lead(lead_id)["handoff_status"] == "pending"  # type: ignore[index]


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


@pytest.mark.asyncio
async def test_language_barrier_uses_seeded_course_facts_and_hands_off_unknown_rules(
    tmp_path: Path,
) -> None:
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

    reply = await service.free_text(lead_id, "I am worried my English is not good enough", None)
    lead = repository.get_lead(lead_id)

    assert "listed medium" in reply.text
    assert "does not confirm a required proficiency level" in reply.text
    assert lead is not None and lead["handoff_status"] == "pending"


@pytest.mark.asyncio
async def test_student_data_deletion_request_is_handed_to_staff_not_deleted(
    tmp_path: Path,
) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
    )
    lead_id, _ = service.start("123", "student")
    repository.add_message(lead_id, "inbound", "please keep my chat", 901)

    reply = await service.free_text(lead_id, "Please delete my data", None)

    assert "Staff must review and perform the deletion" in reply.text
    assert repository.get_lead(lead_id) is not None
    assert repository.list_messages(lead_id)
    assert repository.get_lead(lead_id)["handoff_status"] == "pending"  # type: ignore[index]


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
    assert lead["lifecycle_stage"] == "admission_ready"
    assert lead["readiness_status"] == "considering"


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

    assert ("Just browsing / ask a question", "path:browse") in welcome.buttons
    assert "fictional sample courses" in reply.text
    assert repository.get_lead(lead_id)["state"] == "browsing"  # type: ignore[index]


def test_known_field_recommends_only_complete_catalog_courses_and_persists_path(
    tmp_path: Path,
) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
    )
    lead_id, welcome = service.start("123", "student")

    assert {data for _, data in welcome.buttons} >= {
        "path:course",
        "path:field",
        "path:explore",
        "path:browse",
        "language:menu",
    }
    service.begin_path(lead_id, "field")
    level_reply = service.recommend_field(lead_id, "tech/data")
    assert any(data == "level:any" for _, data in level_reply.buttons)
    activity_reply = service.choose_level(lead_id, "any")
    assert any(data.startswith("activity:") for _, data in activity_reply.buttons)
    reply = service.choose_activity(lead_id, "skip")

    lead = repository.get_lead(lead_id)
    facts = repository.list_facts(lead_id)
    assert lead is not None and lead["lifecycle_stage"] == "discovering"
    assert lead["discovery_path"] == "field"
    assert "Matches your interest in tech/data" in reply.text
    assert all(data.startswith("course:") for _, data in reply.buttons)
    assert any(fact["fact_key"] == "interest_field_student" for fact in facts)


def test_discovery_pause_and_resume_restore_the_pending_question(tmp_path: Path) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
    )
    lead_id, _ = service.start("123", "student")
    service.begin_path(lead_id, "explore")
    service.recommend_field(lead_id, "tech/data")
    service.pause_discovery(lead_id)
    paused = repository.get_lead(lead_id)

    resumed = service.resume_discovery(lead_id)

    assert paused is not None and paused["lifecycle_stage"] == "paused"
    assert "study level" in resumed.text
    assert repository.get_lead(lead_id)["lifecycle_stage"] == "discovering"  # type: ignore[index]


def test_parent_preference_is_attributed_and_waits_for_student_interest(tmp_path: Path) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
    )
    lead_id, _ = service.start("123", "parent")
    service.choose_speaker(lead_id, "parent")
    service.begin_path(lead_id, "field")
    parent_reply = service.recommend_field(lead_id, "business/accounting")
    service.choose_speaker(lead_id, "student")
    service.begin_path(lead_id, "field")
    student_reply = service.recommend_field(lead_id, "tech/data")

    facts = repository.list_facts(lead_id)
    assert "parent's preference" in parent_reply.text
    assert not parent_reply.buttons or parent_reply.buttons[0][1] == "speaker:student"
    assert any(
        fact["fact_key"] == "interest_field_parent" and fact["speaker"] == "parent"
        for fact in facts
    )
    assert any(
        fact["fact_key"] == "interest_field_student" and fact["speaker"] == "student"
        for fact in facts
    )
    assert student_reply.buttons


def test_parent_course_suggestion_requires_student_confirmation(tmp_path: Path) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
    )
    lead_id, _ = service.start("123", "parent")
    service.choose_speaker(lead_id, "parent")

    parent_reply = service.select_course(lead_id, "foundations-computing")
    assert repository.get_lead(lead_id)["selected_course_id"] is None  # type: ignore[index]
    assert any(data == "course:confirm:foundations-computing" for _, data in parent_reply.buttons)

    student_reply = service.confirm_parent_course(lead_id, "foundations-computing")

    lead = repository.get_lead(lead_id)
    facts = repository.list_facts(lead_id)
    assert lead is not None and lead["selected_course_id"] == "foundations-computing"
    assert "Have you completed Grade 12?" in student_reply.text
    assert any(fact["fact_key"] == "course_choice_parent" for fact in facts)
    assert any(fact["fact_key"] == "course_choice_student" for fact in facts)


@pytest.mark.parametrize(
    ("field", "level", "expected_course"),
    [
        ("tech/data", "postgraduate", "data-science-masters"),
        ("business/accounting", "undergraduate", "business-management-bachelors"),
        ("design/media", "diploma", "digital-design-diploma"),
        ("hospitality/tourism", "diploma", "hospitality-diploma"),
        ("vocational-skills", "vocational_certificate", "food-service-skills"),
    ],
)
def test_fixed_catalog_evaluation_matrix_returns_expected_complete_course(
    tmp_path: Path, field: str, level: str, expected_course: str
) -> None:
    repository = Repository(tmp_path / f"{expected_course}.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
    )
    lead_id, _ = service.start("123", "student")
    service.begin_path(lead_id, "explore")
    service.recommend_field(lead_id, field)
    service.choose_level(lead_id, level)
    result = service.choose_activity(lead_id, "skip")

    assert any(data == f"course:{expected_course}" for _, data in result.buttons)


def test_unknown_field_creates_handoff_instead_of_inventing_course(tmp_path: Path) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
    )
    lead_id, _ = service.start("123", "student")

    reply = service.recommend_field(lead_id, "aerospace medicine")

    assert "fictional catalog" in reply.text
    assert repository.get_lead(lead_id)["handoff_status"] == "pending"  # type: ignore[index]


def test_non_undergraduate_selection_does_not_ask_grade12_or_offer_eligibility(
    tmp_path: Path,
) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
    )
    lead_id, _ = service.start("123", "student")

    reply = service.select_course(lead_id, "hospitality-diploma")
    lead = repository.get_lead(lead_id)

    assert "Completed Grade 10 or equivalent" in reply.text
    assert "Live contact and response-time details are not configured" in reply.text
    assert lead is not None
    assert lead["state"] == "browsing"
    assert lead["eligible"] is None
    assert lead["handoff_status"] == "pending"


def test_language_switch_and_staff_handoff_are_persisted_truthfully(tmp_path: Path) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
    )
    lead_id, _ = service.start("123", "student")
    language_reply = service.choose_language(lead_id, "ml")
    handoff_reply = service.handoff(lead_id, "no matching sample offering")
    lead = repository.get_lead(lead_id)

    assert language_reply.text
    assert lead is not None
    assert lead["preferred_language"] == "ml"
    assert lead["lifecycle_stage"] == "handed_off"
    assert lead["handoff_status"] == "pending"
    assert "not configured" in handoff_reply.text


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
