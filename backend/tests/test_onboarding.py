from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.core.constants import UserRole
from app.domain import User
from app.domain.organization import Organization
from app.exceptions.exceptions import (
    AuthorizationException,
    PersistenceDataException,
)
from app.models.onboarding import CreateCustomerOrganizationRequest
from app.services.onboarding_service import OnboardingService


class FakeSession:
    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        return False

    def begin(self):
        return self


def fake_session_factory():
    return FakeSession()


class FakeOrganizationRepository:
    def __init__(self) -> None:
        self.organizations: dict[str, Organization] = {}

    def create(
        self,
        organization: Organization,
    ) -> Organization:
        self.organizations[
            organization.organization_id
        ] = organization

        return organization

    def create_in_session(
        self,
        session,
        organization: Organization,
    ) -> Organization:
        self.organizations[
            organization.organization_id
        ] = organization

        return organization

    def list_all(self) -> list[Organization]:
        return list(
            self.organizations.values()
        )

    def get_by_id(
        self,
        organization_id: str,
    ) -> Organization | None:
        return self.organizations.get(
            organization_id,
        )

    def get_by_name(
        self,
        name: str,
    ) -> Organization | None:
        for organization in self.organizations.values():
            if organization.name == name:
                return organization

        return None

    def get_by_code(
        self,
        code: str,
    ) -> Organization | None:
        for organization in self.organizations.values():
            if organization.code == code:
                return organization

        return None


class FakeSession:
    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        return False

    def begin(self):
        return self

    def fake_session_factory():
        return FakeSession()


class FakeUserRepository:
    def __init__(self) -> None:
        self.users: dict[str, User] = {}

    def create_user(
        self,
        user: User,
    ) -> User:
        self.users[user.id] = user
        return user

    def create_user_in_session(
        self,
        session,
        user: User,
    ) -> User:
        self.users[user.id] = user
        return user

    def get_user_by_email(
        self,
        email: str,
        organization_id: str | None = None,
    ) -> User | None:
        normalized_email = email.strip().lower()

        for user in self.users.values():
            if user.email != normalized_email:
                continue

            if (
                organization_id is not None
                and user.organization_id
                != organization_id
            ):
                continue

            return user

        return None

    def get_user_by_id(
        self,
        user_id: str,
        organization_id: str | None = None,
    ) -> User | None:
        user = self.users.get(user_id)

        if user is None:
            return None

        if (
            organization_id is not None
            and user.organization_id
            != organization_id
        ):
            return None

        return user


def create_super_admin() -> User:
    return User(
        id="super-admin-001",
        full_name="Platform Super Admin",
        email="superadmin@example.com",
        hashed_password="hashed-password",
        is_active=True,
        created_at=datetime.now(UTC),
        role=UserRole.SUPER_ADMIN,
        organization_id=None,
    )


def create_customer_admin(
    organization_id: str = "org-existing",
) -> User:
    return User(
        id="customer-admin-001",
        full_name="Customer Administrator",
        email="admin@customer.example.com",
        hashed_password="hashed-password",
        is_active=True,
        created_at=datetime.now(UTC),
        role=UserRole.ADMIN,
        organization_id=organization_id,
    )


def create_request(
    *,
    organization_name: str = "Acme Financial Services",
    organization_code: str = "ACME",
    industry: str = "Financial Services",
    contact_email: str = "contact@acme.example.com",
    admin_full_name: str = "Acme Administrator",
    admin_email: str = "admin@acme.example.com",
    admin_password: str = "password123",
) -> CreateCustomerOrganizationRequest:
    return CreateCustomerOrganizationRequest(
        organization_name=organization_name,
        organization_code=organization_code,
        industry=industry,
        contact_email=contact_email,
        admin_full_name=admin_full_name,
        admin_email=admin_email,
        admin_password=admin_password,
    )


def create_service() -> OnboardingService:
    return OnboardingService(
        organization_repository=FakeOrganizationRepository(),
        user_repository=FakeUserRepository(),
        session_factory=fake_session_factory,
    )


