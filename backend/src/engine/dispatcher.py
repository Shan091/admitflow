"""Engine Dispatcher (Task 8 & 17).

This module contains the main entry point for the conversation engine,
responsible for loading state, routing the message through guardrails and
nodes, and persisting the updated state.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.mutex import RedisMutex
from src.core.phone import normalize_e164
from src.core.redis import get_redis
from src.core.security import encrypt_pii, hash_phone
from src.db.enums import LeadStatus, MessageDirection
from src.db.models.institution import Institution
from src.db.models.lead import Lead, LeadFact, Message
from src.db.session import get_sessionmaker
from src.engine.nodes.discovery import present_courses
from src.engine.nodes.guardrails import check_input_safety
from src.engine.nodes.qualification import run_qualification
from src.engine.nodes.rag import process_rag_node
from src.engine.nodes.triage import detect_intent
from src.engine.state import EngineState
from src.whatsapp.sender import WhatsAppSender

logger = logging.getLogger(__name__)


async def _load_engine_state(db: AsyncSession, lead: Lead) -> EngineState:
    """Load EngineState from DB records."""
    # Build conversation history
    # The dispatcher needs dicts for conversation_history, so we convert Message objects
    msgs = await db.scalars(
        select(Message)
        .where(Message.lead_id == lead.id)
        .order_by(Message.created_at.asc())
        .limit(20)  # Only load recent history
    )
    history = []
    for m in msgs:
        role = "user" if m.direction == MessageDirection.INBOUND else "assistant"
        history.append({"role": role, "content": m.content or ""})

    # Build facts dict
    facts_result = await db.scalars(select(LeadFact).where(LeadFact.lead_id == lead.id))
    facts = {f.key: f.value for f in facts_result}

    return EngineState(
        lead_id=lead.id,
        tenant_id=lead.tenant_id,
        status=lead.status,
        conversation_history=history,
        extracted_facts=facts,
        current_course_id=lead.current_course_id,
        current_batch_id=lead.current_batch_id,
        copilot_mode=lead.copilot_mode,
    )


async def _flush_engine_state(db: AsyncSession, lead: Lead, state: EngineState) -> None:
    """Flush mutations back to DB records."""
    lead.status = state.status
    lead.current_course_id = state.current_course_id
    lead.current_batch_id = state.current_batch_id
    lead.copilot_mode = state.copilot_mode

    # Upsert facts
    # In a real app we'd merge new facts and issue UPSERT queries
    # For now we'll do a simple loop since this is a prototype
    for key, val in state.extracted_facts.items():
        existing = await db.scalar(
            select(LeadFact).where(LeadFact.lead_id == lead.id, LeadFact.key == key)
        )
        if existing:
            existing.value = val
        else:
            new_fact = LeadFact(
                tenant_id=lead.tenant_id,
                lead_id=lead.id,
                key=key,
                value=val,
            )
            db.add(new_fact)


async def handle_turn(payload: dict[str, Any]) -> None:
    """Process a single turn of conversation."""
    metadata = payload.get("metadata", {})
    phone_number_id = metadata.get("phone_number_id")
    if not phone_number_id:
        logger.warning("No phone_number_id in payload")
        return

    messages = payload.get("messages", [])
    if not messages:
        return

    msg = messages[0]
    user_phone_raw = msg.get("from")
    if not user_phone_raw:
        return

    try:
        user_phone = normalize_e164(user_phone_raw)
    except Exception as e:
        logger.error(f"Invalid phone number {user_phone_raw}: {e}")
        return

    text_dict = msg.get("text", {})
    text_body = text_dict.get("body", "").strip()
    wa_message_id = msg.get("id")

    redis = get_redis()
    async with RedisMutex(redis, f"wa_mutex:{user_phone}"):
        async with get_sessionmaker()() as db:
            # 1. Fetch Tenant
            inst = await db.scalar(
                select(Institution).where(Institution.whatsapp_phone_number_id == phone_number_id)
            )
            if not inst:
                logger.warning(f"No institution found for phone_number_id {phone_number_id}")
                return

            tenant_id = inst.id
            phone_h = hash_phone(user_phone)

            # 2. Fetch or Create Lead
            lead = await db.scalar(
                select(Lead).where(Lead.tenant_id == tenant_id, Lead.phone_hash == phone_h)
            )

            now = datetime.now(UTC)
            if not lead:
                # We need phone_enc, name_enc (assume we just pass text to encrypt_pii)
                # For Task 17, we'll create the lead
                profile = payload.get("contacts", [{}])[0].get("profile", {})
                name_raw = profile.get("name", "")

                lead = Lead(
                    tenant_id=tenant_id,
                    phone_hash=phone_h,
                    phone_enc=encrypt_pii(user_phone),
                    name_enc=encrypt_pii(name_raw) if name_raw else None,
                    status=LeadStatus.NEW,
                )
                db.add(lead)
                await db.flush()  # flush to get lead.id

            lead.last_inbound_at = now

            # Save incoming message
            inbound_msg = Message(
                tenant_id=tenant_id,
                lead_id=lead.id,
                direction=MessageDirection.INBOUND,
                wa_message_id=wa_message_id,
                msg_type="text",
                content=text_body,
            )
            db.add(inbound_msg)
            await db.flush()

            # 3. Load Engine State
            state = await _load_engine_state(db, lead)

            # Setup Sender
            sender = WhatsAppSender()

            # 4. Input Guardrail
            safety = await check_input_safety(text_body)
            if not safety.is_safe:
                if safety.refusal_message:
                    await sender.send_text(to=user_phone, text=safety.refusal_message)
                    # We could save outbound message here
                await db.commit()
                return

            # 5. Triage
            intent = await detect_intent(text_body)

            # 6. Route to Nodes
            if intent == "discovery":
                state = await present_courses(state, db, sender, user_phone)
            elif intent == "rag":
                state = await process_rag_node(state, db, sender, user_phone)
            elif intent == "qualification":
                state = await run_qualification(state, db, sender, user_phone)
            elif intent == "handoff":
                try:
                    state.transition_to(LeadStatus.HANDED_OFF)
                except Exception:
                    pass
                await sender.send_text(
                    to=user_phone,
                    text=(
                        "I've requested a human counselor to join this chat. "
                        "Someone will be with you shortly."
                    ),
                )

            lead.last_outbound_at = datetime.now(UTC)

            # 7. Flush state back
            await _flush_engine_state(db, lead, state)
            await db.commit()
