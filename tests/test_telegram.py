from pathlib import Path
from types import SimpleNamespace

import pytest

from admitflow.adapters.sqlite import Repository
from admitflow.adapters.telegram import callback_handler, start_command, text_handler
from admitflow.adapters.vector_store import VectorStore
from admitflow.services.admissions import AdmissionsService
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


@pytest.mark.asyncio
async def test_start_command_creates_lead_and_sends_course_options(tmp_path: Path) -> None:
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
    assert "fictional sample information" in message.sent[0][0]
    assert message.sent[0][1] is not None
    assert (
        "Help me explore" in message.sent[0][0] or "What would be most useful" in message.sent[0][0]
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
    assert "study level" in message.sent[-1][0]

    async def answer_level() -> None:
        return None

    update.callback_query = SimpleNamespace(answer=answer_level, data="level:any")
    update.update_id = 112
    await callback_handler(update, context)
    assert "activity sounds most interesting" in message.sent[-1][0]

    async def answer_skip_activity() -> None:
        return None

    update.callback_query = SimpleNamespace(answer=answer_skip_activity, data="activity:skip")
    update.update_id = 113
    await callback_handler(update, context)
    assert "Here are sample options" in message.sent[-1][0]

    async def answer_language() -> None:
        return None

    update.callback_query = SimpleNamespace(answer=answer_language, data="language:ml")
    update.update_id = 114
    await callback_handler(update, context)
    lead = repository.list_leads(repository.tenant_id)[0]
    assert lead["preferred_language"] == "ml"
    assert message.sent[-1][0]


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
