from fastapi.routing import APIRoute

from main import app


def _route_exists(path: str, method: str) -> bool:
    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue
        if route.path == path and method in route.methods:
            return True
    return False


def test_integration_routes_are_registered():
    expected = [
        ("POST", "/api/v1/intake/gmail-webhook"),
        ("POST", "/api/v1/intake/hrms-push"),
        ("POST", "/api/v1/intake/hrms-demo"),
        ("POST", "/api/v1/intake/linkedin-import"),
        ("POST", "/api/v1/integrations/linkedin/fetch"),
        ("GET", "/api/v1/integration/gmail/connect"),
        ("GET", "/api/v1/integration/gmail/callback"),
        ("POST", "/api/v1/integration/gmail/sync"),
    ]

    missing = [f"{method} {path}" for method, path in expected if not _route_exists(path, method)]
    assert missing == []
