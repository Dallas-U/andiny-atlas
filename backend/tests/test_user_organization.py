from datetime import UTC, datetime

import pytest

from app.core.constants import UserRole
from app.domain import User
from app.exceptions.exceptions import (
    AuthorizationException,
    PersistenceDataException,
)
from app.models.admin import CreateAdminUserRequest
from app.services.user_administration_service import (
    UserAdministrationService,
)


class FakeUserRepository:
    def __init__(self):
        self.users: dict[str, User] = {}

    def create_user(self, user: User) -> User:
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
                and user.organization_id != organization_id
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
            and user.organization_id != organization_id
        ):
            return None

        return user

    def list_users(
        self,
        offset: int,
        limit: int,
        organization_id: str | None = None,
    ) -> tuple[list[User], int]:

        users = list(self.users.values())

        if organization_id is not None:
            users = [
                user
                for user in users
                if user.organization_id == organization_id
            ]

        users = users[offset : offset + limit]

        return users, len(
            [
                user
                for user in self.users.values()
                if (
                    organization_id is None
                    or user.organization_id == organization_id
                )
            ]
        )

    def update_user(
        self,
        user: User,
        organization_id: str | None = None,
    ) -> User:

        existing = self.get_user_by_id(
            user.id,
            organization_id=organization_id,
        )

        if existing is None:
            raise PersistenceDataException(
                "User not found."
            )

        self.users[user.id] = user

        return user


def make_user(
    *,
    user_id: str,
    role: UserRole,
    organization_id: str | None,
) -> User:

    return User(
        id=user_id,
        full_name=user_id,
        email=f"{user_id}@test.com",
        hashed_password="hashed",
        is_active=True,
        created_at=datetime.now(UTC),
        role=role,
        organization_id=organization_id,
    )


def test_customer_user_can_have_organization():
    repository = FakeUserRepository()
    service = UserAdministrationService(repository)

    admin = make_user(
        user_id="admin-001",
        role=UserRole.ADMIN,
        organization_id="org-001",
    )

    request = CreateAdminUserRequest(
        full_name="Customer Agent",
        email="agent@test.com",
        password="password123",
        role=UserRole.AGENT,
        organization_id="org-999",
    )

    user = service.create_user(
        request,
        current_user=admin,
    )

    assert user.organization_id == "org-001"


def test_customer_admin_cannot_create_super_admin():
    repository = FakeUserRepository()
    service = UserAdministrationService(repository)

    admin = make_user(
        user_id="admin-001",
        role=UserRole.ADMIN,
        organization_id="org-001",
    )

    request = CreateAdminUserRequest(
        full_name="Platform Admin",
        email="platform@test.com",
        password="password123",
        role=UserRole.SUPER_ADMIN,
    )

    with pytest.raises(AuthorizationException):
        service.create_user(
            request,
            current_user=admin,
        )


def test_customer_admin_cannot_choose_another_organization():
    repository = FakeUserRepository()
    service = UserAdministrationService(repository)

    admin = make_user(
        user_id="admin-001",
        role=UserRole.ADMIN,
        organization_id="org-001",
    )

    request = CreateAdminUserRequest(
        full_name="Customer User",
        email="customer@test.com",
        password="password123",
        role=UserRole.AGENT,
        organization_id="org-999",
    )

    user = service.create_user(
        request,
        current_user=admin,
    )

    assert user.organization_id == "org-001"
    assert user.organization_id != request.organization_id


def test_customer_admin_can_only_get_user_from_own_organization():
    repository = FakeUserRepository()
    service = UserAdministrationService(repository)

    admin = make_user(
        user_id="admin-001",
        role=UserRole.ADMIN,
        organization_id="org-001",
    )

    own_user = make_user(
        user_id="user-001",
        role=UserRole.AGENT,
        organization_id="org-001",
    )

    foreign_user = make_user(
        user_id="user-002",
        role=UserRole.AGENT,
        organization_id="org-002",
    )

    repository.users[own_user.id] = own_user
    repository.users[foreign_user.id] = foreign_user

    result = service.get_user(
        user_id=own_user.id,
        current_user=admin,
    )

    assert result is not None
    assert result.id == own_user.id

    result = service.get_user(
        user_id=foreign_user.id,
        current_user=admin,
    )

    assert result is None