def test_super_admin_can_provision_customer_organization():
    service = create_service()
    super_admin = create_super_admin()

    request = create_request()

    result = service.provision_customer_organization(
        request,
        current_user=super_admin,
    )

    assert result.organization_name == (
        "Acme Financial Services"
    )

    assert result.organization_code == "ACME"

    assert result.industry == "Financial Services"

    assert result.organization_is_active is True


def test_initial_customer_admin_is_created():
    service = create_service()
    super_admin = create_super_admin()

    request = create_request()

    result = service.provision_customer_organization(
        request,
        current_user=super_admin,
    )

    assert result.admin_user_id

    assert result.admin_full_name == (
        "Acme Administrator"
    )

    assert result.admin_email == (
        "admin@acme.example.com"
    )


def test_initial_customer_admin_has_admin_role():
    service = create_service()
    super_admin = create_super_admin()

    result = service.provision_customer_organization(
        create_request(),
        current_user=super_admin,
    )

    assert result.admin_role == UserRole.ADMIN


def test_initial_customer_admin_is_bound_to_new_organization():
    service = create_service()
    super_admin = create_super_admin()

    result = service.provision_customer_organization(
        create_request(),
        current_user=super_admin,
    )

    assert result.admin_organization_id == (
        result.organization_id
    )

    assert result.admin_organization_id is not None


def test_initial_customer_admin_is_active():
    service = create_service()
    super_admin = create_super_admin()

    result = service.provision_customer_organization(
        create_request(),
        current_user=super_admin,
    )

    assert result.admin_is_active is True


def test_customer_admin_cannot_provision_organization():
    service = create_service()
    customer_admin = create_customer_admin()

    with pytest.raises(AuthorizationException):
        service.provision_customer_organization(
            create_request(),
            current_user=customer_admin,
        )


def test_duplicate_organization_name_is_rejected():
    organization_repository = FakeOrganizationRepository()
    user_repository = FakeUserRepository()

    service = OnboardingService(
        organization_repository=organization_repository,
        user_repository=user_repository,
    )

    super_admin = create_super_admin()

    service.provision_customer_organization(
        create_request(),
        current_user=super_admin,
    )

    with pytest.raises(PersistenceDataException):
        service.provision_customer_organization(
            create_request(
                organization_code="ACME2",
                admin_email="admin2@acme.example.com",
            ),
            current_user=super_admin,
        )


def test_duplicate_organization_code_is_rejected():
    organization_repository = FakeOrganizationRepository()
    user_repository = FakeUserRepository()

    service = OnboardingService(
        organization_repository=organization_repository,
        user_repository=user_repository,
    )

    super_admin = create_super_admin()

    service.provision_customer_organization(
        create_request(),
        current_user=super_admin,
    )

    with pytest.raises(PersistenceDataException):
        service.provision_customer_organization(
            create_request(
                organization_name="Another Organization",
                organization_code="ACME",
                admin_email="admin2@another.example.com",
            ),
            current_user=super_admin,
        )


def test_customer_admin_cannot_become_super_admin_during_onboarding():
    service = create_service()

    customer_admin = create_customer_admin()

    request = create_request()

    with pytest.raises(AuthorizationException):
        service.provision_customer_organization(
            request,
            current_user=customer_admin,
        )


def test_provisioning_creates_complete_organization_admin_relationship():
    organization_repository = FakeOrganizationRepository()
    user_repository = FakeUserRepository()

    service = OnboardingService(
        organization_repository=organization_repository,
        user_repository=user_repository,
    )

    super_admin = create_super_admin()

    result = service.provision_customer_organization(
        create_request(),
        current_user=super_admin,
    )

    organization = organization_repository.get_by_id(
        result.organization_id,
    )

    admin = user_repository.get_user_by_id(
        result.admin_user_id,
    )

    assert organization is not None
    assert admin is not None

    assert organization.organization_id == (
        admin.organization_id
    )

    assert admin.role == UserRole.ADMIN
    assert admin.is_active is True