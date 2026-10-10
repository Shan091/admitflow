from dataclasses import replace
from pathlib import Path

import pytest

from admitflow.adapters.sqlite import Repository
from admitflow.adapters.vector_store import VectorStore
from admitflow.domain.models import Course, DiscoveryTurn
from admitflow.services.admissions import AdmissionsService, Reply
from admitflow.services.retrieval import RetrievalService


class UnexpectedRouter:
    async def route(self, text: str) -> str:
        raise AssertionError("Fee questions must bypass the intent model")


class UnexpectedEmbedder:
    async def embed(self, texts: list[str]) -> list[list[float]]:
        raise AssertionError("Opted-out messages must not be sent for embeddings")


class FakeDiscoveryInterpreter:
    def __init__(self, turn: DiscoveryTurn) -> None:
        self.turn = turn
        self.calls: list[tuple[str, list[str]]] = []

    async def extract_discovery(self, text: str, courses: list[Course]) -> DiscoveryTurn:
        self.calls.append((text, [course.id for course in courses]))
        return self.turn


class FailingDiscoveryInterpreter:
    async def extract_discovery(self, text: str, courses: list[Course]) -> DiscoveryTurn:
        raise RuntimeError("synthetic extraction failure")


async def _skip_optional_goal_prompt(
    service: AdmissionsService, lead_id: int, reply: Reply
) -> Reply:
    if any(data == "guidance:goal:skip" for _, data in reply.buttons):
        return await service.choose_guidance_goal(lead_id, None)
    return reply


@pytest.mark.parametrize(
    ("language", "disclosure_phrase", "off_phrase"),
    [
        ("hi", "OpenAI को भेजे जाते हैं", "OpenAI प्रोसेसिंग बंद"),
        ("ml", "OpenAI-ലേക്ക് അയയ്ക്കുകയും", "OpenAI പ്രോസസ്സിംഗ് ഓഫ്"),
        ("hinglish", "OpenAI ko bheje", "OpenAI processing band"),
    ],
)
def test_language_switch_localizes_ai_disclosure_and_opt_out_copy(
    tmp_path: Path,
    language: str,
    disclosure_phrase: str,
    off_phrase: str,
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

    discovery = service.choose_language(lead_id, language)

    assert disclosure_phrase in discovery.text
    assert any(data == "path:explore" for _, data in discovery.buttons)
    tap_only = service.set_ai_processing_enabled(lead_id, False)
    assert off_phrase in tap_only.text
    assert service.preferred_language(lead_id) == language


def test_language_switch_updates_disclosure_and_discovery_prompt(tmp_path: Path) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
    )
    lead_id, _ = service.start("123", "student")
    prompt = service.choose_language(lead_id, "hi")

    assert "आप क्या पढ़ने" in prompt.text
    assert "अंग्रेज़ी में" in prompt.text


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
async def test_discovery_is_enabled_by_default_and_opt_out_keeps_tap_only_mode(
    tmp_path: Path,
) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(
            repository, VectorStore(repository), UnexpectedEmbedder(), "fake", 0.72, 0.05
        ),
    )
    lead_id, welcome_prompt = service.start("123", "student")

    assert "OpenAI" in welcome_prompt.text
    assert "demo text only" in welcome_prompt.text.casefold()
    assert any(data == "path:explore" for _, data in welcome_prompt.buttons)
    assert service.ai_processing_enabled(lead_id)

    service.set_ai_processing_enabled(lead_id, False)
    reply = await service.free_text(lead_id, "I like technology and data", UnexpectedRouter())

    assert "buttons" in reply.text.casefold()
    assert "technology and data" not in reply.text
    consent = next(
        fact
        for fact in repository.list_facts(lead_id)
        if fact["fact_key"] == "openai_processing_enabled"
    )
    assert consent["fact_value"] == "no"


@pytest.mark.asyncio
async def test_openai_opt_out_takes_priority_while_waiting_for_marks(tmp_path: Path) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
    )
    lead_id, _ = service.start("123", "student")
    service.set_ai_processing_enabled(lead_id, True)
    repository.update_lead(lead_id, state="awaiting_marks")

    reply = await service.free_text(lead_id, "Don't send to OpenAI", UnexpectedRouter())

    assert repository.get_lead(lead_id)["state"] == "awaiting_marks"  # type: ignore[index]
    consent = next(
        fact
        for fact in repository.list_facts(lead_id)
        if fact["fact_key"] == "openai_processing_enabled"
    )
    assert consent["fact_value"] == "no"
    assert "buttons" in reply.text.casefold()


