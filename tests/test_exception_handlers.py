from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.exceptions import AppException, ValidationException, register_exception_handlers
from main import app as main_app


def test_main_app_registers_app_exception_handler():
    assert AppException in main_app.exception_handlers


def test_registered_handler_returns_structured_error_response():
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/boom")
    async def boom():
        raise ValidationException("invalid input")

    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/boom")

    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "validation_error",
            "message": "invalid input",
        }
    }