def test_customer_admin_list_is_tenant_scoped():
    repository = FakeUserRepository()
    service = UserAdministrationService(repository)

    admin = make_user(
        user_id="admin-001",
        role=UserRole.ADMIN,
        organization_id="org-001",
    )

    org_one_user = make_user(
        user_id="user-001",
        role=UserRole.AGENT,
        organization_id="org-001",
    )

    org_two_user = make_user(
        user_id="user-002",
        role=UserRole.AGENT,
        organization_id="org-002",
    )

    repository.users[admin.id] = admin
    repository.users[org_one_user.id] = org_one_user
    repository.users[org_two_user.id] = org_two_user

    result = service.list_users(
        current_user=admin,
        page=1,
        page_size=20,
    )

    returned_ids = {
        user.id
        for user in result.users
    }

    assert "admin-001" in returned_ids
    assert "user-001" in returned_ids
    assert "user-002" not in returned_ids
    assert result.total == 2


def test_customer_admin_cannot_activate_foreign_user():
    repository = FakeUserRepository()
    service = UserAdministrationService(repository)

    admin = make_user(
        user_id="admin-001",
        role=UserRole.ADMIN,
        organization_id="org-001",
    )

    foreign_user = make_user(
        user_id="user-002",
        role=UserRole.AGENT,
        organization_id="org-002",
    )

    foreign_user = User(
        id=foreign_user.id,
        full_name=foreign_user.full_name,
        email=foreign_user.email,
        hashed_password=foreign_user.hashed_password,
        is_active=False,
        created_at=foreign_user.created_at,
        role=foreign_user.role,
        organization_id=foreign_user.organization_id,
    )

    repository.users[foreign_user.id] = foreign_user

    with pytest.raises(PersistenceDataException):
        service.activate_user(
            user_id=foreign_user.id,
            current_user=admin,
        )


def test_customer_admin_cannot_deactivate_foreign_user():
    repository = FakeUserRepository()
    service = UserAdministrationService(repository)

    admin = make_user(
        user_id="admin-001",
        role=UserRole.ADMIN,
        organization_id="org-001",
    )

    foreign_user = make_user(
        user_id="user-002",
        role=UserRole.AGENT,
        organization_id="org-002",
    )

    repository.users[foreign_user.id] = foreign_user

    with pytest.raises(PersistenceDataException):
        service.deactivate_user(
            user_id=foreign_user.id,
            current_user_id=admin.id,
            current_user=admin,
        )


def test_super_admin_can_access_users_across_organizations():
    repository = FakeUserRepository()
    service = UserAdministrationService(repository)

    super_admin = make_user(
        user_id="super-admin-001",
        role=UserRole.SUPER_ADMIN,
        organization_id=None,
    )

    org_one_user = make_user(
        user_id="user-001",
        role=UserRole.AGENT,
        organization_id="org-001",
    )

    org_two_user = make_user(
        user_id="user-002",
        role=UserRole.AGENT,
        organization_id="org-002",
    )

    repository.users[org_one_user.id] = org_one_user
    repository.users[org_two_user.id] = org_two_user

    result = service.list_users(
        current_user=super_admin,
        page=1,
        page_size=20,
    )

    returned_ids = {
        user.id
        for user in result.users
    }

    assert returned_ids == {
        "user-001",
        "user-002",
    }


def test_super_admin_cannot_change_own_role():
    repository = FakeUserRepository()

    super_admin = make_user(
        user_id="super-admin-001",
        role=UserRole.SUPER_ADMIN,
        organization_id=None,
    )

    repository.users[super_admin.id] = super_admin

    service = UserAdministrationService(repository)

    with pytest.raises(AuthorizationException):
        service.change_role(
            user_id=super_admin.id,
            role=UserRole.ADMIN,
            current_user_id=super_admin.id,
            current_user=super_admin,
        )


def test_customer_admin_cannot_change_role():
    repository = FakeUserRepository()

    admin = make_user(
        user_id="admin-001",
        role=UserRole.ADMIN,
        organization_id="org-001",
    )

    target = make_user(
        user_id="user-001",
        role=UserRole.AGENT,
        organization_id="org-001",
    )

    repository.users[target.id] = target

    service = UserAdministrationService(repository)

    with pytest.raises(AuthorizationException):
        service.change_role(
            user_id=target.id,
            role=UserRole.SUPERVISOR,
            current_user_id=admin.id,
            current_user=admin,
        )


def test_customer_admin_cannot_deactivate_self():
    repository = FakeUserRepository()

    admin = make_user(
        user_id="admin-001",
        role=UserRole.ADMIN,
        organization_id="org-001",
    )

    repository.users[admin.id] = admin

    service = UserAdministrationService(repository)

    with pytest.raises(AuthorizationException):
        service.deactivate_user(
            user_id=admin.id,
            current_user_id=admin.id,
            current_user=admin,
        )