def test_openai_preference_can_be_disabled_and_reenabled(tmp_path: Path) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
    )
    lead_id, _ = service.start("123", "student")

    prompt = service.set_ai_processing_enabled(lead_id, True)
    assert "what do you enjoy" in prompt.text.casefold() or "already know" in prompt.text.casefold()
    assert any(data == "path:course" for _, data in prompt.buttons)
    assert any(data == "path:explore" for _, data in prompt.buttons)

    revoked = service.set_ai_processing_enabled(lead_id, False)
    assert "buttons" in revoked.text.casefold() or "tap" in revoked.text.casefold()
    consent = next(
        fact
        for fact in repository.list_facts(lead_id)
        if fact["fact_key"] == "openai_processing_enabled"
    )
    assert consent["fact_value"] == "no"


@pytest.mark.asyncio
async def test_student_can_describe_multiple_facts_without_consent_step(
    tmp_path: Path,
) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    interpreter = FakeDiscoveryInterpreter(
        DiscoveryTurn(
            intent="discovery",
            course_id=None,
            fields=("tech/data",),
            education_level="diploma",
            interests=("data",),
            activities=("making charts",),
            unsure=False,
            correct_previous=False,
        )
    )
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
        interpreter,
    )
    lead_id, _ = service.start("123", "student")
    service.choose_speaker(lead_id, "student")

    reply = await service.free_text(lead_id, "I enjoy charts and want a diploma in data", None)

    assert len(interpreter.calls) == 1
    assert "Did I get that right" in reply.text
    pending = next(data for _, data in reply.buttons if data.startswith("guidance:confirm:"))
    reply = await service.confirm_guidance(lead_id, pending.removeprefix("guidance:confirm:"))
    assert "Applied Data Analytics Diploma" in reply.text
    assert "\\n" not in reply.text
    assert "courses:\n" in reply.text
    facts = repository.list_facts(lead_id)
    assert any(
        fact["fact_key"] == "interest_field_student" and fact["fact_value"] == "tech/data"
        for fact in facts
    )
    assert any(
        fact["fact_key"] == "education_level_student" and fact["fact_value"] == "diploma"
        for fact in facts
    )

    interpreter.turn = DiscoveryTurn(
        intent="discovery",
        course_id=None,
        fields=("design/media",),
        education_level=None,
        interests=("design",),
        activities=("making visuals",),
        unsure=False,
        correct_previous=False,
    )
    await service.free_text(lead_id, "I also like design and making visuals", None)
    facts = repository.list_facts(lead_id)
    assert any(
        fact["fact_key"] == "interest_fields_student"
        and set(str(fact["fact_value"]).split("|")) == {"tech/data", "design/media"}
        for fact in facts
    )

    interpreter.turn = DiscoveryTurn(
        intent="discovery",
        course_id=None,
        fields=("design/media",),
        education_level="any",
        interests=("design",),
        activities=("making visuals",),
        unsure=False,
        correct_previous=True,
    )
    await service.free_text(lead_id, "Actually, I changed my mind: design/media", None)
    facts = repository.list_facts(lead_id)
    assert any(
        fact["fact_key"] == "interest_fields_student" and fact["fact_value"] == "design/media"
        for fact in facts
    )
    assert not any(fact["fact_key"] == "education_level_student" for fact in facts)


