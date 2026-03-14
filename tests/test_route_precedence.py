from fastapi.routing import APIRoute

from main import app


def _matching_routes(path: str, method: str) -> list[APIRoute]:
    routes: list[APIRoute] = []
    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue
        if route.path != path:
            continue
        if method not in route.methods:
            continue
        routes.append(route)
    return routes


def test_public_candidates_list_route_is_resolved_first():
    routes = _matching_routes("/api/v1/candidates", "GET")
    assert routes
    assert [route.endpoint.__module__ for route in routes] == ["api.routes"]


def test_public_candidate_detail_route_is_resolved_first():
    routes = _matching_routes("/api/v1/candidates/{candidate_id}", "GET")
    assert routes
    assert [route.endpoint.__module__ for route in routes] == ["api.routes"]
