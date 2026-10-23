"""Engine state definition (Task 8).

Defines the plain dataclass/Pydantic model loaded per turn and enforces
lead lifecycle state transitions.
"""

from __future__ import annotations

import uuid
from typing import Any

from pydantic import BaseModel, Field

from src.db.enums import LeadStatus


class InvalidTransitionError(ValueError):
    """Raised when an invalid state transition is attempted."""


# Defined allowed transitions based on SPEC §7.3
VALID_TRANSITIONS: dict[LeadStatus, set[LeadStatus]] = {
    LeadStatus.NEW: {
        LeadStatus.DISCOVERING,
        LeadStatus.QUALIFYING,
        LeadStatus.HANDED_OFF,
        LeadStatus.COLD,
    },
    LeadStatus.DISCOVERING: {
        LeadStatus.QUALIFYING,
        LeadStatus.HANDED_OFF,
        LeadStatus.COLD,
    },
    LeadStatus.QUALIFYING: {
        LeadStatus.DISCOVERING,
        LeadStatus.ADMISSION_READY,
        LeadStatus.HANDED_OFF,
        LeadStatus.COLD,
    },
    LeadStatus.ADMISSION_READY: {
        LeadStatus.FORM_COLLECTING,
        LeadStatus.HANDED_OFF,
        LeadStatus.COLD,
    },
    LeadStatus.FORM_COLLECTING: {
        LeadStatus.PAYMENT_PENDING,
        LeadStatus.HANDED_OFF,
        LeadStatus.COLD,
    },
    LeadStatus.PAYMENT_PENDING: {
        LeadStatus.UNDER_REVIEW,
        LeadStatus.HANDED_OFF,
        LeadStatus.COLD,
    },
    LeadStatus.UNDER_REVIEW: {
        LeadStatus.ENROLLED,
        LeadStatus.REJECTED,
        LeadStatus.WAITLISTED,
    },
    LeadStatus.ENROLLED: set(),
    LeadStatus.REJECTED: set(),
    LeadStatus.WAITLISTED: {
        LeadStatus.ENROLLED,
        LeadStatus.REJECTED,
    },
    LeadStatus.HANDED_OFF: {
        # 'Resume AI' can drop them back into discovery or qualifying
        LeadStatus.DISCOVERING,
        LeadStatus.QUALIFYING,
        LeadStatus.FORM_COLLECTING,
    },
    LeadStatus.COLD: {
        # Re-engagement can restart their flow
        LeadStatus.DISCOVERING,
        LeadStatus.QUALIFYING,
    },
}


class EngineState(BaseModel):
    """The conversation state loaded from the DB per turn.

    This is not a LangGraph checkpointer state. This is a plain typed schema
    that is populated by reading the `leads`, `lead_facts`, and `messages`
    tables at the start of a turn, mutated during `handle_turn()`, and flushed
    back to the DB at the end.
    """

    lead_id: uuid.UUID
    tenant_id: uuid.UUID
    status: LeadStatus = Field(default=LeadStatus.NEW)

    # Message objects or dicts representing the chat history
    conversation_history: list[dict[str, Any]] = Field(default_factory=list)

    # Semantic memory (facts extracted by Qualification node)
    extracted_facts: dict[str, Any] = Field(default_factory=dict)

    current_course_id: uuid.UUID | None = None
    current_batch_id: uuid.UUID | None = None

    copilot_mode: bool = False

    # E.g., 'initial', 'deep_dive', 'objection_handling' (from spec)
    consult_stage: str | None = None

    pending_order_id: uuid.UUID | None = None
    applied_discount_id: uuid.UUID | None = None

    def transition_to(self, new_status: LeadStatus) -> None:
        """Safely transition the lead to a new lifecycle status.

        Raises:
            InvalidTransitionError: If the transition is not allowed by SPEC.
        """
        if new_status == self.status:
            return  # No-op

        allowed = VALID_TRANSITIONS.get(self.status, set())
        if new_status not in allowed:
            raise InvalidTransitionError(
                f"Cannot transition from {self.status.value} to {new_status.value}"
            )

        self.status = new_status