@pytest.mark.asyncio
async def test_broad_match_gets_optional_goal_question_and_goal_filters_results(
    tmp_path: Path,
) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    interpreter = FakeDiscoveryInterpreter(
        DiscoveryTurn(
            intent="discovery",
            course_id=None,
            fields=("tech/data",),
            education_level=None,
            interests=("technology",),
            activities=("working with numbers",),
            unsure=False,
            correct_previous=False,
        )
    )
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
        interpreter,
    )
    lead_id, _ = service.start("123", "student")

    prompt = await service.free_text(lead_id, "I enjoy technology and numbers", None)

    assert "What would you most like to learn" in prompt.text
    assert any(data.startswith("guidance:goal:") for _, data in prompt.buttons)
    assert any(data == "guidance:goal:skip" for _, data in prompt.buttons)
    service.pause_discovery(lead_id)
    resumed = service.resume_discovery(lead_id)
    assert resumed.text == prompt.text
    assert resumed.buttons == prompt.buttons
    goal_reply = await service.choose_guidance_goal(lead_id, "analyze-data")
    assert "Did I get that right" in goal_reply.text
    assert "analyze data" in goal_reply.text
    old_confirm = next(
        data for _, data in goal_reply.buttons if data.startswith("guidance:confirm:")
    )
    interpreter.turn = DiscoveryTurn(
        intent="discovery",
        course_id=None,
        fields=("tech/data",),
        education_level=None,
        interests=("technology",),
        activities=("working with numbers",),
        unsure=False,
        correct_previous=True,
        learning_goals=("create digital products",),
    )
    corrected = await service.free_text(lead_id, "I changed my study goal", None)
    assert "create digital products" in corrected.text
    new_confirm = next(
        data for _, data in corrected.buttons if data.startswith("guidance:confirm:")
    )
    assert new_confirm != old_confirm
    stale = await service.confirm_guidance(lead_id, old_confirm.removeprefix("guidance:confirm:"))
    assert "create digital products" in stale.text

    results = await service.confirm_guidance(lead_id, new_confirm.removeprefix("guidance:confirm:"))
    assert "Web Application Development Diploma" in results.text
    assert "Applied Data Analytics Diploma" not in results.text
    assert "Supports your study goal: create digital products" in results.text


@pytest.mark.asyncio
async def test_broad_match_can_explore_catalog_language_support_and_resume(
    tmp_path: Path,
) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    interpreter = FakeDiscoveryInterpreter(
        DiscoveryTurn(
            intent="discovery",
            course_id=None,
            fields=("tech/data",),
            education_level=None,
            interests=("technology",),
            activities=("working with numbers",),
            unsure=False,
            correct_previous=False,
            learning_goals=("analyze data",),
        )
    )
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
        interpreter,
    )
    lead_id, _ = service.start("123", "student")

    prompt = await service.free_text(lead_id, "I want to analyze data", None)

    assert "English as the teaching medium" in prompt.text
    assert "Recorded language support differs" in prompt.text
    support_callbacks = {
        data for _, data in prompt.buttons if data.startswith("guidance:language:")
    }
    assert "guidance:language:english-support-sessions" in support_callbacks
    assert "guidance:language:malayalam-discussion-support" in support_callbacks
    service.pause_discovery(lead_id)
    resumed = service.resume_discovery(lead_id)
    assert resumed.text == prompt.text
    assert resumed.buttons == prompt.buttons

    reflection = await service.choose_guidance_language_support(
        lead_id, "malayalam-discussion-support"
    )
    assert "you prefer courses listing Malayalam discussion support" in reflection.text
    old_token = next(
        data.removeprefix("guidance:confirm:")
        for _, data in reflection.buttons
        if data.startswith("guidance:confirm:")
    )

    corrected = await service.choose_guidance_language_support(lead_id, "english-support-sessions")
    new_token = next(
        data.removeprefix("guidance:confirm:")
        for _, data in corrected.buttons
        if data.startswith("guidance:confirm:")
    )
    assert new_token != old_token
    stale = await service.confirm_guidance(lead_id, old_token)
    assert "you prefer courses listing English support sessions" in stale.text
    results = await service.confirm_guidance(lead_id, new_token)
    assert "Lists language support: English support sessions" in results.text
    assert "Teaching medium listed: English" in results.text
    assert "language support listed: English support sessions" in results.text
    assert "No complete matching sample course" not in results.text


@pytest.mark.asyncio
async def test_language_support_question_can_be_skipped_without_repeating(tmp_path: Path) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    interpreter = FakeDiscoveryInterpreter(
        DiscoveryTurn(
            intent="discovery",
            course_id=None,
            fields=("tech/data",),
            education_level=None,
            interests=("technology",),
            activities=("working with numbers",),
            unsure=False,
            correct_previous=False,
            learning_goals=("analyze data",),
        )
    )
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
        interpreter,
    )
    lead_id, _ = service.start("123", "student")
    prompt = await service.free_text(lead_id, "I want to analyze data", None)

    skipped = await service.choose_guidance_language_support(lead_id, None)

    assert "Did I get that right" in skipped.text
    assert "Recorded language support differs" not in skipped.text
    token = next(
        data.removeprefix("guidance:confirm:")
        for _, data in skipped.buttons
        if data.startswith("guidance:confirm:")
    )
    results = await service.confirm_guidance(lead_id, token)
    assert "matching fictional sample courses" in results.text
    assert not any(
        item["fact_key"] == "language_support_preference_student"
        for item in repository.list_facts(lead_id)
    )
    assert any(data == "guidance:language:open" for _, data in prompt.buttons)


