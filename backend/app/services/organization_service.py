from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from app.domain.organization import Organization
from app.exceptions.exceptions import PersistenceDataException
from app.repositories.organization_repository import OrganizationRepository


class OrganizationService:
    """
    Business logic for organization management within
    the Andiny Atlas enterprise platform.

    This service is responsible for organization
    provisioning, validation, activation, and retrieval.
    """

    def __init__(
        self,
        repository: OrganizationRepository,
    ) -> None:
        self.repository = repository

    def create_organization(
        self,
        *,
        name: str,
        code: str,
        industry: str,
        contact_email: str,
    ) -> Organization:

        normalized_name = name.strip()
        normalized_code = code.strip().upper()
        normalized_email = contact_email.strip().lower()

        if not normalized_name:
            raise PersistenceDataException(
                "Organization name is required."
            )

        if not normalized_code:
            raise PersistenceDataException(
                "Organization code is required."
            )

        existing_by_name = self.repository.get_by_name(
            normalized_name,
        )

        if existing_by_name is not None:
            raise PersistenceDataException(
                "Organization already exists."
            )

        existing_by_code = self.repository.get_by_code(
            normalized_code,
        )

        if existing_by_code is not None:
            raise PersistenceDataException(
                "Organization code already exists."
            )

        organization = Organization(
            organization_id=str(uuid4()),
            name=normalized_name,
            code=normalized_code,
            industry=industry.strip(),
            contact_email=normalized_email,
            is_active=True,
            created_at=datetime.now(UTC),
        )

        return self.repository.create(
            organization,
        )

    def list_organizations(
        self,
    ) -> list[Organization]:
        return self.repository.list_all()

    def get_organization(
        self,
        organization_id: str,
    ) -> Organization | None:
        return self.repository.get_by_id(
            organization_id,
        )