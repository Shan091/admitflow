from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import pytest

from admitflow.adapters.sqlite import Repository
from admitflow.adapters.telegram import callback_handler, keyboard, start_command, text_handler
from admitflow.adapters.vector_store import VectorStore
from admitflow.services.admissions import AdmissionsService, Reply
from admitflow.services.retrieval import RetrievalService


class FakeMessage:
    def __init__(self, text: str | None = None) -> None:
        self.text = text
        self.sent: list[tuple[str, object]] = []

    async def reply_text(self, text: str, reply_markup: object = None) -> None:
        self.sent.append((text, reply_markup))


def make_runtime(tmp_path: Path) -> tuple[Repository, AdmissionsService, SimpleNamespace]:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    retrieval = RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05)
    admissions = AdmissionsService(repository, repository.tenant_id, retrieval)
    context = SimpleNamespace(
        application=SimpleNamespace(
            bot_data={"repository": repository, "admissions": admissions, "intent_router": None}
        )
    )
    return repository, admissions, context


@pytest.mark.parametrize(
    ("language", "opt_out_label"),
    [
        ("en", "Turn off OpenAI processing"),
        ("hi", "OpenAI प्रोसेसिंग बंद करें"),
        ("ml", "OpenAI പ്രോസസ്സിംഗ് ഓഫ് ചെയ്യുക"),
        ("hinglish", "OpenAI processing band karein"),
    ],
)
def test_persistent_openai_opt_out_keyboard_uses_selected_language(
    language: str, opt_out_label: str
) -> None:
    markup = keyboard(Reply("Continue"), ai_processing_allowed=True, language=language)

    assert markup is not None
    labels = {button.text for row in markup.inline_keyboard for button in row}
    callback_data = {button.callback_data for row in markup.inline_keyboard for button in row}
    assert opt_out_label in labels
    assert "ai:processing:off" in callback_data


@pytest.mark.asyncio
async def test_start_command_discloses_ai_processing_and_starts_discovery(tmp_path: Path) -> None:
    repository, _, context = make_runtime(tmp_path)
    message = FakeMessage()
    update = SimpleNamespace(
        effective_user=SimpleNamespace(id=42, username="sample"),
        effective_message=message,
        update_id=100,
    )

    await start_command(update, context)

    leads = repository.list_leads(repository.tenant_id)
    assert len(leads) == 1
    assert leads[0]["telegram_user_id"] == "42"
    assert len(repository.list_messages(int(leads[0]["id"]))) == 2
    assert "fictional demo guidance" in message.sent[0][0]
    assert "OpenAI" in message.sent[0][0]
    assert "demo text only" in message.sent[0][0]
    assert message.sent[0][1] is not None
    assert any(
        button.callback_data == "path:explore"
        for row in message.sent[0][1].inline_keyboard
        for button in row
    )
    assert any(
        button.callback_data == "language:menu"
        for row in message.sent[0][1].inline_keyboard
        for button in row
    )


@pytest.mark.asyncio
async def test_user_can_turn_openai_processing_off_and_back_on(tmp_path: Path) -> None:
    repository, admissions, context = make_runtime(tmp_path)
    lead_id, _ = admissions.start("42", "sample")
    message = FakeMessage()

    async def answer() -> None:
        return None

    update = SimpleNamespace(
        callback_query=SimpleNamespace(answer=answer, data="ai:processing:off"),
        effective_user=SimpleNamespace(id=42, username="sample"),
        effective_message=message,
        update_id=140,
    )
    await callback_handler(update, context)
    assert not admissions.ai_processing_enabled(lead_id)
    assert "OpenAI processing is off" in message.sent[-1][0]
    off_markup = message.sent[-1][1]
    assert off_markup is not None
    assert any(
        button.callback_data == "ai:processing:on"
        for row in off_markup.inline_keyboard
        for button in row
    )

    update.callback_query = SimpleNamespace(answer=answer, data="ai:processing:on")
    update.update_id = 141
    await callback_handler(update, context)
    assert admissions.ai_processing_enabled(lead_id)
    assert "Typed messages are sent to OpenAI" in message.sent[-1][0]
    on_markup = message.sent[-1][1]
    assert on_markup is not None
    assert any(
        button.callback_data == "ai:processing:off"
        for row in on_markup.inline_keyboard
        for button in row
    )


