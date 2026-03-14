import asyncio
from urllib.parse import parse_qs, urlparse

from fastapi.responses import RedirectResponse

from integrations.gmail import oauth_router as gmail_router


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


def test_gmail_connect_redirects_to_not_configured_when_oauth_missing(monkeypatch):
    monkeypatch.setattr(gmail_router.settings, "gmail_client_id", "")
    monkeypatch.setattr(gmail_router.settings, "gmail_client_secret", "")
    monkeypatch.setattr(gmail_router.settings, "gmail_redirect_uri", "")
    monkeypatch.setattr(gmail_router.settings, "frontend_url", "http://localhost:3000")

    response = asyncio.run(gmail_router.gmail_connect())

    assert isinstance(response, RedirectResponse)
    assert response.headers["location"] == "http://localhost:3000/integrations?gmail=not-configured"


def test_gmail_connect_passes_return_to_as_state(monkeypatch):
    monkeypatch.setattr(gmail_router.settings, "gmail_client_id", "test-id")
    monkeypatch.setattr(gmail_router.settings, "gmail_client_secret", "test-secret")
    monkeypatch.setattr(gmail_router.settings, "gmail_redirect_uri", "http://localhost:8000/api/v1/integration/gmail/callback")

    response = asyncio.run(gmail_router.gmail_connect("http://127.0.0.1:3000/integrations"))

    assert isinstance(response, RedirectResponse)
    location = response.headers["location"]
    parsed = urlparse(location)
    query = parse_qs(parsed.query)
    assert parsed.scheme == "https"
    assert parsed.netloc == "accounts.google.com"
    assert query["state"] == ["http://127.0.0.1:3000/integrations"]


def test_gmail_callback_redirects_to_token_error_when_exchange_fails(monkeypatch):
    monkeypatch.setattr(gmail_router.settings, "gmail_client_id", "test-id")
    monkeypatch.setattr(gmail_router.settings, "gmail_client_secret", "test-secret")
    monkeypatch.setattr(gmail_router.settings, "gmail_redirect_uri", "http://localhost:8000/api/v1/integration/gmail/callback")
    monkeypatch.setattr(gmail_router.settings, "frontend_url", "http://localhost:3000")
    monkeypatch.setattr(
        gmail_router,
        "httpx",
        type("HttpxStub", (), {"AsyncClient": lambda **_kwargs: _FakeHttpClient(_FakeHttpResponse(400, text="bad request"))}),
    )

    response = asyncio.run(gmail_router.gmail_callback("fake-code", state="http://127.0.0.1:3000/integrations"))

    assert isinstance(response, RedirectResponse)
    assert response.headers["location"] == "http://127.0.0.1:3000/integrations?gmail=token-error"
