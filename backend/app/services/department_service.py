from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from app.domain.department import Department
from app.exceptions.exceptions import PersistenceDataException
from app.repositories.branch_repository import BranchRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.organization_repository import OrganizationRepository


class DepartmentService:
    """
    Business logic for department management within
    the Andiny Atlas enterprise platform.

    Responsible for department provisioning, validation,
    retrieval, and hierarchy enforcement.
    """

    def __init__(
        self,
        department_repository: DepartmentRepository,
        branch_repository: BranchRepository,
        organization_repository: OrganizationRepository,
    ) -> None:
        self.department_repository = department_repository
        self.branch_repository = branch_repository
        self.organization_repository = organization_repository

    def create_department(
        self,
        *,
        organization_id: str,
        branch_id: str,
        name: str,
        code: str,
    ) -> Department:

        organization = self.organization_repository.get_by_id(
            organization_id,
        )

        if organization is None:
            raise PersistenceDataException(
                "Organization does not exist."
            )

        branch = self.branch_repository.get_by_id(
            branch_id,
        )

        if branch is None:
            raise PersistenceDataException(
                "Branch does not exist."
            )

        if branch.organization_id != organization_id:
            raise PersistenceDataException(
                "Branch does not belong to the organization."
            )

        existing = self.department_repository.get_by_code(
            code,
        )

        if existing is not None:
            raise PersistenceDataException(
                "Department code already exists."
            )

        department = Department(
            department_id=str(uuid4()),
            organization_id=organization_id,
            branch_id=branch_id,
            name=name,
            code=code,
            is_active=True,
            created_at=datetime.utcnow(),
        )

        return self.department_repository.create(
            department,
        )

    def list_departments(
        self,
        branch_id: str,
    ) -> list[Department]:

        return self.department_repository.list_by_branch(
            branch_id,
        )

    def get_department(
        self,
        department_id: str,
    ) -> Department | None:

        return self.department_repository.get_by_id(
            department_id,
        )