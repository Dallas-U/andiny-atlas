from collections.abc import Callable

from sqlalchemy import func, select
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

    def create_user_in_session(
        self,
        session: Session,
        user: User,
    ) -> User:
        """Create a user using an existing database session."""

        orm_user = domain_user_to_orm(user)

        session.add(orm_user)

        return user

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
        organization_id: str | None = None,
    ) -> User | None:
        """
        Return a domain user by email.

        When organization_id is supplied, the lookup is tenant-scoped.
        When organization_id is None, the lookup is platform-scoped.

        Platform-scoped lookup must only be used by platform-level
        application services such as Super Admin operations.
        """

        normalized_email = email.strip().lower()

        try:
            with self.session_factory() as session:
                statement = select(ORMUser).where(
                    ORMUser.email == normalized_email,
                )

                if organization_id is not None:
                    statement = statement.where(
                        ORMUser.organization_id == organization_id,
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
        organization_id: str | None = None,
    ) -> User | None:
        """
        Return a domain user by ID.

        When organization_id is supplied, the lookup is tenant-scoped.
        A user outside that organization is therefore invisible to the
        caller.
        """

        try:
            with self.session_factory() as session:
                statement = select(ORMUser).where(
                    ORMUser.id == user_id,
                )

                if organization_id is not None:
                    statement = statement.where(
                        ORMUser.organization_id == organization_id,
                    )

                orm_user = session.scalar(statement)

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

    def list_users(
        self,
        offset: int,
        limit: int,
        organization_id: str | None = None,
    ) -> tuple[list[User], int]:
        """
        Return a page of users and the total number of user records.

        If organization_id is supplied, both the count and the result
        set are restricted to that organization.

        Users are ordered by creation date, newest first. The user ID is
        included as a secondary ordering field to keep pagination stable
        when users have identical creation timestamps.
        """

        try:
            with self.session_factory() as session:
                count_statement = select(
                    func.count(ORMUser.id),
                )

                users_statement = select(
                    ORMUser,
                )

                if organization_id is not None:
                    count_statement = count_statement.where(
                        ORMUser.organization_id == organization_id,
                    )

                    users_statement = users_statement.where(
                        ORMUser.organization_id == organization_id,
                    )

                total = session.scalar(
                    count_statement,
                )

                users_statement = (
                    users_statement
                    .order_by(
                        ORMUser.created_at.desc(),
                        ORMUser.id.asc(),
                    )
                    .offset(offset)
                    .limit(limit)
                )

                orm_users = session.scalars(
                    users_statement,
                ).all()

                users = [
                    orm_user_to_domain(orm_user)
                    for orm_user in orm_users
                ]

                return users, int(total or 0)

        except SQLAlchemyError as exc:
            logger.exception(
                "Application users could not be listed.",
            )

            raise PersistenceDataException(
                "User account data could not be read."
            ) from exc

    def update_user(
        self,
        user: User,
        organization_id: str | None = None,
    ) -> User:
        """
        Update an existing application user.

        If organization_id is supplied, the update is tenant-scoped.
        This prevents a customer administrator from modifying a user
        belonging to another organization.
        """

        try:
            with self.session_factory() as session:
                with session.begin():
                    statement = select(
                        ORMUser,
                    ).where(
                        ORMUser.id == user.id,
                    )

                    if organization_id is not None:
                        statement = statement.where(
                            ORMUser.organization_id == organization_id,
                        )

                    orm_user = session.scalar(statement)

                    if orm_user is None:
                        raise PersistenceDataException(
                            "User not found."
                        )

                    orm_user.full_name = user.full_name
                    orm_user.email = user.email
                    orm_user.hashed_password = user.hashed_password
                    orm_user.role = user.role.value
                    orm_user.organization_id = user.organization_id
                    orm_user.is_active = user.is_active

                session.refresh(orm_user)

                return orm_user_to_domain(orm_user)

        except PersistenceDataException:
            raise

        except SQLAlchemyError as exc:
            logger.exception(
                "User account '%s' could not be updated.",
                user.id,
            )

            raise PersistenceDataException(
                "User account could not be updated."
            ) from exc