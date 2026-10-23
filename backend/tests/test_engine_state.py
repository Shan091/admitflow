import uuid

import pytest

from src.db.enums import LeadStatus
from src.engine.state import EngineState, InvalidTransitionError


def test_engine_state_initialization() -> None:
    """Test that EngineState can be initialized with required fields."""
    state: EngineState = EngineState(
        lead_id=uuid.uuid4(),
        tenant_id=uuid.uuid4(),
        status=LeadStatus.NEW,
        conversation_history=[],
        extracted_facts={},
    )
    assert state.status == LeadStatus.NEW
    assert state.copilot_mode is False
    assert state.consult_stage is None


def test_valid_state_transitions() -> None:
    """Test allowed state transitions."""
    state: EngineState = EngineState(
        lead_id=uuid.uuid4(),
        tenant_id=uuid.uuid4(),
        status=LeadStatus.NEW,
        conversation_history=[],
        extracted_facts={},
    )

    # NEW -> DISCOVERING
    state.transition_to(LeadStatus.DISCOVERING)
    assert state.status == LeadStatus.DISCOVERING

    # DISCOVERING -> QUALIFYING
    state.transition_to(LeadStatus.QUALIFYING)
    assert state.status == LeadStatus.QUALIFYING  # type: ignore[comparison-overlap]

    # QUALIFYING -> ADMISSION_READY
    state.transition_to(LeadStatus.ADMISSION_READY)
    assert state.status == LeadStatus.ADMISSION_READY

    # Any state to HANDED_OFF
    state.transition_to(LeadStatus.HANDED_OFF)
    assert state.status == LeadStatus.HANDED_OFF


def test_invalid_state_transition() -> None:
    """Test that invalid transitions raise an error."""
    state: EngineState = EngineState(
        lead_id=uuid.uuid4(),
        tenant_id=uuid.uuid4(),
        status=LeadStatus.NEW,
        conversation_history=[],
        extracted_facts={},
    )

    # NEW -> ENROLLED is invalid
    with pytest.raises(InvalidTransitionError, match="Cannot transition from new to enrolled"):
        state.transition_to(LeadStatus.ENROLLED)


def test_cold_transitions() -> None:
    """Test transitions to and from COLD state."""
    state: EngineState = EngineState(
        lead_id=uuid.uuid4(),
        tenant_id=uuid.uuid4(),
        status=LeadStatus.QUALIFYING,
        conversation_history=[],
        extracted_facts={},
    )

    # Any active state -> COLD
    state.transition_to(LeadStatus.COLD)
    assert state.status == LeadStatus.COLD

    # COLD -> DISCOVERING (re-engaged)
    state.transition_to(LeadStatus.DISCOVERING)
    assert state.status == LeadStatus.DISCOVERING  # type: ignore[comparison-overlap]