@pytest.mark.asyncio
async def test_uniform_support_candidates_do_not_get_language_prompt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    original_courses = repository.list_courses(repository.tenant_id)
    monkeypatch.setattr(
        repository,
        "list_courses",
        lambda tenant_id: [
            replace(course, language_support=("English support sessions",))
            for course in original_courses
        ],
    )
    interpreter = FakeDiscoveryInterpreter(
        DiscoveryTurn(
            intent="discovery",
            course_id=None,
            fields=("tech/data",),
            education_level=None,
            interests=("technology",),
            activities=("working with numbers",),
            unsure=False,
            correct_previous=False,
            learning_goals=("analyze data",),
        )
    )
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
        interpreter,
    )
    lead_id, _ = service.start("123", "student")

    reply = await service.free_text(lead_id, "I want to analyze data", None)

    assert "Recorded language support differs" not in reply.text
    assert not any(data.startswith("guidance:language:") for _, data in reply.buttons)


@pytest.mark.asyncio
async def test_language_preference_statement_is_extracted_not_routed_as_faq(
    tmp_path: Path,
) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    interpreter = FakeDiscoveryInterpreter(
        DiscoveryTurn(
            intent="discovery",
            course_id=None,
            fields=("tech/data",),
            education_level=None,
            interests=("technology",),
            activities=("working with numbers",),
            unsure=False,
            correct_previous=False,
            learning_goals=("analyze data",),
            language_support_preference="Malayalam discussion support",
        )
    )
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
        interpreter,
    )
    lead_id, _ = service.start("123", "student")

    reply = await service.free_text(
        lead_id, "I prefer Malayalam discussion support while studying data", None
    )

    assert interpreter.calls
    assert "you prefer courses listing Malayalam discussion support" in reply.text
    assert any(
        item["fact_key"] == "language_support_preference_student"
        and item["fact_value"] == "Malayalam discussion support"
        for item in repository.list_facts(lead_id)
    )


@pytest.mark.asyncio
async def test_parent_language_preference_is_attributed_but_not_used_for_student(
    tmp_path: Path,
) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    interpreter = FakeDiscoveryInterpreter(
        DiscoveryTurn(
            intent="discovery",
            course_id=None,
            fields=(),
            education_level=None,
            interests=(),
            activities=(),
            unsure=False,
            correct_previous=False,
            language_support_preference="Malayalam discussion support",
        )
    )
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
        interpreter,
    )
    lead_id, _ = service.start("123", "student")
    service.choose_speaker(lead_id, "parent")

    reply = await service.free_text(
        lead_id, "I prefer Malayalam discussion support for my child", None
    )

    facts = repository.list_facts(lead_id)
    assert "parent's preferences" in reply.text
    assert any(
        fact["fact_key"] == "language_support_preference_parent"
        and fact["fact_value"] == "Malayalam discussion support"
        and fact["speaker"] == "parent"
        for fact in facts
    )
    assert not any(fact["fact_key"] == "language_support_preference_student" for fact in facts)


@pytest.mark.asyncio
async def test_unlisted_teaching_medium_request_gets_catalog_boundary_not_inference(
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

    reply = await service.free_text(lead_id, "I need Malayalam as the medium of instruction", None)

    assert "does not confirm the medium or proficiency rules" in reply.text
    assert not any(
        fact["fact_key"] == "language_support_preference_student"
        for fact in repository.list_facts(lead_id)
    )


@pytest.mark.asyncio
async def test_no_language_support_match_can_be_relaxed_after_confirmation(
    tmp_path: Path,
) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    interpreter = FakeDiscoveryInterpreter(
        DiscoveryTurn(
            intent="discovery",
            course_id=None,
            fields=("tech/data",),
            education_level=None,
            interests=("technology",),
            activities=("working with numbers",),
            unsure=False,
            correct_previous=False,
            learning_goals=("analyze data",),
            language_support_preference="Hindi discussion support",
        )
    )
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
        interpreter,
    )
    lead_id, _ = service.start("123", "student")
    reflection = await service.free_text(lead_id, "I want to analyze data", None)
    token = next(
        data.removeprefix("guidance:confirm:")
        for _, data in reflection.buttons
        if data.startswith("guidance:confirm:")
    )

    no_match = await service.confirm_guidance(lead_id, token)

    assert "No complete matching sample course lists Hindi discussion support" in no_match.text
    widened = await service.choose_guidance_language_support(lead_id, None)
    assert "matching fictional sample courses" in widened.text
    assert "Lists language support: Hindi discussion support" not in widened.text


