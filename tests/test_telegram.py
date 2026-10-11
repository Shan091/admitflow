from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import pytest

from admitflow.adapters.sqlite import Repository
from admitflow.adapters.telegram import (
    _record_trace_reply,
    _trace_telegram_interaction,
    callback_handler,
    keyboard,
    start_command,
    text_handler,
)
from admitflow.adapters.vector_store import VectorStore
from admitflow.domain.models import Course, DiscoveryTurn
from admitflow.services.admissions import AdmissionsService, Reply
from admitflow.services.retrieval import RetrievalService


class FakeMessage:
    def __init__(
        self,
        text: str | None = None,
        events: list[tuple[object, ...]] | None = None,
    ) -> None:
        self.text = text
        self.chat_id: int | None = None
        self.sent: list[tuple[str, object]] = []
        self.events = events

    async def reply_text(self, text: str, reply_markup: object = None) -> None:
        self.sent.append((text, reply_markup))
        if self.events is not None:
            self.events.append(("reply", text))


class FakeBot:
    def __init__(self) -> None:
        self.events: list[tuple[object, ...]] = []

    async def send_chat_action(self, *, chat_id: int | None, action: str) -> bool:
        self.events.append(("action", chat_id, action))
        return True


class FakeTrace:
    def __init__(self, *, input: object) -> None:
        self.input = input
        self.output: object = None

    def update(self, *, output: object) -> None:
        self.output = output


class FakeLangfuse:
    def __init__(self) -> None:
        self.observations: list[FakeTrace] = []
        self.flush_count = 0

    def flush(self) -> None:
        self.flush_count += 1

    @contextmanager
    def start_as_current_observation(self, **kwargs: object):
        trace = FakeTrace(input=kwargs["input"])
        self.observations.append(trace)
        yield trace


class FailingFlushLangfuse(FakeLangfuse):
    def flush(self) -> None:
        raise RuntimeError("synthetic Langfuse export failure")


class FailingLangfuse:
    def start_as_current_observation(self, **kwargs: object):
        raise RuntimeError("synthetic Langfuse failure")


def make_runtime(tmp_path: Path) -> tuple[Repository, AdmissionsService, SimpleNamespace]:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    retrieval = RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05)
    admissions = AdmissionsService(repository, repository.tenant_id, retrieval)
    bot = FakeBot()
    context = SimpleNamespace(
        bot=bot,
        application=SimpleNamespace(
            bot_data={"repository": repository, "admissions": admissions, "intent_router": None}
        ),
    )
    return repository, admissions, context


def test_langfuse_trace_records_ids_messages_replies_and_saved_facts(tmp_path: Path) -> None:
    repository, admissions, _ = make_runtime(tmp_path)
    lead_id, _ = admissions.start("12345", "student")
    repository.save_fact(lead_id, "interest", "data analysis")
    langfuse = FakeLangfuse()

    with _trace_telegram_interaction(
        langfuse, repository, lead_id, "12345", "67890", "I like data analysis"
    ) as observation:
        _record_trace_reply(observation, Reply("Let's explore data courses."), repository, lead_id)

    assert len(langfuse.observations) == 1
    trace = langfuse.observations[0]
    assert trace.input["telegram_user_id"] == "12345"
    assert trace.input["telegram_chat_id"] == "67890"
    assert trace.input["message_text"] == "I like data analysis"
    assert trace.input["saved_learner_facts"][0]["fact_value"] == "data analysis"
    assert trace.output["reply_text"] == "Let's explore data courses."
    assert trace.output["saved_learner_facts"][0]["fact_value"] == "data analysis"
    assert langfuse.flush_count == 1


def test_langfuse_trace_failure_does_not_block_the_turn(tmp_path: Path) -> None:
    repository, admissions, _ = make_runtime(tmp_path)
    lead_id, _ = admissions.start("12345", "student")

    with _trace_telegram_interaction(
        FailingLangfuse(), repository, lead_id, "12345", "67890", "hello"
    ) as observation:
        assert observation is None


