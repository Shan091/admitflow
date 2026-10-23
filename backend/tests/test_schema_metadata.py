"""Schema invariants — pure metadata assertions, no database required.

These encode the rules that must hold for every model (ADR-003 tenant scoping,
the SPEC lifecycle enums, money-as-integer) as executable checks that run in
the baseline gate without Postgres.
"""

from __future__ import annotations

import uuid

from sqlalchemy import Integer
from sqlalchemy.orm import configure_mappers

from src.db.enums import LeadStatus, RuleOperator
from src.db.models import (
    Application,
    AuditLog,
    Base,
    Batch,
    ConversationEvent,
    ConversationMemory,
    ConversationReply,
    Course,
    DiscountCode,
    HumanRequest,
    Institution,
    KnowledgeUpload,
    Lead,
    LeadFact,
    Message,
    OutboundMessage,
    PaymentEvent,
    PaymentOrder,
    QualificationRule,
    StaffSession,
    StaffUser,
    TelegramBot,
    TelegramIdentity,
)

# The tenant root has no tenant_id (its own id *is* the tenant).
TENANT_ROOT = "institutions"

EXPECTED_TABLES = {
    "institutions": Institution,
    "staff_users": StaffUser,
    "courses": Course,
    "batches": Batch,
    "qualification_rules": QualificationRule,
    "discount_codes": DiscountCode,
    "leads": Lead,
    "lead_facts": LeadFact,
    "messages": Message,
    "applications": Application,
    "payment_orders": PaymentOrder,
    "audit_logs": AuditLog,
    "telegram_bots": TelegramBot,
    "telegram_identities": TelegramIdentity,
    "knowledge_uploads": KnowledgeUpload,
    "staff_sessions": StaffSession,
    "conversation_events": ConversationEvent,
    "conversation_replies": ConversationReply,
    "conversation_memories": ConversationMemory,
    "human_requests": HumanRequest,
    "outbound_messages": OutboundMessage,
    "payment_events": PaymentEvent,
}


def test_all_core_models_are_registered() -> None:
    registered = set(Base.metadata.tables)
    assert set(EXPECTED_TABLES) <= registered, (
        f"missing tables: {set(EXPECTED_TABLES) - registered}"
    )


def test_every_tenant_scoped_table_has_tenant_id_fk_to_institutions() -> None:
    """ADR-003: every tenant-scoped table carries tenant_id -> institutions.id."""
    for name, table in Base.metadata.tables.items():
        if name == TENANT_ROOT:
            assert "tenant_id" not in table.c, "tenant root must not carry tenant_id"
            continue
        assert "tenant_id" in table.c, f"{name} is missing tenant_id"
        col = table.c["tenant_id"]
        assert not col.nullable, f"{name}.tenant_id must be NOT NULL"
        targets = {fk.column.table.name for fk in col.foreign_keys}
        expected_targets = {
            "telegram_identities": {TENANT_ROOT, "telegram_bots", "leads"},
            "knowledge_uploads": {TENANT_ROOT, "staff_users", "documents"},
            "staff_sessions": {TENANT_ROOT, "staff_users"},
            "conversation_events": {TENANT_ROOT, "telegram_identities"},
            "conversation_replies": {TENANT_ROOT, "conversation_events"},
            "conversation_memories": {TENANT_ROOT, "leads"},
            "human_requests": {TENANT_ROOT, "leads"},
            "outbound_messages": {TENANT_ROOT, "leads"},
            "payment_events": {TENANT_ROOT, "payment_orders"},
            "integration_events": {TENANT_ROOT, "leads"},
            "webhook_deliveries": {TENANT_ROOT, "webhook_endpoints", "integration_events"},
            "notification_receipts": {TENANT_ROOT, "staff_users", "integration_events"},
        }.get(name, {TENANT_ROOT})
        assert targets == expected_targets, f"{name}.tenant_id must enforce tenant ownership"


def test_relationships_resolve() -> None:
    # Raises if any relationship() can't determine its join condition.
    configure_mappers()


def test_every_model_has_uuid_primary_key() -> None:
    for model in EXPECTED_TABLES.values():
        pk_cols = list(model.__table__.primary_key)
        assert len(pk_cols) == 1, f"{model.__name__} must have a single-column PK"
        assert pk_cols[0].name == "id"
        assert pk_cols[0].type.python_type is uuid.UUID


def test_lead_status_covers_all_spec_lifecycle_states() -> None:
    expected = {
        "new",
        "discovering",
        "qualifying",
        "admission_ready",
        "form_collecting",
        "payment_pending",
        "under_review",
        "enrolled",
        "rejected",
        "waitlisted",
        "handed_off",
        "cold",
    }
    assert {s.value for s in LeadStatus} == expected


def test_rule_operator_covers_spec_operator_set() -> None:
    expected = {">=", "<=", "=", "!=", ">", "<", "in", "not_in"}
    assert {o.value for o in RuleOperator} == expected


def test_money_columns_are_integer_minor_units() -> None:
    # Money is integer paise, never float (ADR-006 "code owns the money").
    for column in (
        Course.__table__.c["application_fee"],
        DiscountCode.__table__.c["amount"],
        PaymentOrder.__table__.c["amount"],
    ):
        assert isinstance(column.type, Integer)
