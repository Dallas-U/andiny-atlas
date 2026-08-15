from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.repositories.branch_repository import BranchRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.organization_repository import OrganizationRepository
from app.services.department_service import DepartmentService

router = APIRouter()


class CreateDepartmentRequest(BaseModel):
    organization_id: str
    branch_id: str
    name: str
    code: str


class DepartmentResponse(BaseModel):
    department_id: str
    organization_id: str
    branch_id: str
    name: str
    code: str
    is_active: bool


@router.post(
    "/",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create department",
    description="Provision a new department beneath a branch.",
)
def create_department(
    request: CreateDepartmentRequest,
):

    service = DepartmentService(
        DepartmentRepository(),
        BranchRepository(),
        OrganizationRepository(),
    )

    department = service.create_department(
        organization_id=request.organization_id,
        branch_id=request.branch_id,
        name=request.name,
        code=request.code,
    )

    return DepartmentResponse(
        department_id=department.department_id,
        organization_id=department.organization_id,
        branch_id=department.branch_id,
        name=department.name,
        code=department.code,
        is_active=department.is_active,
    )


@router.get(
    "/branch/{branch_id}",
    response_model=list[DepartmentResponse],
    summary="List branch departments",
    description="Return all departments belonging to a branch.",
)
def list_departments(
    branch_id: str,
):

    service = DepartmentService(
        DepartmentRepository(),
        BranchRepository(),
        OrganizationRepository(),
    )

    departments = service.list_departments(
        branch_id,
    )

    return [
        DepartmentResponse(
            department_id=item.department_id,
            organization_id=item.organization_id,
            branch_id=item.branch_id,
            name=item.name,
            code=item.code,
            is_active=item.is_active,
        )
        for item in departments
    ]


@router.get(
    "/{department_id}",
    response_model=DepartmentResponse,
    summary="Get department",
    description="Return a department by its identifier.",
)
def get_department(
    department_id: str,
):

    service = DepartmentService(
        DepartmentRepository(),
        BranchRepository(),
        OrganizationRepository(),
    )

    department = service.get_department(
        department_id,
    )

    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found.",
        )

    return DepartmentResponse(
        department_id=department.department_id,
        organization_id=department.organization_id,
        branch_id=department.branch_id,
        name=department.name,
        code=department.code,
        is_active=department.is_active,
    )