def test_langfuse_flush_failure_does_not_block_the_turn(tmp_path: Path) -> None:
    repository, admissions, _ = make_runtime(tmp_path)
    lead_id, _ = admissions.start("12345", "student")

    with _trace_telegram_interaction(
        FailingFlushLangfuse(), repository, lead_id, "12345", "67890", "hello"
    ) as observation:
        assert observation is not None
        observation.update(output={"reply_text": "hello back"})


@pytest.mark.asyncio
async def test_ai_text_turn_sends_typing_action_before_reply(tmp_path: Path) -> None:
    _, _, context = make_runtime(tmp_path)
    message = FakeMessage("hello", events=context.bot.events)
    message.chat_id = 42
    update = SimpleNamespace(
        effective_user=SimpleNamespace(id=42, username="sample"),
        effective_message=message,
        update_id=199,
    )

    await text_handler(update, context)

    assert context.bot.events[0] == ("action", 42, "typing")
    assert context.bot.events[1][0] == "reply"
    assert len(message.sent) == 1


@pytest.mark.asyncio
async def test_opted_out_text_turn_does_not_send_typing_action(tmp_path: Path) -> None:
    _, admissions, context = make_runtime(tmp_path)
    lead_id, _ = admissions.start("42", "sample")
    admissions.set_ai_processing_enabled(lead_id, False)
    message = FakeMessage("hello", events=context.bot.events)
    message.chat_id = 42
    update = SimpleNamespace(
        effective_user=SimpleNamespace(id=42, username="sample"),
        effective_message=message,
        update_id=200,
    )

    await text_handler(update, context)

    assert not context.bot.events or context.bot.events[0][0] != "action"
    assert len(message.sent) == 1


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
    markup = keyboard(
        Reply("Continue"),
        ai_processing_allowed=True,
        show_ai_processing_control=True,
        language=language,
    )

    assert markup is not None
    labels = {button.text for row in markup.inline_keyboard for button in row}
    callback_data = {button.callback_data for row in markup.inline_keyboard for button in row}
    assert opt_out_label in labels
    assert "ai:processing:off" in callback_data


