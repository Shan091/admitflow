"""Reject oversized multipart streams before they can fill temporary storage."""

from fastapi import HTTPException
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from src.core.settings import get_settings


class UploadBodyLimit:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http" or not scope.get("path", "").startswith(
            ("/api/knowledge", "/api/staff")
        ):
            await self.app(scope, receive, send)
            return
        cap = (
            get_settings().upload_batch_max_bytes + 1024 * 1024
            if scope.get("path") == "/api/knowledge/documents" and scope.get("method") == "POST"
            else 64 * 1024
        )
        headers = dict(scope.get("headers", []))
        try:
            length = int(headers.get(b"content-length", b"0"))
        except ValueError:
            length = cap + 1
        if length > cap or length < 0:
            await JSONResponse({"detail": "Upload batch is too large."}, status_code=413)(
                scope, receive, send
            )
            return
        size = 0

        async def limited_receive() -> Message:
            nonlocal size
            message = await receive()
            size += len(message.get("body", b""))
            if size > cap:
                raise HTTPException(413, "Upload batch is too large.")
            return message

        async def private_send(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = [
                    (key, value)
                    for key, value in message.get("headers", [])
                    if key.lower() != b"cache-control"
                ]
                headers.append((b"cache-control", b"no-store"))
                message["headers"] = headers
            await send(message)

        await self.app(scope, limited_receive, private_send)
