from datetime import UTC, datetime

import pytest

from app.core.constants import UserRole
from app.domain import User
from app.domain.branch import Branch
from app.domain.department import Department
from app.exceptions.exceptions import AuthorizationException
from app.repositories.branch_repository import BranchRepository
from app.repositories.department_repository import (
    DepartmentRepository,
)
from app.repositories.organization_repository import (
    OrganizationRepository,
)
from app.services.branch_service import BranchService
from app.services.department_service import DepartmentService


@pytest.fixture
def organization_a_id() -> str:
    return "00000000-0000-4000-8000-000000000101"


@pytest.fixture
def organization_b_id() -> str:
    return "00000000-0000-4000-8000-000000000102"


@pytest.fixture
def customer_user_a(
    organization_a_id: str,
) -> User:
    return User(
        id="00000000-0000-4000-8000-000000000201",
        full_name="Organization A Administrator",
        email="admin-a@example.com",
        hashed_password="not-used-by-test",
        is_active=True,
        created_at=datetime(
            2026,
            9,
            1,
            12,
            0,
            tzinfo=UTC,
        ),
        role=UserRole.ADMIN,
        organization_id=organization_a_id,
    )


@pytest.fixture
def customer_user_b(
    organization_b_id: str,
) -> User:
    return User(
        id="00000000-0000-4000-8000-000000000202",
        full_name="Organization B Administrator",
        email="admin-b@example.com",
        hashed_password="not-used-by-test",
        is_active=True,
        created_at=datetime(
            2026,
            9,
            1,
            12,
            0,
            tzinfo=UTC,
        ),
        role=UserRole.ADMIN,
        organization_id=organization_b_id,
    )


@pytest.fixture
def super_admin_user() -> User:
    return User(
        id="00000000-0000-4000-8000-000000000203",
        full_name="Platform Super Admin",
        email="superadmin@example.com",
        hashed_password="not-used-by-test",
        is_active=True,
        created_at=datetime(
            2026,
            9,
            1,
            12,
            0,
            tzinfo=UTC,
        ),
        role=UserRole.SUPER_ADMIN,
        organization_id=None,
    )


def test_customer_user_cannot_access_branch_from_another_organization():
    branch = Branch(
        branch_id="00000000-0000-4000-8000-000000000301",
        organization_id="organization-b",
        name="Organization B Branch",
        code="ORG-B-BRANCH",
        city="Lagos",
        state="Lagos",
        is_active=True,
        created_at=datetime.now(UTC),
    )

    class FakeBranchRepository:
        def get_by_id(self, branch_id: str):
            return branch

    class FakeOrganizationRepository:
        pass

    service = BranchService(
        FakeBranchRepository(),
        FakeOrganizationRepository(),
    )

    with pytest.raises(AuthorizationException):
        service.get_branch(
            branch.branch_id,
            current_user_organization_id="organization-a",
            current_user_role=UserRole.ADMIN,
        )


def test_customer_user_cannot_list_branches_from_another_organization():
    class FakeOrganization:
        organization_id = "organization-b"
        is_active = True

    class FakeBranchRepository:
        def list_by_organization(
            self,
            organization_id: str,
        ):
            return []

    class FakeOrganizationRepository:
        def get_by_id(
            self,
            organization_id: str,
        ):
            return FakeOrganization()

    service = BranchService(
        FakeBranchRepository(),
        FakeOrganizationRepository(),
    )

    with pytest.raises(AuthorizationException):
        service.list_branches(
            "organization-b",
            current_user_organization_id="organization-a",
            current_user_role=UserRole.ADMIN,
        )


def test_super_admin_can_access_branch_across_organizations():
    branch = Branch(
        branch_id="00000000-0000-4000-8000-000000000302",
        organization_id="organization-b",
        name="Organization B Branch",
        code="ORG-B-BRANCH-2",
        city="Abuja",
        state="FCT",
        is_active=True,
        created_at=datetime.now(UTC),
    )

    class FakeBranchRepository:
        def get_by_id(self, branch_id: str):
            return branch

    class FakeOrganizationRepository:
        pass

    service = BranchService(
        FakeBranchRepository(),
        FakeOrganizationRepository(),
    )

    result = service.get_branch(
        branch.branch_id,
        current_user_organization_id=None,
        current_user_role=UserRole.SUPER_ADMIN,
    )

    assert result is not None
    assert result.branch_id == branch.branch_id
    assert result.organization_id == "organization-b"


def test_customer_user_cannot_access_department_from_another_organization():
    department = Department(
        department_id="00000000-0000-4000-8000-000000000401",
        organization_id="organization-b",
        branch_id="branch-b",
        name="Operations",
        code="ORG-B-OPS",
        is_active=True,
        created_at=datetime.now(UTC),
    )

    class FakeDepartmentRepository:
        def get_by_id(self, department_id: str):
            return department

    class FakeBranchRepository:
        pass

    class FakeOrganizationRepository:
        pass

    service = DepartmentService(
        FakeDepartmentRepository(),
        FakeBranchRepository(),
        FakeOrganizationRepository(),
    )

    with pytest.raises(AuthorizationException):
        service.get_department(
            department.department_id,
            current_user_organization_id="organization-a",
            current_user_role=UserRole.ADMIN,
        )


def test_customer_user_cannot_list_departments_from_another_organization():
    branch = Branch(
        branch_id="branch-b",
        organization_id="organization-b",
        name="Organization B Branch",
        code="ORG-B-BRANCH-3",
        city="Lagos",
        state="Lagos",
        is_active=True,
        created_at=datetime.now(UTC),
    )

    class FakeDepartmentRepository:
        def list_by_branch(
            self,
            branch_id: str,
        ):
            return []

    class FakeBranchRepository:
        def get_by_id(
            self,
            branch_id: str,
        ):
            return branch

    class FakeOrganizationRepository:
        pass

    service = DepartmentService(
        FakeDepartmentRepository(),
        FakeBranchRepository(),
        FakeOrganizationRepository(),
    )

    with pytest.raises(AuthorizationException):
        service.list_departments(
            "branch-b",
            current_user_organization_id="organization-a",
            current_user_role=UserRole.ADMIN,
        )


def test_super_admin_can_access_department_across_organizations():
    department = Department(
        department_id="00000000-0000-4000-8000-000000000402",
        organization_id="organization-b",
        branch_id="branch-b",
        name="Finance",
        code="ORG-B-FIN",
        is_active=True,
        created_at=datetime.now(UTC),
    )

    class FakeDepartmentRepository:
        def get_by_id(
            self,
            department_id: str,
        ):
            return department

    class FakeBranchRepository:
        pass

    class FakeOrganizationRepository:
        pass

    service = DepartmentService(
        FakeDepartmentRepository(),
        FakeBranchRepository(),
        FakeOrganizationRepository(),
    )

    result = service.get_department(
        department.department_id,
        current_user_organization_id=None,
        current_user_role=UserRole.SUPER_ADMIN,
    )

    assert result is not None
    assert result.department_id == department.department_id
    assert result.organization_id == "organization-b"