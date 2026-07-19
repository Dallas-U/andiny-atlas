from collections.abc import Callable

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database.mappers import (
    domain_user_to_orm,
    orm_user_to_domain,
)
from app.database.models import User as ORMUser
from app.database.session import SessionLocal
from app.domain import User
from app.exceptions.exceptions import PersistenceDataException
from app.logging.logger import logger


class UserRepository:
    """Handles persistence of application users."""

    def __init__(
        self,
        session_factory: Callable[[], Session] = SessionLocal,
    ):
        self.session_factory = session_factory

    def create_user(
        self,
        user: User,
    ) -> User:
        """Persist a domain user and return the saved domain entity."""

        logger.info(
            "Creating user account for '%s'.",
            user.email,
        )

        orm_user = domain_user_to_orm(user)

        try:
            with self.session_factory() as session:
                with session.begin():
                    session.add(orm_user)

                session.refresh(orm_user)

                saved_user = orm_user_to_domain(orm_user)

        except SQLAlchemyError as exc:
            logger.exception(
                "User account for '%s' could not be created.",
                user.email,
            )

            raise PersistenceDataException(
                "User account could not be saved."
            ) from exc

        logger.info(
            "User account for '%s' created successfully.",
            user.email,
        )

        return saved_user

    def get_user_by_email(
        self,
        email: str,
    ) -> User | None:
        """Return a domain user by email address."""

        normalized_email = email.strip().lower()

        try:
            with self.session_factory() as session:
                statement = select(ORMUser).where(
                    ORMUser.email == normalized_email,
                )

                orm_user = session.scalar(statement)

                if orm_user is None:
                    return None

                return orm_user_to_domain(orm_user)

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
        """Return a domain user by ID."""

        try:
            with self.session_factory() as session:
                orm_user = session.get(
                    ORMUser,
                    user_id,
                )

                if orm_user is None:
                    return None

                return orm_user_to_domain(orm_user)

        except SQLAlchemyError as exc:
            logger.exception(
                "User account '%s' could not be loaded.",
                user_id,
            )

            raise PersistenceDataException(
                "User account data could not be read."
            ) from exc