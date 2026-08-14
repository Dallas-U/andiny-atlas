from __future__ import annotations

from datetime import datetime
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

        existing = self.repository.get_by_name(name)

        if existing is not None:
            raise PersistenceDataException(
                "Organization already exists."
            )

        organization = Organization(
            organization_id=str(uuid4()),
            name=name,
            code=code,
            industry=industry,
            contact_email=contact_email,
            is_active=True,
            created_at=datetime.utcnow(),
        )

        return self.repository.create(organization)

    def list_organizations(self) -> list[Organization]:
        return self.repository.list_all()

    def get_organization(
        self,
        organization_id: str,
    ) -> Organization | None:
        return self.repository.get_by_id(organization_id)