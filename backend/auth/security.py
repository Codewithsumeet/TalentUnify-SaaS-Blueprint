from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import get_settings
from app.exceptions import AuthenticationException

settings = get_settings()
pwd_context = CryptContext(
    # Use a pure-Python default to avoid runtime failures when bcrypt backend
    # is unavailable in local/dev environments.
    schemes=["pbkdf2_sha256", "bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_token(*, subject: str, token_type: str, expires_delta: timedelta) -> str:
    expires_at = datetime.now(timezone.utc) + expires_delta
    payload = {
        "sub": subject,
        "type": token_type,
        "exp": expires_at,
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError as exc:
        raise AuthenticationException("Invalid or expired token") from exc
