from __future__ import annotations

from collections.abc import Callable

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database.models import Organization as ORMOrganization
from app.database.session import SessionLocal
from app.domain.organization import Organization
from app.exceptions.exceptions import PersistenceDataException


def _to_domain(
    organization: ORMOrganization,
) -> Organization:
    return Organization(
        organization_id=organization.organization_id,
        name=organization.name,
        code=organization.code,
        industry=organization.industry,
        contact_email=organization.contact_email,
        is_active=organization.is_active,
        created_at=organization.created_at,
    )


class OrganizationRepository:
    """
    Persistence layer for organization tenants.

    This repository follows the established Atlas
    architecture: repository isolation, session factory
    injection, SQLAlchemy exception handling, and ORM ↔
    domain conversion.
    """

    def __init__(
        self,
        session_factory: Callable[[], Session] = SessionLocal,
    ) -> None:
        self.session_factory = session_factory

    def create(
        self,
        organization: Organization,
    ) -> Organization:
        record = ORMOrganization(
            organization_id=organization.organization_id,
            name=organization.name,
            code=organization.code,
            industry=organization.industry,
            contact_email=organization.contact_email,
            is_active=organization.is_active,
            created_at=organization.created_at,
        )

        try:
            with self.session_factory() as session:
                with session.begin():
                    session.add(record)

        except SQLAlchemyError as exc:
            raise PersistenceDataException(
                "Organization could not be created."
            ) from exc

        return organization

    def create_in_session(
        self,
        session: Session,
        organization: Organization,
    ) -> Organization:
        """
        Create an organization using an existing
        database session.
        """

        record = ORMOrganization(
            organization_id=organization.organization_id,
            name=organization.name,
            code=organization.code,
            industry=organization.industry,
            contact_email=organization.contact_email,
            is_active=organization.is_active,
            created_at=organization.created_at,
        )

        session.add(record)

        return organization

    def list_all(
        self,
    ) -> list[Organization]:
        statement = select(
            ORMOrganization,
        ).order_by(
            ORMOrganization.name.asc(),
        )

        try:
            with self.session_factory() as session:
                organizations = session.scalars(
                    statement,
                ).all()

        except SQLAlchemyError as exc:
            raise PersistenceDataException(
                "Organizations could not be loaded."
            ) from exc

        return [
            _to_domain(item)
            for item in organizations
        ]

    def get_by_id(
        self,
        organization_id: str,
    ) -> Organization | None:
        try:
            with self.session_factory() as session:
                organization = session.get(
                    ORMOrganization,
                    organization_id,
                )

        except SQLAlchemyError as exc:
            raise PersistenceDataException(
                "Organization could not be loaded."
            ) from exc

        if organization is None:
            return None

        return _to_domain(organization)

    def get_by_name(
        self,
        name: str,
    ) -> Organization | None:
        statement = select(
            ORMOrganization,
        ).where(
            ORMOrganization.name == name,
        )

        try:
            with self.session_factory() as session:
                organization = session.scalars(
                    statement,
                ).first()

        except SQLAlchemyError as exc:
            raise PersistenceDataException(
                "Organization could not be loaded."
            ) from exc

        if organization is None:
            return None

        return _to_domain(organization)

    def get_by_code(
        self,
        code: str,
    ) -> Organization | None:
        statement = select(
            ORMOrganization,
        ).where(
            ORMOrganization.code == code,
        )

        try:
            with self.session_factory() as session:
                organization = session.scalars(
                    statement,
                ).first()

        except SQLAlchemyError as exc:
            raise PersistenceDataException(
                "Organization could not be loaded."
            ) from exc

        if organization is None:
            return None

        return _to_domain(organization)

    def update_configuration(
        self,
        organization_id: str,
        *,
        name: str,
        industry: str,
        contact_email: str,
    ) -> Organization | None:
        """
        Update the configurable profile fields of an organization.

        Tenant identity, organization code, lifecycle state,
        and creation metadata are intentionally not modified.
        """

        try:
            with self.session_factory() as session:
                with session.begin():
                    organization = session.get(
                        ORMOrganization,
                        organization_id,
                    )

                    if organization is None:
                        return None

                    organization.name = name
                    organization.industry = industry
                    organization.contact_email = contact_email

                    session.flush()
                    session.refresh(organization)

                    return _to_domain(organization)

        except SQLAlchemyError as exc:
            raise PersistenceDataException(
                "Organization configuration could not be updated."
            ) from exc

    def update_active_status(
        self,
        organization_id: str,
        *,
        is_active: bool,
    ) -> Organization | None:
        """
        Update the lifecycle status of an organization.

        Returns the updated organization when found,
        otherwise returns None.
        """

        try:
            with self.session_factory() as session:
                with session.begin():
                    organization = session.get(
                        ORMOrganization,
                        organization_id,
                    )

                    if organization is None:
                        return None

                    organization.is_active = is_active

                    session.flush()
                    session.refresh(organization)

                    return _to_domain(organization)

        except SQLAlchemyError as exc:
            raise PersistenceDataException(
                "Organization lifecycle status could not be updated."
            ) from exc