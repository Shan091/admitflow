# ADR-010: Triage Fallback Routing (Anti-Spam)

## Status
Accepted


## Context
During the implementation of the Triage Node (Task 11), we needed to decide how the system handles "empty" messages (e.g., WhatsApp media like images without text) or "unclear/chitchat" intents (e.g., a user just saying "hello", "hi", or something out-of-domain). 

Initially, there was a risk of defaulting these unknown intents to the `handoff` state. However, doing so would mean every accidental image upload, stray "hello", or non-actionable message would trigger an immediate escalation to a human agent, completely spamming the institution's staff and defeating the purpose of an AI frontline.

## Decision
We enforce a strict **fallback to discovery** for all unclear, empty, or conversational messages. 

1. **Code-Level Failsafe**: In `src/engine/nodes/triage.py`, if the incoming message is entirely empty (whitespace-only) or if the LLM's structured output fails, the function hardcodes a fallback return of `"discovery"`.
2. **Prompt-Level Enforcement**: The LLM prompt explicitly instructs the classifier: *If the message is a greeting, unclear, or out-of-domain, you MUST classify it as "discovery" so the bot can handle it. DO NOT classify as "handoff" unless the user explicitly demands a human or is angry.*

The `discovery` node is safe because it allows the conversational LLM to reply naturally ("How can I help you today?" or "I didn't quite catch that. Are you looking for courses?"), keeping the user engaged without involving a human.

## Consequences
- **Positive**: Staff are protected from spam. Human agents only see genuine escalations (anger, explicit requests for help, sensitive topics).
- **Positive**: The bot appears more conversational and resilient to users sending random greetings or images.
- **Negative/Risk**: If a user genuinely needs help but communicates it very poorly, they might get looped in `discovery`. However, if they get frustrated, the anger detection (auto-escalation trigger) will eventually catch it and route them to `handoff`.
