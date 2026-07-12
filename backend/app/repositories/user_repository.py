from collections.abc import Callable

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database.models import User
from app.database.session import SessionLocal
from app.exceptions.exceptions import PersistenceDataException
from app.logging.logger import logger


class UserRepository:
    """Handles persistence of application users."""

    def __init__(
        self,
        session_factory: Callable[[], Session] = SessionLocal,
    ):
        self.session_factory = session_factory

    def create_user(self, user: User) -> User:
        """Persist a new user."""

        logger.info(
            "Creating user account for '%s'.",
            user.email,
        )

        try:
            with self.session_factory() as session:
                with session.begin():
                    session.add(user)

                session.refresh(user)

        except SQLAlchemyError as exc:
            logger.exception(
                "User account for '%s' could not be created.",
                user.email,
            )

            raise PersistenceDataException("User account could not be saved.") from exc

        logger.info(
            "User account for '%s' created successfully.",
            user.email,
        )

        return user

    def get_user_by_email(
        self,
        email: str,
    ) -> User | None:
        """Return a user by email address."""

        normalized_email = email.strip().lower()

        try:
            with self.session_factory() as session:
                statement = select(User).where(
                    User.email == normalized_email,
                )

                return session.scalar(statement)

        except SQLAlchemyError as exc:
            logger.exception(
                "User account for '%s' could not be loaded.",
                normalized_email,
            )

            raise PersistenceDataException(
                "User account data could not be read."
            ) from exc

    def get_user_by_id(
        self,
        user_id: str,
    ) -> User | None:
        """Return a user by ID."""

        try:
            with self.session_factory() as session:
                return session.get(
                    User,
                    user_id,
                )

        except SQLAlchemyError as exc:
            logger.exception(
                "User account '%s' could not be loaded.",
                user_id,
            )

            raise PersistenceDataException(
                "User account data could not be read."
            ) from exc
