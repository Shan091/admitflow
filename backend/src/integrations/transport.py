"""HTTPS delivery pins a public resolved address while retaining TLS host verification."""

import asyncio
import hashlib
import hmac
import ipaddress
import logging
import re
import socket
from contextvars import ContextVar
from urllib.parse import SplitResult, urlsplit, urlunsplit

import httpx2 as httpx

_private_delivery: ContextVar[bool] = ContextVar("private_webhook_delivery", default=False)


class PrivateTransportLogs(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return not (_private_delivery.get() and record.name.startswith(("httpx", "httpcore")))


def protect_logs() -> None:
    # Suppress only this async delivery's HTTP traces, which could contain secret
    # URL paths/query strings or echoed response headers. Other calls retain logs.
    loggers = [logging.getLogger(name) for name in ("httpx", "httpx2", "httpcore", "httpcore2")]
    loggers.extend(
        item
        for name, item in list(logging.Logger.manager.loggerDict.items())
        if name.startswith(("httpx", "httpcore")) and isinstance(item, logging.Logger)
    )
    for target in [*loggers, *logging.getLogger().handlers]:
        if not any(isinstance(item, PrivateTransportLogs) for item in target.filters):
            target.addFilter(PrivateTransportLogs())


def public_ip(address: str) -> bool:
    try:
        value = ipaddress.ip_address(address)
        return value.is_global and not value.is_multicast and not value.is_unspecified
    except ValueError:
        return False


def destination(url: str) -> SplitResult:
    if any(ord(c) < 33 for c in url) or "\\" in url:
        raise ValueError("Use an HTTPS URL without spaces or control characters.")
    parsed = urlsplit(url)
    host = parsed.hostname
    if (
        parsed.scheme != "https"
        or not host
        or parsed.username
        or parsed.password
        or parsed.fragment
        or parsed.port not in (None, 443)
    ):
        raise ValueError("Use a public HTTPS URL on port 443 without credentials or a fragment.")
    host = host.encode("idna").decode("ascii").lower()
    try:
        ipaddress.ip_address(host)
    except ValueError:
        if (
            not re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]{0,251}[a-z0-9])?", host)
            or "." not in host
            or host.endswith((".localhost", ".local", ".internal"))
        ):
            raise ValueError("Use a public fully qualified hostname.") from None
    else:
        if not public_ip(host):
            raise ValueError("Internal or reserved network destinations are not allowed.")
    authority = f"[{host}]" if ":" in host else host
    return parsed._replace(netloc=authority)


async def resolve_public(hostname: str) -> str:
    async with asyncio.timeout(5):
        results = await asyncio.get_running_loop().getaddrinfo(
            hostname, 443, type=socket.SOCK_STREAM
        )
    addresses = [str(result[4][0]) for result in results]
    if not addresses or not all(public_ip(address) for address in addresses):
        raise ValueError("Destination resolution includes an internal or reserved address.")
    return addresses[0]


def signature(secret: str, timestamp: str, body: bytes) -> str:
    return (
        "v1="
        + hmac.new(secret.encode(), timestamp.encode() + b"." + body, hashlib.sha256).hexdigest()
    )


async def post_event(url: str, secret: str, delivery_id: str, timestamp: str, body: bytes) -> int:
    target = destination(url)
    host = target.hostname
    assert host is not None
    address = await resolve_public(host)
    pinned = target._replace(netloc=f"[{address}]" if ":" in address else address)
    # Resolve exactly once. Reconnecting cannot resolve the hostname to a private IP.
    # The Host header and SNI keep certificate verification bound to the original host.
    token = _private_delivery.set(True)
    try:
        async with (
            asyncio.timeout(20),
            httpx.AsyncClient(timeout=10, follow_redirects=False, trust_env=False) as client,
        ):
            protect_logs()
            async with client.stream(
                "POST",
                urlunsplit(pinned),
                content=body,
                headers={
                    "Host": target.netloc,
                    "Content-Type": "application/json",
                    "X-AdmitFlow-Delivery": delivery_id,
                    "X-AdmitFlow-Timestamp": timestamp,
                    "X-AdmitFlow-Signature": signature(secret, timestamp, body),
                },
                extensions={"sni_hostname": host},
            ) as response:
                return response.status_code
    finally:
        _private_delivery.reset(token)
