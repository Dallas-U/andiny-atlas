from datetime import UTC, datetime

import pytest

from app.core.constants import UserRole
from app.domain.branch import Branch
from app.domain.department import Department
from app.domain.organization import Organization
from app.exceptions.exceptions import (
    AuthorizationException,
    PersistenceDataException,
)
from app.services.branch_service import BranchService
from app.services.department_service import DepartmentService


class FakeOrganizationRepository:
    def __init__(self):
        self.organizations: dict[str, Organization] = {}

    def get_by_id(
        self,
        organization_id: str,
    ) -> Organization | None:
        return self.organizations.get(organization_id)


class FakeBranchRepository:
    def __init__(self):
        self.branches: dict[str, Branch] = {}

    def create(
        self,
        branch: Branch,
    ) -> Branch:
        self.branches[branch.branch_id] = branch
        return branch

    def get_by_id(
        self,
        branch_id: str,
    ) -> Branch | None:
        return self.branches.get(branch_id)

    def get_by_code(
        self,
        code: str,
    ) -> Branch | None:
        for branch in self.branches.values():
            if branch.code == code:
                return branch

        return None

    def list_by_organization(
        self,
        organization_id: str,
    ) -> list[Branch]:
        return [
            branch
            for branch in self.branches.values()
            if branch.organization_id == organization_id
        ]


class FakeDepartmentRepository:
    def __init__(self):
        self.departments: dict[str, Department] = {}

    def create(
        self,
        department: Department,
    ) -> Department:
        self.departments[department.department_id] = department
        return department

    def get_by_id(
        self,
        department_id: str,
    ) -> Department | None:
        return self.departments.get(department_id)

    def get_by_code(
        self,
        code: str,
    ) -> Department | None:
        for department in self.departments.values():
            if department.code == code:
                return department

        return None

    def list_by_branch(
        self,
        branch_id: str,
    ) -> list[Department]:
        return [
            department
            for department in self.departments.values()
            if department.branch_id == branch_id
        ]


def make_organization(
    *,
    organization_id: str,
    name: str,
    code: str,
) -> Organization:
    return Organization(
        organization_id=organization_id,
        name=name,
        code=code,
        industry="Technology",
        contact_email=f"{code.lower()}@test.com",
        is_active=True,
        created_at=datetime.now(UTC),
    )


def make_branch(
    *,
    branch_id: str,
    organization_id: str,
    name: str,
    code: str,
) -> Branch:
    return Branch(
        branch_id=branch_id,
        organization_id=organization_id,
        name=name,
        code=code,
        city="Lagos",
        state="Lagos",
        is_active=True,
        created_at=datetime.now(UTC),
    )


def make_department(
    *,
    department_id: str,
    organization_id: str,
    branch_id: str,
    name: str,
    code: str,
) -> Department:
    return Department(
        department_id=department_id,
        organization_id=organization_id,
        branch_id=branch_id,
        name=name,
        code=code,
        is_active=True,
        created_at=datetime.now(UTC),
    )


# ---------------------------------------------------------------------------
# Branch tenant-isolation tests
# ---------------------------------------------------------------------------


def test_branch_list_is_organization_scoped():
    organization_repository = FakeOrganizationRepository()
    branch_repository = FakeBranchRepository()

    organization_repository.organizations["org-001"] = make_organization(
        organization_id="org-001",
        name="Organization One",
        code="ORG1",
    )

    organization_repository.organizations["org-002"] = make_organization(
        organization_id="org-002",
        name="Organization Two",
        code="ORG2",
    )

    branch_one = make_branch(
        branch_id="branch-001",
        organization_id="org-001",
        name="Victoria Island",
        code="VI",
    )

    branch_two = make_branch(
        branch_id="branch-002",
        organization_id="org-002",
        name="Ikeja",
        code="IKEJA",
    )

    branch_repository.branches[branch_one.branch_id] = branch_one
    branch_repository.branches[branch_two.branch_id] = branch_two

    service = BranchService(
        branch_repository,
        organization_repository,
    )

    result = service.list_branches(
        "org-001",
        current_user_organization_id="org-001",
        current_user_role=UserRole.ADMIN,
    )

    assert [branch.branch_id for branch in result] == [
        "branch-001",
    ]


