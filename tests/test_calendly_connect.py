import asyncio
from contextlib import asynccontextmanager
from urllib.parse import parse_qs, urlparse

from fastapi.responses import RedirectResponse

from routers import calendly as calendly_router
from integrations.calendly import token_store


def test_calendly_connect_redirects_to_mock_mode_when_oauth_missing(monkeypatch):
    monkeypatch.setattr(calendly_router.settings, "calendly_client_id", "")
    monkeypatch.setattr(calendly_router.settings, "calendly_redirect_uri", "")
    monkeypatch.setattr(calendly_router.settings, "calendly_mock_mode", True)
    monkeypatch.setattr(calendly_router.settings, "frontend_url", "http://localhost:3000")

    response = asyncio.run(calendly_router.calendly_connect())

    assert isinstance(response, RedirectResponse)
    assert response.headers["location"] == "http://localhost:3000/integrations?calendly=mock-connected"


def test_calendly_connect_redirects_to_not_configured_when_mock_disabled(monkeypatch):
    monkeypatch.setattr(calendly_router.settings, "calendly_client_id", "")
    monkeypatch.setattr(calendly_router.settings, "calendly_redirect_uri", "")
    monkeypatch.setattr(calendly_router.settings, "calendly_mock_mode", False)
    monkeypatch.setattr(calendly_router.settings, "frontend_url", "http://localhost:3000")

    response = asyncio.run(calendly_router.calendly_connect())

    assert isinstance(response, RedirectResponse)
    assert response.headers["location"] == "http://localhost:3000/integrations?calendly=not-configured"


def test_calendly_connect_passes_return_to_as_state(monkeypatch):
    monkeypatch.setattr(calendly_router.settings, "calendly_client_id", "client-id")
    monkeypatch.setattr(calendly_router.settings, "calendly_redirect_uri", "http://localhost:8000/api/v1/integration/calendly/callback")

    response = asyncio.run(calendly_router.calendly_connect("http://127.0.0.1:3000/integrations"))

    assert isinstance(response, RedirectResponse)
    location = response.headers["location"]
    parsed = urlparse(location)
    query = parse_qs(parsed.query)
    assert parsed.scheme == "https"
    assert parsed.netloc == "auth.calendly.com"
    assert query["state"] == ["http://127.0.0.1:3000/integrations"]


class _FakeHttpResponse:
    def __init__(self, status_code: int, payload: dict | None = None, text: str = ""):
        self.status_code = status_code
        self._payload = payload or {}
        self.text = text

    def json(self):
        return self._payload


class _FakeHttpClient:
    def __init__(self, response: _FakeHttpResponse):
        self._response = response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def post(self, *_args, **_kwargs):
        return self._response


def test_calendly_callback_redirects_to_token_error_when_exchange_fails(monkeypatch):
    monkeypatch.setattr(calendly_router, "httpx", type("HttpxStub", (), {"AsyncClient": lambda **_kwargs: _FakeHttpClient(_FakeHttpResponse(400, text="bad request"))}))

    response = asyncio.run(calendly_router.calendly_callback("sample-code"))

    assert isinstance(response, RedirectResponse)
    assert response.headers["location"] == "http://localhost:3000/integrations?calendly=token-error"


def test_calendly_callback_uses_allowed_state_redirect(monkeypatch):
    monkeypatch.setattr(
        calendly_router,
        "httpx",
        type("HttpxStub", (), {"AsyncClient": lambda **_kwargs: _FakeHttpClient(_FakeHttpResponse(400, text="bad request"))}),
    )

    response = asyncio.run(
        calendly_router.calendly_callback("sample-code", state="http://127.0.0.1:3000/integrations")
    )

    assert isinstance(response, RedirectResponse)
    assert response.headers["location"] == "http://127.0.0.1:3000/integrations?calendly=token-error"


def test_calendly_callback_redirects_to_callback_error_when_token_save_fails(monkeypatch):
    monkeypatch.setattr(
        calendly_router,
        "httpx",
        type(
            "HttpxStub",
            (),
            {"AsyncClient": lambda **_kwargs: _FakeHttpClient(_FakeHttpResponse(200, payload={"access_token": "ok-token"}))},
        ),
    )

    @asynccontextmanager
    async def _fake_db():
        yield object()

    async def _failing_save_tokens(_tokens, _db):
        raise RuntimeError("db write failure")

    monkeypatch.setattr(calendly_router, "get_db", _fake_db)
    monkeypatch.setattr(calendly_router, "save_tokens", _failing_save_tokens)

    response = asyncio.run(calendly_router.calendly_callback("sample-code"))

    assert isinstance(response, RedirectResponse)
    assert response.headers["location"] == "http://localhost:3000/integrations?calendly=callback-error"


def test_save_tokens_normalizes_expires_at_to_naive_utc(monkeypatch):
    captured: dict[str, object] = {}

    async def _fake_upsert(db, service, access_token, refresh_token=None, expires_at=None):
        captured["db"] = db
        captured["service"] = service
        captured["access_token"] = access_token
        captured["refresh_token"] = refresh_token
        captured["expires_at"] = expires_at
        return {"ok": True}

    monkeypatch.setattr(token_store, "upsert_service_token", _fake_upsert)

    asyncio.run(
        token_store.save_tokens(
            {"access_token": "token-1", "refresh_token": "refresh-1", "expires_in": 600},
            db=object(),
            service="calendly",
        )
    )

    expires_at = captured["expires_at"]
    assert expires_at is not None
    assert getattr(expires_at, "tzinfo", None) is None
