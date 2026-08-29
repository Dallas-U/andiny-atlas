from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from app.core.constants import UserRole
from app.core.security import hash_password
from app.domain import User
from app.domain.organization import Organization
from app.exceptions.exceptions import (
    AuthorizationException,
    PersistenceDataException,
    UserAlreadyExistsException,
)
from app.models.onboarding import (
    CreateCustomerOrganizationRequest,
    OnboardedOrganizationResponse,
)
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.user_repository import UserRepository
from app.services.organization_service import OrganizationService


class OnboardingService:
    """
    Application service responsible for customer tenant provisioning.

    This service orchestrates:

        Organization creation
        Initial customer administrator creation

    Platform governance remains restricted to Super Admin.
    """

    def __init__(
        self,
        organization_repository: OrganizationRepository,
        user_repository: UserRepository,
    ) -> None:
        self._organization_service = OrganizationService(
            organization_repository,
        )

        self._organization_repository = (
            organization_repository
        )

        self._user_repository = user_repository

    def provision_customer_organization(
        self,
        request: CreateCustomerOrganizationRequest,
        *,
        current_user: User,
    ) -> OnboardedOrganizationResponse:
        """
        Provision a complete customer tenant.

        Only Super Admin may execute this operation.

        Resulting hierarchy:

            Organization
                └── Initial Customer Admin
        """

        if current_user.role != UserRole.SUPER_ADMIN:
            raise AuthorizationException()

        organization = self._create_organization(
            request,
        )

        admin = self._create_initial_customer_admin(
            request=request,
            organization=organization,
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

    def _create_organization(
        self,
        request: CreateCustomerOrganizationRequest,
    ) -> Organization:
        organization_name = (
            request.organization_name.strip()
        )

        organization_code = (
            request.organization_code.strip().upper()
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

        return self._organization_service.create_organization(
            name=organization_name,
            code=organization_code,
            industry=request.industry.strip(),
            contact_email=(
                str(request.contact_email)
                .strip()
                .lower()
            ),
        )

    def _create_initial_customer_admin(
        self,
        *,
        request: CreateCustomerOrganizationRequest,
        organization: Organization,
    ) -> User:
        """
        Create the first administrator belonging to the
        newly created organization.

        The organization ID comes exclusively from the
        newly provisioned organization.
        """

        normalized_email = (
            str(request.admin_email)
            .strip()
            .lower()
        )

        existing_user = (
            self._user_repository.get_user_by_email(
                normalized_email,
                organization_id=organization.organization_id,
            )
        )

        if existing_user is not None:
            raise UserAlreadyExistsException(
                normalized_email,
            )

        admin = User(
            id=str(uuid4()),
            full_name=request.admin_full_name.strip(),
            email=normalized_email,
            hashed_password=hash_password(
                request.admin_password,
            ),
            is_active=True,
            created_at=datetime.now(UTC),
            role=UserRole.ADMIN,
            organization_id=organization.organization_id,
        )

        return self._user_repository.create_user(
            admin,
        )