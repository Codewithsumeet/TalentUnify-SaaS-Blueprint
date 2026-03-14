from fastapi.routing import APIRoute

from main import app


def test_calendly_routes_do_not_depend_on_get_db_context_manager():
    offending_routes: list[str] = []

    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue
        if not route.path.startswith("/api/v1/integration/calendly"):
            continue

        for dependency in route.dependant.dependencies:
            if dependency.call is not None and dependency.call.__name__ == "get_db":
                offending_routes.append(f"{sorted(route.methods)} {route.path}")

    assert offending_routes == []
