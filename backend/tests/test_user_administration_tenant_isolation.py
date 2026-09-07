from datetime import UTC, datetime

import pytest

from app.core.constants import UserRole
from app.domain import User
from app.exceptions.exceptions import (
    AuthorizationException,
    PersistenceDataException,
)
from app.models.admin import (
    CreateAdminUserRequest,
)
from app.repositories.user_repository import (
    UserRepository,
)
from app.services.user_administration_service import (
    UserAdministrationService,
)


ORGANIZATION_A_ID = (
    "00000000-0000-4000-8000-000000000101"
)

ORGANIZATION_B_ID = (
    "00000000-0000-4000-8000-000000000102"
)


@pytest.fixture
def user_administration_service(
    isolated_user_repository: UserRepository,
) -> UserAdministrationService:
    """Provide user administration with isolated persistence."""

    return UserAdministrationService(
        isolated_user_repository,
    )


@pytest.fixture
def customer_admin_a() -> User:
    """Provide a Customer Admin for Organization A."""

    return User(
        id="00000000-0000-4000-8000-000000000201",
        full_name="Organization A Admin",
        email="admin-a@example.com",
        hashed_password="not-used-by-test",
        is_active=True,
        created_at=datetime(
            2026,
            9,
            6,
            10,
            0,
            tzinfo=UTC,
        ),
        role=UserRole.ADMIN,
        organization_id=ORGANIZATION_A_ID,
    )


@pytest.fixture
def customer_admin_b() -> User:
    """Provide a Customer Admin for Organization B."""

    return User(
        id="00000000-0000-4000-8000-000000000202",
        full_name="Organization B Admin",
        email="admin-b@example.com",
        hashed_password="not-used-by-test",
        is_active=True,
        created_at=datetime(
            2026,
            9,
            6,
            10,
            0,
            tzinfo=UTC,
        ),
        role=UserRole.ADMIN,
        organization_id=ORGANIZATION_B_ID,
    )


@pytest.fixture
def super_admin() -> User:
    """Provide a platform-scoped Super Admin."""

    return User(
        id="00000000-0000-4000-8000-000000000203",
        full_name="Platform Super Admin",
        email="super-admin@example.com",
        hashed_password="not-used-by-test",
        is_active=True,
        created_at=datetime(
            2026,
            9,
            6,
            10,
            0,
            tzinfo=UTC,
        ),
        role=UserRole.SUPER_ADMIN,
        organization_id=None,
    )


def create_customer_user(
    service: UserAdministrationService,
    current_user: User,
    *,
    full_name: str,
    email: str,
    role: UserRole = UserRole.AGENT,
    organization_id: str | None = None,
) -> User:
    """Create a user through the administration service."""

    request = CreateAdminUserRequest(
        full_name=full_name,
        email=email,
        password="StrongPassword123",
        role=role,
        organization_id=organization_id,
    )

    return service.create_user(
        request,
        current_user=current_user,
    )


def test_customer_admin_can_only_create_user_in_own_organization(
    user_administration_service: UserAdministrationService,
    customer_admin_a: User,
) -> None:
    """Customer Admin tenant scope must come from authentication."""

    user = create_customer_user(
        user_administration_service,
        customer_admin_a,
        full_name="Organization A Agent",
        email="agent-a@example.com",
        organization_id=ORGANIZATION_B_ID,
    )

    assert user.organization_id == ORGANIZATION_A_ID
    assert user.role == UserRole.AGENT


def test_customer_admin_cannot_create_super_admin(
    user_administration_service: UserAdministrationService,
    customer_admin_a: User,
) -> None:
    """Customer Admin must never provision a Super Admin."""

    request = CreateAdminUserRequest(
        full_name="Unauthorized Super Admin",
        email="unauthorized-super@example.com",
        password="StrongPassword123",
        role=UserRole.SUPER_ADMIN,
    )

    with pytest.raises(AuthorizationException):
        user_administration_service.create_user(
            request,
            current_user=customer_admin_a,
        )


def test_customer_admin_cannot_view_user_from_another_organization(
    user_administration_service: UserAdministrationService,
    customer_admin_a: User,
    customer_admin_b: User,
) -> None:
    """Users outside the tenant must be invisible."""

    user_b = create_customer_user(
        user_administration_service,
        customer_admin_b,
        full_name="Organization B Agent",
        email="agent-b@example.com",
    )

    result = user_administration_service.get_user(
        user_id=user_b.id,
        current_user=customer_admin_a,
    )

    assert result is None


def test_customer_admin_list_is_restricted_to_own_organization(
    user_administration_service: UserAdministrationService,
    customer_admin_a: User,
    customer_admin_b: User,
) -> None:
    """Customer Admin listing must not expose another tenant."""

    user_a = create_customer_user(
        user_administration_service,
        customer_admin_a,
        full_name="Organization A Agent",
        email="list-agent-a@example.com",
    )

    user_b = create_customer_user(
        user_administration_service,
        customer_admin_b,
        full_name="Organization B Agent",
        email="list-agent-b@example.com",
    )

    result = user_administration_service.list_users(
        current_user=customer_admin_a,
        page=1,
        page_size=100,
    )

    user_ids = {
        user.id
        for user in result.users
    }

    assert user_a.id in user_ids
    assert user_b.id not in user_ids
    assert result.total == 1


