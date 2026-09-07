from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.core.constants import UserRole
from app.core.security import hash_password
from app.database.session import SessionLocal
from app.domain import User
from app.domain.organization import Organization
from app.exceptions.exceptions import (
    AuthorizationException,
    PersistenceDataException,
)
from app.models.onboarding import (
    CreateCustomerOrganizationRequest,
    OnboardedOrganizationResponse,
)
from app.repositories.organization_repository import (
    OrganizationRepository,
)
from app.repositories.user_repository import UserRepository


class OnboardingService:
    """
    Application service responsible for customer tenant
    provisioning.

    This service orchestrates:

        1. Organization creation
        2. Initial Customer Administrator creation

    Organization and administrator provisioning occur
    atomically inside one database transaction.

    Platform governance remains restricted to Super Admin.
    """

    def __init__(
        self,
        organization_repository: OrganizationRepository,
        user_repository: UserRepository,
        session_factory: Callable[[], Session] = SessionLocal,
    ) -> None:
        self._organization_repository = (
            organization_repository
        )

        self._user_repository = user_repository

        self._session_factory = session_factory

    def provision_customer_organization(
        self,
        request: CreateCustomerOrganizationRequest,
        *,
        current_user: User,
    ) -> OnboardedOrganizationResponse:
        """
        Provision a complete customer tenant.

        Only Super Admin may execute this operation.

        The following operations occur atomically:

            Organization creation
            Initial Customer Admin creation

        If either operation fails, the transaction is rolled
        back and no partial customer tenant is created.
        """

        if current_user.role != UserRole.SUPER_ADMIN:
            raise AuthorizationException()

        organization_name = (
            request.organization_name.strip()
        )

        organization_code = (
            request.organization_code.strip().upper()
        )

        contact_email = (
            str(request.contact_email)
            .strip()
            .lower()
        )

        normalized_admin_email = (
            str(request.admin_email)
            .strip()
            .lower()
        )

        existing_by_name = (
            self._organization_repository.get_by_name(
                organization_name,
            )
        )

        if existing_by_name is not None:
            raise PersistenceDataException(
                "Organization already exists."
            )

        existing_by_code = (
            self._organization_repository.get_by_code(
                organization_code,
            )
        )

        if existing_by_code is not None:
            raise PersistenceDataException(
                "Organization code already exists."
            )

        organization = Organization(
            organization_id=str(uuid4()),
            name=organization_name,
            code=organization_code,
            industry=request.industry.strip(),
            contact_email=contact_email,
            is_active=True,
            created_at=datetime.now(UTC),
        )

        admin = User(
            id=str(uuid4()),
            full_name=request.admin_full_name.strip(),
            email=normalized_admin_email,
            hashed_password=hash_password(
                request.admin_password,
            ),
            is_active=True,
            created_at=datetime.now(UTC),
            role=UserRole.ADMIN,
            organization_id=organization.organization_id,
        )

        with self._session_factory() as session:
            with session.begin():
                self._organization_repository.create_in_session(
                    session,
                    organization,
                )

                self._user_repository.create_user_in_session(
                    session,
                    admin,
                )

        return OnboardedOrganizationResponse(
            organization_id=organization.organization_id,
            organization_name=organization.name,
            organization_code=organization.code,
            industry=organization.industry,
            contact_email=organization.contact_email,
            organization_is_active=organization.is_active,
            admin_user_id=admin.id,
            admin_full_name=admin.full_name,
            admin_email=admin.email,
            admin_role=admin.role,
            admin_organization_id=admin.organization_id,
            admin_is_active=admin.is_active,
            admin_created_at=admin.created_at,
        )