@pytest.mark.asyncio
async def test_skipping_goal_question_does_not_ask_it_again(tmp_path: Path) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    interpreter = FakeDiscoveryInterpreter(
        DiscoveryTurn(
            intent="discovery",
            course_id=None,
            fields=("tech/data",),
            education_level=None,
            interests=("technology",),
            activities=("working with numbers",),
            unsure=False,
            correct_previous=False,
        )
    )
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
        interpreter,
    )
    lead_id, _ = service.start("123", "student")

    prompt = await service.free_text(lead_id, "I like technology and numbers", None)
    assert "What would you most like to learn" in prompt.text

    reply = await service.choose_guidance_goal(lead_id, None)

    assert "Did I get that right" in reply.text
    assert "What would you most like to learn" not in reply.text


@pytest.mark.asyncio
async def test_vague_interest_gets_targeted_follow_up_before_recommendations(
    tmp_path: Path,
) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    interpreter = FakeDiscoveryInterpreter(
        DiscoveryTurn(
            intent="discovery",
            course_id=None,
            fields=("design/media",),
            education_level=None,
            interests=("design",),
            activities=(),
            unsure=False,
            correct_previous=False,
        )
    )
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
        interpreter,
    )
    lead_id, _ = service.start("123", "student")

    follow_up = await service.free_text(lead_id, "I like design", None)

    assert "What would you like to do or learn more about" in follow_up.text
    assert "Digital Design Diploma" not in follow_up.text
    activity_choice = next(
        (data for _, data in follow_up.buttons if data.startswith("guidance:activity:")), None
    )
    assert activity_choice is not None

    reflection = await service.choose_guidance_signal(
        lead_id, activity_slug=activity_choice.removeprefix("guidance:activity:")
    )
    reflection = await _skip_optional_goal_prompt(service, lead_id, reflection)

    assert "Did I get that right" in reflection.text
    assert "Digital Design Diploma" not in reflection.text
    assert any(data.startswith("guidance:confirm:") for _, data in reflection.buttons)

    recommendation = await service.free_text(lead_id, "Yes, that sounds right", None)

    assert "Digital Design Diploma" in recommendation.text
    assert "Matches your interest in design" in recommendation.text
    assert "Includes activities you chose" in recommendation.text
    assert len(interpreter.calls) == 1


@pytest.mark.asyncio
async def test_changed_preferences_make_an_old_confirmation_button_stale(
    tmp_path: Path,
) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    interpreter = FakeDiscoveryInterpreter(
        DiscoveryTurn("discovery", None, ("design/media",), None, ("design",), (), False, False)
    )
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
        interpreter,
    )
    lead_id, _ = service.start("123", "student")

    follow_up = await service.free_text(lead_id, "I like design", None)
    activity_choice = next(
        data for _, data in follow_up.buttons if data.startswith("guidance:activity:")
    )
    old_reflection = await service.choose_guidance_signal(
        lead_id, activity_slug=activity_choice.removeprefix("guidance:activity:")
    )
    old_reflection = await _skip_optional_goal_prompt(service, lead_id, old_reflection)
    old_confirmation = next(
        data for _, data in old_reflection.buttons if data.startswith("guidance:confirm:")
    )

    interpreter.turn = DiscoveryTurn(
        "discovery",
        None,
        ("business/accounting",),
        None,
        ("business",),
        ("planning projects",),
        False,
        True,
    )
    corrected = await service.free_text(
        lead_id, "Actually, business and planning projects fit me better", None
    )
    corrected = await _skip_optional_goal_prompt(service, lead_id, corrected)
    new_confirmation = next(
        data for _, data in corrected.buttons if data.startswith("guidance:confirm:")
    )

    assert "business/accounting" in corrected.text
    assert "Digital Design Diploma" not in corrected.text
    assert new_confirmation != old_confirmation

    stale_reply = await service.confirm_guidance(
        lead_id, old_confirmation.removeprefix("guidance:confirm:")
    )

    assert "business/accounting" in stale_reply.text
    assert "Digital Design Diploma" not in stale_reply.text