def test_branch_list_rejects_cross_tenant_access():
    organization_repository = FakeOrganizationRepository()
    branch_repository = FakeBranchRepository()

    organization_repository.organizations["org-001"] = make_organization(
        organization_id="org-001",
        name="Organization One",
        code="ORG1",
    )

    organization_repository.organizations["org-002"] = make_organization(
        organization_id="org-002",
        name="Organization Two",
        code="ORG2",
    )

    service = BranchService(
        branch_repository,
        organization_repository,
    )

    with pytest.raises(AuthorizationException):
        service.list_branches(
            "org-002",
            current_user_organization_id="org-001",
            current_user_role=UserRole.ADMIN,
        )


def test_branch_cannot_be_created_for_nonexistent_organization():
    organization_repository = FakeOrganizationRepository()
    branch_repository = FakeBranchRepository()

    service = BranchService(
        branch_repository,
        organization_repository,
    )

    with pytest.raises(PersistenceDataException):
        service.create_branch(
            organization_id="org-999",
            name="Unknown Branch",
            code="UNKNOWN",
            city="Lagos",
            state="Lagos",
            current_user_organization_id="org-999",
            current_user_role=UserRole.ADMIN,
        )


def test_branch_creation_preserves_organization_ownership():
    organization_repository = FakeOrganizationRepository()
    branch_repository = FakeBranchRepository()

    organization_repository.organizations["org-001"] = make_organization(
        organization_id="org-001",
        name="Organization One",
        code="ORG1",
    )

    service = BranchService(
        branch_repository,
        organization_repository,
    )

    branch = service.create_branch(
        organization_id="org-001",
        name="Victoria Island",
        code="VI",
        city="Lagos",
        state="Lagos",
        current_user_organization_id="org-001",
        current_user_role=UserRole.ADMIN,
    )

    assert branch.organization_id == "org-001"


def test_branch_creation_rejects_cross_tenant_organization():
    organization_repository = FakeOrganizationRepository()
    branch_repository = FakeBranchRepository()

    organization_repository.organizations["org-002"] = make_organization(
        organization_id="org-002",
        name="Organization Two",
        code="ORG2",
    )

    service = BranchService(
        branch_repository,
        organization_repository,
    )

    with pytest.raises(AuthorizationException):
        service.create_branch(
            organization_id="org-002",
            name="Ikeja",
            code="IKEJA",
            city="Lagos",
            state="Lagos",
            current_user_organization_id="org-001",
            current_user_role=UserRole.ADMIN,
        )


# ---------------------------------------------------------------------------
# Department tenant-isolation tests
# ---------------------------------------------------------------------------


def test_department_list_is_branch_scoped():
    organization_repository = FakeOrganizationRepository()
    branch_repository = FakeBranchRepository()
    department_repository = FakeDepartmentRepository()

    organization_repository.organizations["org-001"] = make_organization(
        organization_id="org-001",
        name="Organization One",
        code="ORG1",
    )

    organization_repository.organizations["org-002"] = make_organization(
        organization_id="org-002",
        name="Organization Two",
        code="ORG2",
    )

    branch_one = make_branch(
        branch_id="branch-001",
        organization_id="org-001",
        name="Victoria Island",
        code="VI",
    )

    branch_two = make_branch(
        branch_id="branch-002",
        organization_id="org-002",
        name="Ikeja",
        code="IKEJA",
    )

    department_one = make_department(
        department_id="dept-001",
        organization_id="org-001",
        branch_id="branch-001",
        name="Sales",
        code="SALES1",
    )

    department_two = make_department(
        department_id="dept-002",
        organization_id="org-002",
        branch_id="branch-002",
        name="Support",
        code="SUPPORT1",
    )

    branch_repository.branches[branch_one.branch_id] = branch_one
    branch_repository.branches[branch_two.branch_id] = branch_two

    department_repository.departments[
        department_one.department_id
    ] = department_one

    department_repository.departments[
        department_two.department_id
    ] = department_two

    service = DepartmentService(
        department_repository,
        branch_repository,
        organization_repository,
    )

    result = service.list_departments(
        "branch-001",
        current_user_organization_id="org-001",
        current_user_role=UserRole.ADMIN,
    )

    assert [department.department_id for department in result] == [
        "dept-001",
    ]