@pytest.mark.asyncio
async def test_course_callback_updates_lead_and_persists_exchange(tmp_path: Path) -> None:
    repository, _, context = make_runtime(tmp_path)
    message = FakeMessage()
    answered = False

    async def answer() -> None:
        nonlocal answered
        answered = True

    query = SimpleNamespace(answer=answer, data="course:foundations-computing")
    update = SimpleNamespace(
        callback_query=query,
        effective_user=SimpleNamespace(id=42, username="sample"),
        effective_message=message,
        update_id=101,
    )

    await callback_handler(update, context)

    lead = repository.list_leads(repository.tenant_id)[0]
    assert answered
    assert lead["selected_course_id"] == "foundations-computing"
    assert lead["state"] == "awaiting_grade12"
    assert len(repository.list_messages(int(lead["id"]))) == 2
    assert "Have you completed Grade 12?" in message.sent[0][0]


@pytest.mark.asyncio
async def test_guided_course_detail_callback_does_not_enter_qualification(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repository, admissions, context = make_runtime(tmp_path)
    original_courses = repository.list_courses(repository.tenant_id)
    monkeypatch.setattr(
        repository,
        "list_courses",
        lambda tenant_id: [
            replace(
                course,
                learning_goals=("analyze data",),
                language_support=("English support sessions",),
                delivery_modes=("in_person",),
            )
            for course in original_courses
        ],
    )
    lead_id, _ = admissions.start("42", "sample")
    repository.save_fact(lead_id, "interest_terms_student", "technology", "student")
    repository.save_fact(lead_id, "activity_terms_student", "making charts", "student")
    repository.save_fact(lead_id, "education_level_student", "undergraduate", "student")
    repository.update_lead(lead_id, education_level="undergraduate")
    reflection = admissions._present_guidance(lead_id)
    token = next(
        data.removeprefix("guidance:confirm:")
        for _, data in reflection.buttons
        if data.startswith("guidance:confirm:")
    )
    results = await admissions.confirm_guidance(lead_id, token)
    course_id = next(
        data.removeprefix("guidance:course:")
        for _, data in results.buttons
        if data.startswith("guidance:course:")
    )
    message = FakeMessage()

    async def answer() -> None:
        return None

    update = SimpleNamespace(
        callback_query=SimpleNamespace(answer=answer, data=f"guidance:course:{course_id}"),
        effective_user=SimpleNamespace(id=42, username="sample"),
        effective_message=message,
        update_id=150,
    )
    await callback_handler(update, context)

    assert "Fictional sample details" in message.sent[-1][0]
    assert repository.get_lead(lead_id)["selected_course_id"] is None
    callbacks = {
        button.callback_data for row in message.sent[-1][1].inline_keyboard for button in row
    }
    assert f"course:{course_id}" in callbacks
    assert "guidance:matches" in callbacks

    update.callback_query = SimpleNamespace(answer=answer, data="guidance:matches")
    update.update_id = 151
    await callback_handler(update, context)
    assert "matching fictional sample courses" in message.sent[-1][0]
    assert any(
        button.callback_data == f"guidance:course:{course_id}"
        for row in message.sent[-1][1].inline_keyboard
        for button in row
    )


@pytest.mark.asyncio
async def test_language_support_callback_records_catalog_option(tmp_path: Path) -> None:
    repository, admissions, context = make_runtime(tmp_path)
    lead_id, _ = admissions.start("42", "sample")
    repository.save_fact(lead_id, "interest_terms_student", "technology", "student")
    repository.save_fact(lead_id, "activity_terms_student", "working with numbers", "student")
    repository.save_fact(lead_id, "learning_goals_student", "analyze data", "student")
    message = FakeMessage()
    answered = False

    async def answer() -> None:
        nonlocal answered
        answered = True

    update = SimpleNamespace(
        callback_query=SimpleNamespace(
            answer=answer, data="guidance:language:malayalam-discussion-support"
        ),
        effective_user=SimpleNamespace(id=42, username="sample"),
        effective_message=message,
        update_id=145,
    )

    await callback_handler(update, context)

    assert answered
    assert "you prefer courses listing Malayalam discussion support" in message.sent[-1][0]
    assert any(
        fact["fact_key"] == "language_support_preference_student"
        and fact["fact_value"] == "Malayalam discussion support"
        for fact in repository.list_facts(lead_id)
    )


@pytest.mark.asyncio
async def test_delivery_mode_open_callback_keeps_format_unspecified(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repository, admissions, context = make_runtime(tmp_path)
    lead_id, _ = admissions.start("42", "sample")
    original_courses = repository.list_courses(repository.tenant_id)
    monkeypatch.setattr(
        repository,
        "list_courses",
        lambda tenant_id: [
            replace(
                course,
                learning_goals=("analyze data",),
                language_support=("English support sessions",),
            )
            for course in original_courses
        ],
    )
    repository.save_fact(lead_id, "interest_terms_student", "technology", "student")
    repository.save_fact(lead_id, "activity_terms_student", "making charts", "student")
    prompt = admissions._present_guidance(lead_id)
    assert "different study formats" in prompt.text
    message = FakeMessage()

    async def answer() -> None:
        return None

    update = SimpleNamespace(
        callback_query=SimpleNamespace(answer=answer, data="guidance:mode:open"),
        effective_user=SimpleNamespace(id=42, username="sample"),
        effective_message=message,
        update_id=146,
    )

    await callback_handler(update, context)

    assert "Did I get that right" in message.sent[-1][0]
    assert not any(
        fact["fact_key"] == "delivery_mode_preference_student"
        for fact in repository.list_facts(lead_id)
    )


@pytest.mark.asyncio
async def test_exploration_callbacks_recommend_and_language_choice_persists(tmp_path: Path) -> None:
    repository, _, context = make_runtime(tmp_path)
    message = FakeMessage()
    answered = False

    async def answer() -> None:
        nonlocal answered
        answered = True

    user = SimpleNamespace(id=42, username="sample")
    update = SimpleNamespace(
        callback_query=SimpleNamespace(answer=answer, data="path:explore"),
        effective_user=user,
        effective_message=message,
        update_id=110,
    )

    await callback_handler(update, context)
    assert answered
    assert "topics or activities" in message.sent[-1][0]
    assert repository.list_leads(repository.tenant_id)[0]["lifecycle_stage"] == "discovering"

    async def answer_field() -> None:
        return None

    update.callback_query = SimpleNamespace(answer=answer_field, data="field:tech/data")
    update.update_id = 111
    await callback_handler(update, context)
    assert "What would you like to do or learn more about" in message.sent[-1][0]
    activity_choice = next(
        button.callback_data
        for row in message.sent[-1][1].inline_keyboard
        for button in row
        if button.callback_data and button.callback_data.startswith("guidance:activity:")
    )

    async def answer_activity() -> None:
        return None

    update.callback_query = SimpleNamespace(answer=answer_activity, data=activity_choice)
    update.update_id = 112
    await callback_handler(update, context)
    assert "What would you most like to learn" in message.sent[-1][0]

    async def answer_goal() -> None:
        return None

    update.callback_query = SimpleNamespace(answer=answer_goal, data="guidance:goal:analyze-data")
    update.update_id = 113
    await callback_handler(update, context)
    assert "Did I get that right" in message.sent[-1][0]
    assert "analyze data" in message.sent[-1][0]
    confirmation_markup = message.sent[-1][1]
    assert confirmation_markup is not None
    confirm_callback = next(
        button.callback_data
        for row in confirmation_markup.inline_keyboard
        for button in row
        if button.callback_data and button.callback_data.startswith("guidance:confirm:")
    )

    async def answer_confirm_guidance() -> None:
        return None

    update.callback_query = SimpleNamespace(answer=answer_confirm_guidance, data=confirm_callback)
    update.update_id = 114
    await callback_handler(update, context)
    assert "matching fictional sample courses" in message.sent[-1][0]

    async def answer_language() -> None:
        return None

    update.callback_query = SimpleNamespace(answer=answer_language, data="language:ml")
    update.update_id = 115
    await callback_handler(update, context)
    lead = repository.list_leads(repository.tenant_id)[0]
    assert lead["preferred_language"] == "ml"
    assert "OpenAI-ലേക്ക് അയയ്ക്കുകയും" in message.sent[-1][0]
    markup = message.sent[-1][1]
    assert markup is not None
    callbacks = {button.callback_data for row in markup.inline_keyboard for button in row}
    assert "path:explore" in callbacks
    assert "ai:processing:off" in callbacks


@pytest.mark.asyncio
async def test_qualification_sends_test_payment_link_when_enabled(tmp_path: Path) -> None:
    repository, admissions, context = make_runtime(tmp_path)
    lead_id, _ = admissions.start("42", "sample")
    admissions.select_course(lead_id, "foundations-computing")
    admissions.answer_grade12(lead_id, True)

    class FakePayments:
        async def create_for_qualified_lead(self, requested_lead_id: int) -> tuple[str, int]:
            assert requested_lead_id == lead_id
            return "https://rzp.io/i/test123", 50000

    context.application.bot_data["payment_service"] = FakePayments()
    message = FakeMessage("75")
    update = SimpleNamespace(
        effective_user=SimpleNamespace(id=42, username="sample"),
        effective_message=message,
        update_id=102,
    )

    await text_handler(update, context)

    assert "Would you like to continue" in message.sent[0][0]
    assert "https://rzp.io/i/test123" not in message.sent[0][0]

    async def answer_payment() -> None:
        return None

    payment_message = FakeMessage()
    payment_update = SimpleNamespace(
        callback_query=SimpleNamespace(answer=answer_payment, data="payment:yes"),
        effective_user=SimpleNamespace(id=42, username="sample"),
        effective_message=payment_message,
        update_id=104,
    )
    await callback_handler(payment_update, context)

    assert "Razorpay test-mode" in payment_message.sent[0][0]
    assert "₹500" in payment_message.sent[0][0]
    assert "https://rzp.io/i/test123" in payment_message.sent[0][0]
    assert repository.get_lead(lead_id)["readiness_status"] == "ready_to_apply"  # type: ignore[index]
    stored_messages = repository.list_messages(lead_id)
    assert stored_messages[-1]["direction"] == "outbound"
    assert "https://rzp.io/i/test123" in stored_messages[-1]["body"]


@pytest.mark.parametrize(
    ("payment_status", "expected_text"),
    [
        ("missing", "don't see a demo application payment link"),
        ("created", "payment is still pending"),
        ("paid", "payment is confirmed as paid"),
    ],
)
@pytest.mark.asyncio
async def test_payment_status_question_uses_persisted_state(
    tmp_path: Path, payment_status: str, expected_text: str
) -> None:
    repository, admissions, context = make_runtime(tmp_path)
    lead_id, _ = admissions.start("42", "sample")
    admissions.select_course(lead_id, "foundations-computing")
    admissions.answer_grade12(lead_id, True)
    admissions.answer_marks(lead_id, "75")

    if payment_status != "missing":
        payment, created = repository.get_or_create_payment_intent(
            repository.tenant_id, lead_id, "AF-status-test"
        )
        assert created and payment is not None
        repository.save_payment_link(payment["id"], "plink_status_test", "https://rzp.io/test")
        if payment_status == "paid":
            event = {
                "payload": {
                    "payment_link": {
                        "entity": {
                            "id": "plink_status_test",
                            "reference_id": "AF-status-test",
                            "status": "paid",
                            "amount": 50000,
                            "amount_paid": 50000,
                            "currency": "INR",
                        }
                    }
                }
            }
            assert repository.apply_razorpay_paid_event("evt-status-test", event) == "applied"

    message = FakeMessage("Has my payment gone through?")
    update = SimpleNamespace(
        effective_user=SimpleNamespace(id=42, username="sample"),
        effective_message=message,
        update_id=103,
    )

    await text_handler(update, context)

    assert expected_text in message.sent[0][0]
