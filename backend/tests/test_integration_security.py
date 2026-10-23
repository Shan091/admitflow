"""Outbound integrations reject unsafe destinations and sign exact delivery bytes."""

import asyncio
import hashlib
import hmac
import logging

import httpx2
import pytest

from src.integrations import transport
from src.integrations.transport import destination, public_ip, signature


@pytest.mark.parametrize(
    "url",
    [
        "http://example.com/hook",
        "https://user:pass@example.com/",
        "https://example.com:444/hook",
        "https://example.com/#fragment",
        "https://localhost/hook",
        "https://127.0.0.1/",
        "https://[::1]/",
        "https://169.254.169.254/",
        "https://example.com\\@localhost/",
    ],
)
def test_unsafe_destination_is_rejected(url):
    with pytest.raises(ValueError):
        destination(url)


@pytest.mark.parametrize(
    "address",
    [
        "127.0.0.1",
        "10.0.0.1",
        "169.254.169.254",
        "::1",
        "::ffff:127.0.0.1",
        "192.168.0.3",
        "100.64.0.1",
        "0.0.0.0",
    ],
)
def test_internal_and_nonpublic_addresses_are_rejected(address):
    assert not public_ip(address)


def test_signature_covers_timestamp_and_exact_body():
    body = b'{"id":"synthetic"}'
    expected = hmac.new(b"test-secret", b"123." + body, hashlib.sha256).hexdigest()
    assert signature("test-secret", "123", body) == "v1=" + expected
    assert signature("test-secret", "124", body) != "v1=" + expected
    assert destination("https://example.com/hook?tenant=a").hostname == "example.com"


async def test_pinned_https_keeps_tls_hostname_and_never_follows_redirects(monkeypatch, caplog):
    original = httpx2.AsyncClient
    calls = []

    async def handler(request):
        calls.append(request)
        assert request.url.host == "8.8.8.8"
        assert request.extensions["sni_hostname"] == "hooks.example.test"
        assert request.headers["host"] == "hooks.example.test"
        assert request.headers["x-admitflow-signature"] == signature(
            "synthetic-secret", "123", b"event"
        )
        return httpx2.Response(302, headers={"Location": "http://127.0.0.1/"})

    def client(**kwargs):
        assert kwargs["trust_env"] is False and kwargs["follow_redirects"] is False
        return original(transport=httpx2.MockTransport(handler), **kwargs)

    async def resolve(_host):
        return "8.8.8.8"

    monkeypatch.setattr(transport, "resolve_public", resolve)
    monkeypatch.setattr(transport.httpx, "AsyncClient", client)
    with caplog.at_level(logging.DEBUG):
        assert (
            await transport.post_event(
                "https://hooks.example.test/private?token=synthetic-url-secret",
                "synthetic-secret",
                "stable-id",
                "123",
                b"event",
            )
            == 302
        )
    assert len(calls) == 1 and "synthetic-url-secret" not in caplog.text


async def test_mixed_public_private_dns_answers_are_blocked(monkeypatch):
    async def resolve(*args, **kwargs):
        return [(2, 1, 6, "", ("8.8.8.8", 443)), (2, 1, 6, "", ("127.0.0.1", 443))]

    monkeypatch.setattr(asyncio.get_running_loop(), "getaddrinfo", resolve)
    with pytest.raises(ValueError):
        await transport.resolve_public("rebind.example.test")
