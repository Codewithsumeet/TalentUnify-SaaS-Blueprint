from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    def __init__(self, *, status_code: int, message: str, code: str) -> None:
        self.status_code = status_code
        self.message = message
        self.code = code
        super().__init__(message)


class NotFoundException(AppException):
    def __init__(self, message: str) -> None:
        super().__init__(status_code=404, message=message, code="not_found")


class ConflictException(AppException):
    def __init__(self, message: str) -> None:
        super().__init__(status_code=409, message=message, code="conflict")


class AuthenticationException(AppException):
    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(status_code=401, message=message, code="unauthorized")


class ValidationException(AppException):
    def __init__(self, message: str) -> None:
        super().__init__(status_code=400, message=message, code="validation_error")


async def app_exception_handler(_: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            }
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppException, app_exception_handler)