@pytest.mark.asyncio
async def test_guidance_reflection_resumes_and_confirmation_is_path_bound(
    tmp_path: Path,
) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    interpreter = FakeDiscoveryInterpreter(
        DiscoveryTurn("discovery", None, ("design/media",), None, ("design",), (), False, False)
    )
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
        interpreter,
    )
    lead_id, _ = service.start("123", "student")
    follow_up = await service.free_text(lead_id, "I like design", None)
    activity_choice = next(
        data for _, data in follow_up.buttons if data.startswith("guidance:activity:")
    )
    reflection = await service.choose_guidance_signal(
        lead_id, activity_slug=activity_choice.removeprefix("guidance:activity:")
    )
    reflection = await _skip_optional_goal_prompt(service, lead_id, reflection)
    token = next(
        data.removeprefix("guidance:confirm:")
        for _, data in reflection.buttons
        if data.startswith("guidance:confirm:")
    )

    service.pause_discovery(lead_id)
    resumed = service.resume_discovery(lead_id)

    assert "Did I get that right" in resumed.text
    assert token in {data.removeprefix("guidance:confirm:") for _, data in resumed.buttons}
    accepted = await service.confirm_guidance(lead_id, token)
    assert "Digital Design Diploma" in accepted.text
    service.pause_discovery(lead_id)
    resumed_results = service.resume_discovery(lead_id)
    assert "Digital Design Diploma" in resumed_results.text
    assert "Did I get that right" not in resumed_results.text

    service.begin_path(lead_id, "browse")
    stale = await service.confirm_guidance(lead_id, token)

    assert "confirmation has expired" in stale.text
    assert "Digital Design Diploma" not in stale.text


@pytest.mark.asyncio
async def test_preference_correction_requires_confirmation_even_if_facts_return_to_old_values(
    tmp_path: Path,
) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    interpreter = FakeDiscoveryInterpreter(
        DiscoveryTurn(
            "discovery",
            None,
            ("design/media",),
            None,
            ("design",),
            ("making visuals",),
            False,
            False,
        )
    )
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
        interpreter,
    )
    lead_id, _ = service.start("123", "student")
    initial = await service.free_text(lead_id, "I like design and making visuals", None)
    initial = await _skip_optional_goal_prompt(service, lead_id, initial)
    first_token = next(
        data.removeprefix("guidance:confirm:")
        for _, data in initial.buttons
        if data.startswith("guidance:confirm:")
    )
    shown = await service.confirm_guidance(lead_id, first_token)
    assert "Digital Design Diploma" in shown.text

    interpreter.turn = DiscoveryTurn(
        "discovery",
        None,
        ("design/media",),
        None,
        ("design",),
        ("making visuals",),
        False,
        True,
    )
    reconfirm = await service.free_text(lead_id, "I want to reconsider my choices", None)
    reconfirm = await _skip_optional_goal_prompt(service, lead_id, reconfirm)

    assert "Did I get that right" in reconfirm.text
    assert "Digital Design Diploma" not in reconfirm.text


@pytest.mark.asyncio
async def test_guidance_revision_prompt_survives_pause_and_resume(tmp_path: Path) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    interpreter = FakeDiscoveryInterpreter(
        DiscoveryTurn("discovery", None, ("design/media",), None, ("design",), (), False, False)
    )
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
        interpreter,
    )
    lead_id, _ = service.start("123", "student")
    follow_up = await service.free_text(lead_id, "I like design", None)
    activity = next(data for _, data in follow_up.buttons if data.startswith("guidance:activity:"))
    reflection = await service.choose_guidance_signal(
        lead_id, activity_slug=activity.removeprefix("guidance:activity:")
    )
    reflection = await _skip_optional_goal_prompt(service, lead_id, reflection)
    token = next(
        data.removeprefix("guidance:revise:")
        for _, data in reflection.buttons
        if data.startswith("guidance:revise:")
    )

    revision = await service.revise_guidance(lead_id, token)
    service.pause_discovery(lead_id)
    resumed = service.resume_discovery(lead_id)

    assert "What should I change or add" in revision.text
    assert resumed.text == revision.text