def test_department_list_rejects_cross_tenant_access():
    organization_repository = FakeOrganizationRepository()
    branch_repository = FakeBranchRepository()
    department_repository = FakeDepartmentRepository()

    organization_repository.organizations["org-001"] = make_organization(
        organization_id="org-001",
        name="Organization One",
        code="ORG1",
    )

    branch = make_branch(
        branch_id="branch-002",
        organization_id="org-002",
        name="Ikeja",
        code="IKEJA",
    )

    branch_repository.branches[branch.branch_id] = branch

    service = DepartmentService(
        department_repository,
        branch_repository,
        organization_repository,
    )

    with pytest.raises(AuthorizationException):
        service.list_departments(
            "branch-002",
            current_user_organization_id="org-001",
            current_user_role=UserRole.ADMIN,
        )


def test_department_cannot_be_created_for_nonexistent_organization():
    organization_repository = FakeOrganizationRepository()
    branch_repository = FakeBranchRepository()
    department_repository = FakeDepartmentRepository()

    service = DepartmentService(
        department_repository,
        branch_repository,
        organization_repository,
    )

    with pytest.raises(PersistenceDataException):
        service.create_department(
            organization_id="org-999",
            branch_id="branch-001",
            name="Sales",
            code="SALES",
            current_user_organization_id="org-999",
            current_user_role=UserRole.ADMIN,
        )


def test_department_cannot_be_created_for_nonexistent_branch():
    organization_repository = FakeOrganizationRepository()
    branch_repository = FakeBranchRepository()
    department_repository = FakeDepartmentRepository()

    organization_repository.organizations["org-001"] = make_organization(
        organization_id="org-001",
        name="Organization One",
        code="ORG1",
    )

    service = DepartmentService(
        department_repository,
        branch_repository,
        organization_repository,
    )

    with pytest.raises(PersistenceDataException):
        service.create_department(
            organization_id="org-001",
            branch_id="branch-999",
            name="Sales",
            code="SALES",
            current_user_organization_id="org-001",
            current_user_role=UserRole.ADMIN,
        )


def test_department_cannot_cross_organization_boundary():
    organization_repository = FakeOrganizationRepository()
    branch_repository = FakeBranchRepository()
    department_repository = FakeDepartmentRepository()

    organization_repository.organizations["org-001"] = make_organization(
        organization_id="org-001",
        name="Organization One",
        code="ORG1",
    )

    organization_repository.organizations["org-002"] = make_organization(
        organization_id="org-002",
        name="Organization Two",
        code="ORG2",
    )

    branch = make_branch(
        branch_id="branch-002",
        organization_id="org-002",
        name="Ikeja",
        code="IKEJA",
    )

    branch_repository.branches[branch.branch_id] = branch

    service = DepartmentService(
        department_repository,
        branch_repository,
        organization_repository,
    )

    with pytest.raises(AuthorizationException):
        service.create_department(
            organization_id="org-001",
            branch_id="branch-002",
            name="Sales",
            code="SALES",
            current_user_organization_id="org-001",
            current_user_role=UserRole.ADMIN,
        )


def test_department_creation_preserves_organization_and_branch_ownership():
    organization_repository = FakeOrganizationRepository()
    branch_repository = FakeBranchRepository()
    department_repository = FakeDepartmentRepository()

    organization_repository.organizations["org-001"] = make_organization(
        organization_id="org-001",
        name="Organization One",
        code="ORG1",
    )

    branch = make_branch(
        branch_id="branch-001",
        organization_id="org-001",
        name="Victoria Island",
        code="VI",
    )

    branch_repository.branches[branch.branch_id] = branch

    service = DepartmentService(
        department_repository,
        branch_repository,
        organization_repository,
    )

    department = service.create_department(
        organization_id="org-001",
        branch_id="branch-001",
        name="Sales",
        code="SALES",
        current_user_organization_id="org-001",
        current_user_role=UserRole.ADMIN,
    )

    assert department.organization_id == "org-001"
    assert department.branch_id == "branch-001"


def test_super_admin_can_operate_across_organizations():
    organization_repository = FakeOrganizationRepository()
    branch_repository = FakeBranchRepository()

    organization_repository.organizations["org-001"] = make_organization(
        organization_id="org-001",
        name="Organization One",
        code="ORG1",
    )

    service = BranchService(
        branch_repository,
        organization_repository,
    )

    branch = service.create_branch(
        organization_id="org-001",
        name="Victoria Island",
        code="VI",
        city="Lagos",
        state="Lagos",
        current_user_organization_id=None,
        current_user_role=UserRole.SUPER_ADMIN,
    )

    assert branch.organization_id == "org-001"