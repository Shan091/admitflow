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

    assert "Razorpay test-mode" in message.sent[0][0]
    assert "₹500" in message.sent[0][0]
    assert "https://rzp.io/i/test123" in message.sent[0][0]
    stored_messages = repository.list_messages(lead_id)
    assert stored_messages[-1]["direction"] == "outbound"
    assert "https://rzp.io/i/test123" in stored_messages[-1]["body"]
