"""Bounded live checks; print sanitized results without credentials or update content."""

import argparse
import asyncio
import json
from typing import Literal

from pydantic import BaseModel

from src.core.settings import get_settings
from src.engine.llm_factory import generate_completion
from src.knowledge.processing import embed_chunks
from src.telegram.adapter import TelegramClient


class Probe(BaseModel):
    ready: Literal["ready"]


async def validate(openai: bool, telegram: bool) -> dict[str, object]:
    result: dict[str, object] = {}
    if openai:
        try:
            response = await generate_completion(
                [{"role": "user", "content": 'Return {"ready":"ready"}.'}], response_format=Probe
            )
            Probe.model_validate_json(response.choices[0].message.content)
            vectors = await embed_chunks(["Synthetic admissions reference validation."])
            result["openai"] = {
                "status": "passed",
                "structured_output": True,
                "embedding_dimensions": len(vectors[0]),
            }
        except Exception as error:
            result["openai"] = {"status": "failed", "error_type": type(error).__name__}
    if telegram:
        token = get_settings().telegram_bot_token
        if not token:
            result["telegram"] = {"status": "missing_token"}
        else:
            try:
                client = TelegramClient(token.get_secret_value())
                bot = await client.call("getMe", {})
                hook = await client.call("getWebhookInfo", {})
                result["telegram"] = {
                    "status": "passed",
                    "username": bot.get("username"),
                    "webhook_configured": bool(hook.get("url")),
                }
            except Exception as error:
                result["telegram"] = {"status": "failed", "error_type": type(error).__name__}
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--openai", action="store_true", help="Make two small paid API requests")
    parser.add_argument("--telegram", action="store_true", help="Read bot identity/webhook status")
    args = parser.parse_args()
    if not args.openai and not args.telegram:
        parser.error("Select --openai and/or --telegram")
    result = asyncio.run(validate(args.openai, args.telegram))
    print(json.dumps(result, indent=2))
    if any(isinstance(item, dict) and item.get("status") != "passed" for item in result.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
