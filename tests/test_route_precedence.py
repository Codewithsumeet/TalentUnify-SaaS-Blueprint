from fastapi.routing import APIRoute

from main import app


def _get_route(path: str, method: str) -> APIRoute:
    for route in app.routes:
        if isinstance(route, APIRoute) and route.path == path and method in route.methods:
            return route
    raise AssertionError(f"Route not found: {method} {path}")


def test_candidate_detail_route_is_uuid_scoped_and_auth_protected():
    route = _get_route("/api/v1/candidates/{candidate_id:uuid}", "GET")
    dependency_names = {
        dependency.call.__name__
        for dependency in route.dependant.dependencies
        if dependency.call is not None
    }

    assert route.endpoint.__module__ == "candidate.router"
    assert "get_current_user" in dependency_names


def test_candidate_upload_route_still_exists_as_static_path():
    route = _get_route("/api/v1/candidates/upload", "POST")
    assert route.endpoint.__module__ == "api.routes"
