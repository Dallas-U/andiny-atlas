from datetime import UTC, datetime
from uuid import uuid4

from app.core.jwt import create_access_token
from app.core.security import (
    hash_password,
    verify_password,
)
from app.database.models import User
from app.exceptions.exceptions import (
    InactiveUserException,
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
    """Business logic for authentication."""

    def __init__(
        self,
        repository: UserRepository,
    ):
        self.repository = repository

    def register_user(
        self,
        request: UserCreate,
    ) -> User:
        """Register a new user."""

        normalized_email = request.email.strip().lower()

        existing = self.repository.get_user_by_email(
            normalized_email,
        )

        if existing is not None:
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
            is_active=True,
            created_at=datetime.now(UTC),
        )

        return self.repository.create_user(user)

    def authenticate(
        self,
        request: UserLogin,
    ) -> User:
        """Authenticate a user."""

        normalized_email = request.email.strip().lower()

        user = self.repository.get_user_by_email(
            normalized_email,
        )

        if user is None:
            raise InvalidCredentialsException()

        if not verify_password(
            request.password,
            user.hashed_password,
        ):
            raise InvalidCredentialsException()

        if not user.is_active:
            raise InactiveUserException()

        return user

    def create_token(
        self,
        request: UserLogin,
    ) -> Token:
        """Authenticate a user and issue an access token."""

        user = self.authenticate(request)

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

        return self.repository.get_user_by_id(user_id)