@pytest.mark.asyncio
async def test_discovery_interpreter_is_called_by_default_and_opt_out_disables_it(
    tmp_path: Path,
) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    interpreter = FakeDiscoveryInterpreter(
        DiscoveryTurn("discovery", None, (), None, (), (), False, False)
    )
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
        interpreter,
    )
    lead_id, _ = service.start("123", "student")

    reply = await service.free_text(lead_id, "I like design", None)

    assert len(interpreter.calls) == 1

    service.set_ai_processing_enabled(lead_id, False)
    reply = await service.free_text(lead_id, "I like design", None)

    assert len(interpreter.calls) == 1
    assert "OpenAI processing is off" in reply.text
    assert "buttons" in reply.text.casefold() or "tap" in reply.text.casefold()


@pytest.mark.asyncio
async def test_extraction_failure_does_not_persist_partial_facts(tmp_path: Path) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
        FailingDiscoveryInterpreter(),
    )
    lead_id, _ = service.start("123", "student")
    service.set_ai_processing_enabled(lead_id, True)
    reply = await service.free_text(lead_id, "I enjoy art and making posters", None)

    assert "couldn't understand that safely" in reply.text.casefold()
    assert not any(
        fact["fact_key"].startswith(("interest_", "education_level_", "activity_"))
        for fact in repository.list_facts(lead_id)
    )


@pytest.mark.asyncio
async def test_natural_language_known_course_enters_existing_course_flow(tmp_path: Path) -> None:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    course = next(
        item
        for item in repository.list_courses(repository.tenant_id)
        if item.education_level == "undergraduate"
    )
    interpreter = FakeDiscoveryInterpreter(
        DiscoveryTurn("course_lookup", course.id, (), None, (), (), False, False)
    )
    service = AdmissionsService(
        repository,
        repository.tenant_id,
        RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05),
        interpreter,
    )
    lead_id, _ = service.start("123", "student")
    service.set_ai_processing_enabled(lead_id, True)

    reply = await service.free_text(lead_id, f"I already know I want {course.name}", None)

    assert "Grade 12" in reply.text
    assert "Recorded language support differs" not in reply.text
    assert repository.get_lead(lead_id)["selected_course_id"] == course.id  # type: ignore[index]
    assert not any(
        fact["fact_key"].startswith(("interest_field", "interest_terms", "activity_terms"))
        for fact in repository.list_facts(lead_id)
    )


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
    welcome = service.set_ai_processing_enabled(lead_id, True)

    reply = service.browse(lead_id)

    assert ("Just browsing / ask a question", "path:browse") in welcome.buttons
    assert "fictional sample courses" in reply.text
    assert repository.get_lead(lead_id)["state"] == "browsing"  # type: ignore[index]


@pytest.mark.asyncio
async def test_known_field_recommends_only_complete_catalog_courses_and_persists_path(
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
    welcome = service.set_ai_processing_enabled(lead_id, True)

    assert {data for _, data in welcome.buttons} >= {
        "path:course",
        "path:field",
        "path:explore",
        "path:browse",
    }
    service.begin_path(lead_id, "field")
    level_reply = service.recommend_field(lead_id, "tech/data")
    assert any(data == "level:any" for _, data in level_reply.buttons)
    reflection = service.choose_level(lead_id, "any")
    reflection = await _skip_optional_goal_prompt(service, lead_id, reflection)
    assert "open to all listed study levels" in reflection.text
    pending = next(data for _, data in reflection.buttons if data.startswith("guidance:confirm:"))
    reply = await service.confirm_guidance(lead_id, pending.removeprefix("guidance:confirm:"))

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
@pytest.mark.asyncio
async def test_fixed_catalog_evaluation_matrix_returns_expected_complete_course(
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
    reflection = service.choose_level(lead_id, level)
    reflection = await _skip_optional_goal_prompt(service, lead_id, reflection)
    assert "Did I get that right" in reflection.text
    confirmation = next(
        data for _, data in reflection.buttons if data.startswith("guidance:confirm:")
    )
    result = await service.confirm_guidance(lead_id, confirmation.removeprefix("guidance:confirm:"))

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
