import uuid
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from src.db.enums import LeadStatus, RuleOperator
from src.db.models.catalog import QualificationRule
from src.engine.nodes.qualification import run_qualification
from src.engine.state import EngineState


@pytest.fixture
def base_state() -> EngineState:
    return EngineState(
        lead_id=uuid.uuid4(),
        tenant_id=uuid.uuid4(),
        status=LeadStatus.QUALIFYING,
        current_course_id=uuid.uuid4(),
        conversation_history=[
            {"role": "user", "content": "I am 18 years old."},
        ],
    )


class MockResult:
    def __init__(self, items: list[Any]) -> None:
        self.items = items

    def scalars(self) -> "MockResult":
        return self

    def all(self) -> list[Any]:
        return self.items


@pytest.mark.asyncio
async def test_qualification_no_course() -> None:
    state = EngineState(
        lead_id=uuid.uuid4(),
        tenant_id=uuid.uuid4(),
        status=LeadStatus.QUALIFYING,
        current_course_id=None,
    )
    db = AsyncMock()
    sender = AsyncMock()

    new_state = await run_qualification(state, db, sender, "1234")
    assert new_state.status == LeadStatus.DISCOVERING
    sender.send_text.assert_called_once()


@pytest.mark.asyncio
async def test_qualification_no_rules(base_state: EngineState) -> None:
    db = AsyncMock()
    db.execute.return_value = MockResult([])
    sender = AsyncMock()

    new_state = await run_qualification(base_state, db, sender, "1234")
    assert new_state.status == LeadStatus.ADMISSION_READY
    sender.send_text.assert_called_once()
    assert "qualify" in sender.send_text.call_args[1]["text"].lower()


@pytest.mark.asyncio
async def test_qualification_missing_fields(base_state: EngineState) -> None:
    rule = QualificationRule(
        field="age",
        operator=RuleOperator.GTE,
        value=16,
    )
    db = AsyncMock()
    db.execute.return_value = MockResult([rule])
    sender = AsyncMock()

    class MockMessage:
        content = '{"extracted_fields": {}, "next_question": "How old are you?"}'

    class MockChoice:
        message = MockMessage()

    class MockResponse:
        choices = [MockChoice()]

    with patch(
        "src.engine.nodes.qualification.generate_completion", new_callable=AsyncMock
    ) as mock_llm:
        mock_llm.return_value = MockResponse()
        new_state = await run_qualification(base_state, db, sender, "1234")

        assert new_state.status == LeadStatus.QUALIFYING
        sender.send_text.assert_called_with(to="1234", text="How old are you?")


@pytest.mark.asyncio
async def test_qualification_extracts_and_passes(base_state: EngineState) -> None:
    rule = QualificationRule(
        field="age",
        operator=RuleOperator.GTE,
        value=16,
    )
    db = AsyncMock()
    db.execute.return_value = MockResult([rule])
    sender = AsyncMock()

    class MockMessage:
        content = '{"extracted_fields": {"age": 18}, "next_question": null}'

    class MockChoice:
        message = MockMessage()

    class MockResponse:
        choices = [MockChoice()]

    with patch(
        "src.engine.nodes.qualification.generate_completion", new_callable=AsyncMock
    ) as mock_llm:
        mock_llm.return_value = MockResponse()
        new_state = await run_qualification(base_state, db, sender, "1234")

        assert new_state.status == LeadStatus.ADMISSION_READY
        assert new_state.extracted_facts["age"] == 18
        sender.send_text.assert_called_once()


@pytest.mark.asyncio
async def test_qualification_extracts_and_fails(base_state: EngineState) -> None:
    rule = QualificationRule(
        field="age",
        operator=RuleOperator.GTE,
        value=21,
    )
    db = AsyncMock()
    db.execute.return_value = MockResult([rule])
    sender = AsyncMock()

    class MockMessage:
        content = '{"extracted_fields": {"age": 18}, "next_question": null}'

    class MockChoice:
        message = MockMessage()

    class MockResponse:
        choices = [MockChoice()]

    with patch(
        "src.engine.nodes.qualification.generate_completion", new_callable=AsyncMock
    ) as mock_llm:
        mock_llm.return_value = MockResponse()
        new_state = await run_qualification(base_state, db, sender, "1234")

        assert new_state.status == LeadStatus.DISCOVERING
        assert new_state.extracted_facts["age"] == 18
        sender.send_text.assert_called_once()
        assert "don't meet" in sender.send_text.call_args[1]["text"].lower()
