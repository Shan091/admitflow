"""Enumerated types used across the schema.

These are Python ``str`` enums mapped to **native Postgres enum types**. Values
are the SPEC's canonical strings (lead lifecycle §7.3, qualification operators
§7.4) so DB rows read the same as the spec and the dashboard.
"""

from __future__ import annotations

import enum


class LeadStatus(enum.StrEnum):
    """Lead lifecycle states (SPEC §7.3).

    Where a lead *stands*, not a fixed track — the engine moves leads between
    these adaptively; only money/hard-eligibility transitions are code-decided.
    """

    NEW = "new"
    DISCOVERING = "discovering"
    QUALIFYING = "qualifying"
    ADMISSION_READY = "admission_ready"
    FORM_COLLECTING = "form_collecting"
    PAYMENT_PENDING = "payment_pending"
    UNDER_REVIEW = "under_review"
    ENROLLED = "enrolled"
    REJECTED = "rejected"
    WAITLISTED = "waitlisted"
    HANDED_OFF = "handed_off"
    COLD = "cold"


class StaffRole(enum.StrEnum):
    """Dashboard access role (SPEC — admin vs agent)."""

    ADMIN = "admin"
    AGENT = "agent"


class RuleOperator(enum.StrEnum):
    """Qualification-rule comparison operators (SPEC §7.4).

    Evaluated deterministically in code (ADR-006) — the LLM only extracts the
    field value; it never decides the outcome.
    """

    GTE = ">="
    LTE = "<="
    EQ = "="
    NEQ = "!="
    GT = ">"
    LT = "<"
    IN = "in"
    NOT_IN = "not_in"


class DiscountType(enum.StrEnum):
    """How a discount code reduces the fee."""

    PERCENT = "percent"
    FLAT = "flat"


class MessageDirection(enum.StrEnum):
    """Direction of a WhatsApp message row (episodic memory, ADR-004)."""

    INBOUND = "inbound"
    OUTBOUND = "outbound"


class PaymentStatus(enum.StrEnum):
    """Payment order lifecycle (SPEC §7.10)."""

    CREATED = "created"
    LINK_SENT = "link_sent"
    PAID = "paid"
    FAILED = "failed"
    WAIVED = "waived"


class ApplicationStatus(enum.StrEnum):
    """Application review status (SPEC §7.9 / lifecycle)."""

    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    WAITLISTED = "waitlisted"
    REJECTED = "rejected"
