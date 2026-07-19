from datetime import UTC, datetime
from uuid import uuid4

from app.core.constants import UserRole
from app.core.jwt import create_access_token
from app.core.security import (
    hash_password,
    verify_password,
)
from app.domain import User
from app.exceptions.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
)
from app.models.user import (
    Token,
    UserCreate,
    UserLogin,
)
from app.repositories.user_repository import UserRepository


class AuthService:
    """Application service responsible for user authentication."""

    def __init__(
        self,
        repository: UserRepository,
    ):
        self._repository = repository

    def register_user(
        self,
        request: UserCreate,
    ) -> User:
        """Register a new user with the default Agent role."""

        normalized_email = request.email.strip().lower()

        existing_user = self._repository.get_user_by_email(
            normalized_email,
        )

        if existing_user is not None:
            raise UserAlreadyExistsException(
                normalized_email,
            )

        user = User(
            id=str(uuid4()),
            full_name=request.full_name.strip(),
            email=normalized_email,
            hashed_password=hash_password(
                request.password,
            ),
            role=UserRole.AGENT,
            is_active=True,
            created_at=datetime.now(
                tz=UTC,
            ),
        )

        return self._repository.create_user(
            user,
        )

    def create_token(
        self,
        request: UserLogin,
    ) -> Token:
        """Authenticate a user and issue an access token."""

        normalized_email = request.email.strip().lower()

        user = self._repository.get_user_by_email(
            normalized_email,
        )

        if user is None:
            raise InvalidCredentialsException()

        if not verify_password(
            request.password,
            user.hashed_password,
        ):
            raise InvalidCredentialsException()

        access_token = create_access_token(
            subject=user.id,
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
        )

    def get_user_by_id(
        self,
        user_id: str,
    ) -> User | None:
        """Return a user by ID."""

        return self._repository.get_user_by_id(
            user_id,
        )