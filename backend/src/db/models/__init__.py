"""ORM models package.

Importing this package registers every model on ``Base.metadata`` — Alembic's
``env.py`` imports it so autogenerate and migrations see the full schema.
"""

from src.db.base import Base
from src.db.models.application import Application, PaymentOrder
from src.db.models.audit import AuditLog
from src.db.models.catalog import Batch, Course, DiscountCode, QualificationRule
from src.db.models.conversation import (
    ConversationEvent,
    ConversationMemory,
    ConversationReply,
    HumanRequest,
)
from src.db.models.delivery import OutboundMessage, PaymentEvent
from src.db.models.institution import Institution, StaffUser
from src.db.models.knowledge import Document, DocumentChunk
from src.db.models.lead import Lead, LeadFact, Message
from src.db.models.telegram import TelegramBot, TelegramIdentity
from src.db.models.uploads import KnowledgeUpload, StaffSession

__all__ = [
    "Application",
    "AuditLog",
    "Base",
    "Batch",
    "ConversationEvent",
    "ConversationReply",
    "ConversationMemory",
    "HumanRequest",
    "Course",
    "DiscountCode",
    "Document",
    "DocumentChunk",
    "Institution",
    "KnowledgeUpload",
    "Lead",
    "LeadFact",
    "Message",
    "PaymentOrder",
    "OutboundMessage",
    "PaymentEvent",
    "QualificationRule",
    "StaffUser",
    "StaffSession",
    "TelegramBot",
    "TelegramIdentity",
]
