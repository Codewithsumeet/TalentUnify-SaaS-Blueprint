from fastapi.routing import APIRoute

from main import app


def _get_route(path: str, method: str) -> APIRoute:
    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue
        if route.path == path and method in route.methods:
            return route
    raise AssertionError(f"Route not found: {method} {path}")


def _has_dependency(route: APIRoute, dependency_name: str) -> bool:
    return any(
        dependency.call is not None and dependency.call.__name__ == dependency_name
        for dependency in route.dependant.dependencies
    )


def test_core_ai_routes_require_auth_dependency():
    secured_targets = [
        ("GET", "/api/v1/candidates"),
        ("GET", "/api/v1/candidates/{candidate_id}"),
        ("POST", "/api/v1/candidates/upload"),
        ("POST", "/api/v1/search"),
    ]

    for method, path in secured_targets:
        route = _get_route(path, method)
        assert _has_dependency(route, "get_current_user"), f"Expected auth dependency on {method} {path}"


def test_calendly_connect_route_remains_public():
    route = _get_route("/api/v1/integration/calendly/connect", "GET")
    assert not _has_dependency(route, "get_current_user")