def test_openai_opt_out_control_is_not_added_to_routine_reply() -> None:
    markup = keyboard(Reply("Continue"), ai_processing_allowed=True)

    assert markup is not None
    assert all(
        button.callback_data != "ai:processing:off"
        for row in markup.inline_keyboard
        for button in row
    )


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
    assert "Course details and fees are for demonstration" in message.sent[0][0]
    assert "OpenAI" in message.sent[0][0]
    assert "recent chat context" in message.sent[0][0]
    assert "don't share real student" in message.sent[0][0]
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
    assert any(
        button.callback_data == "ai:processing:off"
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
    assert "recent chat context are sent to OpenAI" in message.sent[-1][0]
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

    assert "Course details" in message.sent[-1][0]
    assert repository.get_lead(lead_id)["selected_course_id"] is None
    callbacks = {
        button.callback_data for row in message.sent[-1][1].inline_keyboard for button in row
    }
    assert f"guidance:continue:{course_id}" in callbacks
    assert "guidance:matches" in callbacks

    update.callback_query = SimpleNamespace(answer=answer, data="guidance:matches")
    update.update_id = 151
    await callback_handler(update, context)
    assert "matching courses" in message.sent[-1][0]
    assert any(
        button.callback_data == f"guidance:course:{course_id}"
        for row in message.sent[-1][1].inline_keyboard
        for button in row
    )
    update.callback_query = SimpleNamespace(answer=answer, data=f"guidance:continue:{course_id}")
    update.update_id = 153
    await callback_handler(update, context)
    assert "Have you completed Grade 12?" in message.sent[-1][0]
    assert repository.get_lead(lead_id)["selected_course_id"] == course_id


@pytest.mark.asyncio
async def test_unrelated_text_during_confirmation_gets_focused_recovery_not_same_prompt(
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

    class FixedInterpreter:
        async def extract_discovery(
            self,
            text: str,
            courses: list[Course],
            conversation_context: dict[str, object] | None = None,
        ) -> DiscoveryTurn:
            assert text == "no can you write me a story"
            return DiscoveryTurn(
                "out_of_scope",
                None,
                (),
                None,
                (),
                (),
                False,
                False,
                assistant_message=(
                    "I can help with course questions. What would you like to explore?"
                ),
            )

    admissions.discovery_interpreter = FixedInterpreter()
    message = FakeMessage("no can you write me a story")
    update = SimpleNamespace(
        effective_user=SimpleNamespace(id=42, username="sample"),
        effective_message=message,
        update_id=152,
    )
    await text_handler(update, context)

    response, markup = message.sent[-1]
    assert "Did I get that right" in reflection.text
    assert "Did I get that right" not in response
    assert response == "I can help with course questions. What would you like to explore?"
    assert "staff" not in response.casefold()
    assert repository.get_lead(lead_id)["discovery_step"] == "guidance_confirmation"
    assert markup is not None
    callbacks = {button.callback_data for row in markup.inline_keyboard for button in row}
    assert any(str(callback).startswith("guidance:confirm:") for callback in callbacks)
    assert any(str(callback).startswith("guidance:revise:") for callback in callbacks)
    assert "path:browse" in callbacks


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
    assert "matching courses" in message.sent[-1][0]

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
    assert "ai:processing:off" not in callbacks


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

    assert "This is a test payment" in payment_message.sent[0][0]
    assert "₹500" in payment_message.sent[0][0]
    assert "https://rzp.io/i/test123" in payment_message.sent[0][0]
    assert repository.get_lead(lead_id)["readiness_status"] == "ready_to_apply"  # type: ignore[index]
    stored_messages = repository.list_messages(lead_id)
    assert stored_messages[-1]["direction"] == "outbound"
    assert "https://rzp.io/i/test123" in stored_messages[-1]["body"]


@pytest.mark.asyncio
async def test_diploma_self_report_can_reach_the_test_payment_link(tmp_path: Path) -> None:
    repository, admissions, context = make_runtime(tmp_path)
    lead_id, _ = admissions.start("42", "sample")

    class FakePayments:
        async def create_for_qualified_lead(self, requested_lead_id: int) -> tuple[str, int]:
            assert requested_lead_id == lead_id
            return "https://rzp.io/i/diploma-test", 35000

    context.application.bot_data["payment_service"] = FakePayments()

    async def tap(data: str) -> FakeMessage:
        message = FakeMessage()
        update = SimpleNamespace(
            callback_query=SimpleNamespace(answer=_no_op, data=data),
            effective_user=SimpleNamespace(id=42, username="sample"),
            effective_message=message,
            update_id=104,
        )
        await callback_handler(update, context)
        return message

    course_prompt = await tap("course:hospitality-diploma")
    assert "sample-prerequisites:yes:hospitality-diploma" in _callback_data(course_prompt)

    confirmation = await tap("sample-prerequisites:yes:hospitality-diploma")
    assert "payment:yes" in _callback_data(confirmation)
    assert "self-report" in confirmation.sent[0][0].casefold()

    payment = await tap("payment:yes")
    assert "https://rzp.io/i/diploma-test" in payment.sent[0][0]
    assert "₹350" in payment.sent[0][0]


async def _no_op() -> None:
    return None


def _callback_data(message: FakeMessage) -> set[str]:
    markup = message.sent[-1][1]
    assert markup is not None
    return {button.callback_data for row in markup.inline_keyboard for button in row}


@pytest.mark.parametrize(
    ("payment_status", "expected_text"),
    [
        ("missing", "don't see an application payment link"),
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
