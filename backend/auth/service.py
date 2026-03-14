from datetime import timedelta
from uuid import UUID

from app.config import get_settings
from app.exceptions import AuthenticationException, ConflictException
from auth.repository import AuthRepository
from auth.schemas import (
    AuthResponse,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from auth.security import create_token, decode_token, hash_password, verify_password
from db.models import User

settings = get_settings()


class AuthService:
    def __init__(self, repository: AuthRepository) -> None:
        self.repository = repository

    async def register(self, payload: RegisterRequest) -> AuthResponse:
        existing = await self.repository.get_user_by_email(str(payload.email))
        if existing:
            raise ConflictException("User with this email already exists")

        user = await self.repository.create_user(payload, hash_password(payload.password))
        tokens = self._build_token_response(user.id)
        return AuthResponse(user=UserResponse.model_validate(user), tokens=tokens)

    async def login(self, payload: LoginRequest) -> TokenResponse:
        user = await self.repository.get_user_by_email(str(payload.email))
        if not user:
            raise AuthenticationException("Invalid credentials")

        if not verify_password(payload.password, user.password_hash):
            raise AuthenticationException("Invalid credentials")

        return self._build_token_response(user.id)

    async def refresh(self, payload: RefreshRequest) -> TokenResponse:
        token_data = decode_token(payload.refresh_token)
        if token_data.get("type") != "refresh":
            raise AuthenticationException("Invalid refresh token")

        user_id = self._parse_user_id(token_data.get("sub"))
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise AuthenticationException("User not found for token")

        return self._build_token_response(user.id)

    async def get_user_from_access_token(self, token: str) -> User:
        token_data = decode_token(token)
        if token_data.get("type") != "access":
            raise AuthenticationException("Invalid access token")

        user_id = self._parse_user_id(token_data.get("sub"))
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise AuthenticationException("User not found")
        return user

    def _build_token_response(self, user_id: UUID) -> TokenResponse:
        access_expires = timedelta(minutes=settings.access_token_expire_minutes)
        refresh_expires = timedelta(days=settings.refresh_token_expire_days)
        return TokenResponse(
            access_token=create_token(
                subject=str(user_id),
                token_type="access",
                expires_delta=access_expires,
            ),
            refresh_token=create_token(
                subject=str(user_id),
                token_type="refresh",
                expires_delta=refresh_expires,
            ),
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60,
        )

    @staticmethod
    def _parse_user_id(raw_subject: object) -> UUID:
        if not isinstance(raw_subject, str):
            raise AuthenticationException("Invalid token payload")
        try:
            return UUID(raw_subject)
        except ValueError as exc:
            raise AuthenticationException("Invalid token subject") from exc
