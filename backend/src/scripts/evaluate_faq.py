"""Bounded live FAQ evaluation on the fictional demo tenant; no messages or writes."""

import asyncio
import json
import uuid
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict
from sqlalchemy import select

from src.core.settings import get_settings
from src.db.models import Course, Institution, Lead
from src.db.session import get_engine, get_sessionmaker
from src.engine.contracts import Reply
from src.engine.journey import answer_question, copy

REFERENCE = "synthetic-campus-reference.txt"


class Case(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    language: Literal["en", "hi", "hinglish", "ml"]
    question: str
    expected: str | None


def score_answer(case: Case, answer: Reply) -> bool:
    if case.expected is None:
        return answer.text == copy("unknown", {"language": case.language}) and answer.source is None
    return (
        answer.source is not None
        and answer.source.relative_path == REFERENCE
        and case.expected.casefold() in answer.text.casefold()
        and "Source:" not in answer.text
        and REFERENCE not in answer.text
    )


def cases() -> list[Case]:
    questions: dict[Literal["en", "hi", "hinglish", "ml"], list[str]] = {
        "en": [
            "Where is the demo campus?",
            "When is the library open?",
            "Is hostel accommodation available?",
            "What is the campus Wi-Fi password?",
            "Does the institution guarantee a job?",
            "Can I visit the moon?",
        ],
        "hi": [
            "डेमो कैंपस कहाँ है?",
            "पुस्तकालय कब खुलता है?",
            "क्या हॉस्टल की सुविधा उपलब्ध है?",
            "कैंपस के वाई-फाई का पासवर्ड क्या है?",
            "क्या संस्था नौकरी की गारंटी देती है?",
            "क्या मैं चाँद पर जा सकता हूँ?",
        ],
        "hinglish": [
            "Demo campus kahan hai?",
            "Library kab khulti hai?",
            "Hostel accommodation available hai?",
            "Campus Wi-Fi ka password kya hai?",
            "Kya institution job guarantee deta hai?",
            "Kya main moon par ja sakta hoon?",
        ],
        "ml": [
            "ഡെമോ ക്യാമ്പസ് എവിടെയാണ്?",
            "ലൈബ്രറി എപ്പോഴാണ് തുറക്കുന്നത്?",
            "ഹോസ്റ്റൽ സൗകര്യം ലഭ്യമാണോ?",
            "ക്യാമ്പസിലെ വൈഫൈ പാസ്‌വേഡ് എന്താണ്?",
            "സ്ഥാപനം ജോലി ഉറപ്പുനൽകുന്നുണ്ടോ?",
            "എനിക്ക് ചന്ദ്രനിൽ പോകാമോ?",
        ],
    }
    expected = [
        "The demo campus is in Kochi.",
        "The library is open from 9 AM to 5 PM.",
        "Hostel accommodation is available on campus.",
        None,
        None,
        None,
    ]
    topics = ["campus", "library", "hostel", "wifi", "job", "moon"]
    return [
        Case(
            id=f"{language}-{topics[i]}", language=language, question=question, expected=expected[i]
        )
        for language, items in questions.items()
        for i, question in enumerate(items)
    ]


async def evaluate() -> dict[str, object]:
    results: list[dict[str, object]] = []
    try:
        async with get_sessionmaker()() as db:
            institution = await db.scalar(
                select(Institution).where(
                    Institution.slug == get_settings().telegram_institution_code,
                    Institution.name == "AdmitFlow Demo Institute",
                )
            )
            if institution is None:
                raise ValueError("The fictional demo institution must be seeded first")
            course = await db.scalar(
                select(Course).where(
                    Course.tenant_id == institution.id, Course.name == "Digital Skills Foundation"
                )
            )
            # Transient object only: never add, flush, commit or send a Telegram update.
            lead = Lead(
                id=uuid.uuid4(),
                tenant_id=institution.id,
                current_course_id=course.id if course else None,
            )
            for case in cases():
                try:
                    reply = await asyncio.wait_for(
                        answer_question(db, lead, {"language": case.language}, case.question),
                        timeout=90,
                    )
                    result: dict[str, object] = {
                        "id": case.id,
                        "language": case.language,
                        "expected": "source_quote" if case.expected else "abstention",
                        "passed": score_answer(case, reply),
                    }
                except Exception as error:
                    result = {"id": case.id, "passed": False, "error_type": type(error).__name__}
                results.append(result)
                print(json.dumps(result), flush=True)
            await db.rollback()
    finally:
        await get_engine().dispose()
    return {
        "scope": "24 synthetic live FAQ cases; no fluency, production or statistical claim",
        "provider": "configured OpenAI roles and embeddings",
        "reference": REFERENCE,
        "cases": results,
        "passed": sum(result["passed"] is True for result in results),
        "total": len(results),
        "all_passed": len(results) == 24 and all(result["passed"] is True for result in results),
    }


def main() -> None:
    try:
        report = asyncio.run(evaluate())
    except Exception as error:
        print(json.dumps({"status": "failed", "error_type": type(error).__name__}))
        raise SystemExit(1) from None
    target = Path(__file__).resolve().parents[3] / "docs/event/EVALUATION_RESULTS.json"
    target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "total": report["total"]}))
    if not report["all_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
