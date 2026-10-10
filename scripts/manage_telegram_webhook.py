"""Register or remove the Telegram webhook using credentials from the local .env file."""

import argparse
import json
import os
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "public_base_url",
        nargs="?",
        help="Public HTTPS origin that forwards to this app, without a path",
    )
    parser.add_argument("--delete", action="store_true", help="Remove the bot's configured webhook")
    args = parser.parse_args()

    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    secret = os.getenv("TELEGRAM_WEBHOOK_SECRET")
    if not token:
        parser.error("TELEGRAM_BOT_TOKEN must be set in the local .env file")
    if args.delete:
        method = "deleteWebhook"
        payload = {"drop_pending_updates": "false"}
    else:
        if not secret:
            parser.error("TELEGRAM_WEBHOOK_SECRET must be set in the local .env file")
        if not args.public_base_url or not args.public_base_url.startswith("https://"):
            parser.error("provide a public HTTPS origin, for example https://bot.example.com")
        method = "setWebhook"
        payload = {
            "url": args.public_base_url.rstrip("/") + "/api/v1/webhooks/telegram",
            "secret_token": secret,
            "allowed_updates": json.dumps(["message", "callback_query"]),
        }

    api_url = f"https://api.telegram.org/bot{token}/{method}"
    try:
        with httpx.Client(timeout=15) as client:
            response = client.post(api_url, data=payload)
            response.raise_for_status()
            result = response.json()
            if not result.get("ok"):
                print(f"Telegram rejected {method}: {result.get('description', 'unknown error')}")
                return 1
            if args.delete:
                print("Telegram webhook removed.")
                return 0

            status_response = client.get(f"https://api.telegram.org/bot{token}/getWebhookInfo")
            status_response.raise_for_status()
            status = status_response.json()
            info = status.get("result", {})
            if not status.get("ok") or info.get("url") != payload["url"]:
                print("Telegram did not report the requested webhook URL after registration.")
                return 1
            print("Telegram webhook registered and verified.")
            print(f"URL: {info['url']}")
            print(f"Pending updates: {info.get('pending_update_count', 0)}")
            if info.get("last_error_message"):
                print(f"Last delivery error: {info['last_error_message']}")
            return 0
    except (httpx.HTTPError, ValueError) as exc:
        print(f"Telegram webhook request failed: {type(exc).__name__}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