def test_customer_admin_cannot_activate_user_from_another_organization(
    user_administration_service: UserAdministrationService,
    customer_admin_a: User,
    customer_admin_b: User,
) -> None:
    """Customer Admin cannot activate a user outside the tenant."""

    user_b = create_customer_user(
        user_administration_service,
        customer_admin_b,
        full_name="Inactive Organization B Agent",
        email="activate-agent-b@example.com",
    )

    user_administration_service.deactivate_user(
        user_id=user_b.id,
        current_user_id=customer_admin_b.id,
        current_user=customer_admin_b,
    )

    with pytest.raises(PersistenceDataException) as exc_info:
        user_administration_service.activate_user(
            user_id=user_b.id,
            current_user=customer_admin_a,
        )

    assert str(exc_info.value) == "User not found."


def test_customer_admin_cannot_deactivate_user_from_another_organization(
    user_administration_service: UserAdministrationService,
    customer_admin_a: User,
    customer_admin_b: User,
) -> None:
    """Customer Admin cannot deactivate a user outside the tenant."""

    user_b = create_customer_user(
        user_administration_service,
        customer_admin_b,
        full_name="Organization B Protected Agent",
        email="deactivate-agent-b@example.com",
    )

    with pytest.raises(PersistenceDataException) as exc_info:
        user_administration_service.deactivate_user(
            user_id=user_b.id,
            current_user_id=customer_admin_a.id,
            current_user=customer_admin_a,
        )

    assert str(exc_info.value) == "User not found."


def test_customer_admin_can_activate_user_in_own_organization(
    user_administration_service: UserAdministrationService,
    customer_admin_a: User,
) -> None:
    """Customer Admin can activate users inside own tenant."""

    user = create_customer_user(
        user_administration_service,
        customer_admin_a,
        full_name="Organization A Lifecycle Agent",
        email="lifecycle-agent-a@example.com",
    )

    deactivated_user = (
        user_administration_service.deactivate_user(
            user_id=user.id,
            current_user_id=customer_admin_a.id,
            current_user=customer_admin_a,
        )
    )

    assert deactivated_user.is_active is False

    activated_user = (
        user_administration_service.activate_user(
            user_id=user.id,
            current_user=customer_admin_a,
        )
    )

    assert activated_user.is_active is True


def test_customer_admin_cannot_deactivate_self(
    user_administration_service: UserAdministrationService,
    customer_admin_a: User,
) -> None:
    """An administrator must not deactivate their own account."""

    with pytest.raises(AuthorizationException):
        user_administration_service.deactivate_user(
            user_id=customer_admin_a.id,
            current_user_id=customer_admin_a.id,
            current_user=customer_admin_a,
        )


def test_super_admin_can_view_users_across_organizations(
    user_administration_service: UserAdministrationService,
    customer_admin_a: User,
    customer_admin_b: User,
    super_admin: User,
) -> None:
    """Super Admin is platform-scoped."""

    user_a = create_customer_user(
        user_administration_service,
        customer_admin_a,
        full_name="Platform Visible Agent A",
        email="platform-agent-a@example.com",
    )

    user_b = create_customer_user(
        user_administration_service,
        customer_admin_b,
        full_name="Platform Visible Agent B",
        email="platform-agent-b@example.com",
    )

    result = user_administration_service.list_users(
        current_user=super_admin,
        page=1,
        page_size=100,
    )

    user_ids = {
        user.id
        for user in result.users
    }

    assert user_a.id in user_ids
    assert user_b.id in user_ids


def test_super_admin_can_provision_customer_user(
    user_administration_service: UserAdministrationService,
    super_admin: User,
) -> None:
    """Super Admin may explicitly provision a customer user."""

    user = create_customer_user(
        user_administration_service,
        super_admin,
        full_name="Super Admin Provisioned Agent",
        email="super-provisioned-agent@example.com",
        organization_id=ORGANIZATION_A_ID,
    )

    assert user.organization_id == ORGANIZATION_A_ID
    assert user.role == UserRole.AGENT


def test_super_admin_can_provision_platform_super_admin(
    user_administration_service: UserAdministrationService,
    super_admin: User,
) -> None:
    """Super Admin may provision another platform Super Admin."""

    user = create_customer_user(
        user_administration_service,
        super_admin,
        full_name="Second Platform Super Admin",
        email="second-super-admin@example.com",
        role=UserRole.SUPER_ADMIN,
    )

    assert user.organization_id is None
    assert user.role == UserRole.SUPER_ADMIN


def test_super_admin_cannot_change_own_role(
    user_administration_service: UserAdministrationService,
    super_admin: User,
) -> None:
    """A Super Admin must not be able to change their own role."""

    with pytest.raises(AuthorizationException):
        user_administration_service.change_role(
            user_id=super_admin.id,
            role=UserRole.ADMIN,
            current_user_id=super_admin.id,
            current_user=super_admin,
        )