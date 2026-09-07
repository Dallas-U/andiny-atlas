from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.dependencies import (
    get_current_user,
    require_user_administrator,
)
from app.domain import User
from app.exceptions.exceptions import (
    AuthorizationException,
    PersistenceDataException,
)
from app.repositories.branch_repository import BranchRepository
from app.repositories.organization_repository import OrganizationRepository
from app.services.branch_service import BranchService


router = APIRouter()


class CreateBranchRequest(BaseModel):
    organization_id: str
    name: str
    code: str
    city: str
    state: str


class BranchResponse(BaseModel):
    branch_id: str
    organization_id: str
    name: str
    code: str
    city: str
    state: str
    is_active: bool


def _get_branch_service() -> BranchService:
    return BranchService(
        BranchRepository(),
        OrganizationRepository(),
    )


def _to_response(
    branch,
) -> BranchResponse:
    return BranchResponse(
        branch_id=branch.branch_id,
        organization_id=branch.organization_id,
        name=branch.name,
        code=branch.code,
        city=branch.city,
        state=branch.state,
        is_active=branch.is_active,
    )


@router.post(
    "/",
    response_model=BranchResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create branch",
    description=(
        "Provision a new branch beneath an organization. "
        "Customer administrators may only create branches "
        "within their own organization. Super Admin may "
        "provision branches across organizations."
    ),
)
def create_branch(
    request: CreateBranchRequest,
    current_user: User = Depends(
        require_user_administrator,
    ),
    service: BranchService = Depends(
        _get_branch_service,
    ),
) -> BranchResponse:

    try:
        branch = service.create_branch(
            organization_id=request.organization_id,
            name=request.name,
            code=request.code,
            city=request.city,
            state=request.state,
            current_user_organization_id=current_user.organization_id,
            current_user_role=current_user.role,
        )
    except AuthorizationException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to manage this organization.",
        ) from exc

    except PersistenceDataException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return _to_response(branch)


@router.get(
    "/organization/{organization_id}",
    response_model=list[BranchResponse],
    summary="List organization branches",
    description=(
        "Return branches belonging to an authorized organization. "
        "Customer users are restricted to their own organization."
    ),
)
def list_branches(
    organization_id: str,
    current_user: User = Depends(
        get_current_user,
    ),
    service: BranchService = Depends(
        _get_branch_service,
    ),
) -> list[BranchResponse]:

    try:
        branches = service.list_branches(
            organization_id,
            current_user_organization_id=current_user.organization_id,
            current_user_role=current_user.role,
        )
    except AuthorizationException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this organization.",
        ) from exc

    except PersistenceDataException as exc:
        if str(exc) == "Organization does not exist.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return [
        _to_response(item)
        for item in branches
    ]


@router.get(
    "/{branch_id}",
    response_model=BranchResponse,
    summary="Get branch",
    description=(
        "Return a branch only when it belongs to the "
        "authenticated user's organization. Super Admin "
        "may access branches across organizations."
    ),
)
def get_branch(
    branch_id: str,
    current_user: User = Depends(
        get_current_user,
    ),
    service: BranchService = Depends(
        _get_branch_service,
    ),
) -> BranchResponse:

    try:
        branch = service.get_branch(
            branch_id,
            current_user_organization_id=current_user.organization_id,
            current_user_role=current_user.role,
        )
    except AuthorizationException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this branch.",
        ) from exc

    if branch is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Branch not found.",
        )

    return _to_response(branch)


@router.patch(
    "/{branch_id}/activate",
    response_model=BranchResponse,
    summary="Activate branch",
    description=(
        "Activate a branch within the authenticated organization's "
        "tenant scope."
    ),
)
def activate_branch(
    branch_id: str,
    current_user: User = Depends(
        require_user_administrator,
    ),
    service: BranchService = Depends(
        _get_branch_service,
    ),
) -> BranchResponse:

    try:
        branch = service.activate_branch(
            branch_id,
            current_user_organization_id=current_user.organization_id,
            current_user_role=current_user.role,
        )
    except AuthorizationException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to manage this branch.",
        ) from exc

    except PersistenceDataException as exc:
        if str(exc) == "Branch not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return _to_response(branch)


@router.patch(
    "/{branch_id}/deactivate",
    response_model=BranchResponse,
    summary="Deactivate branch",
    description=(
        "Deactivate a branch within the authenticated organization's "
        "tenant scope."
    ),
)
def deactivate_branch(
    branch_id: str,
    current_user: User = Depends(
        require_user_administrator,
    ),
    service: BranchService = Depends(
        _get_branch_service,
    ),
) -> BranchResponse:

    try:
        branch = service.deactivate_branch(
            branch_id,
            current_user_organization_id=current_user.organization_id,
            current_user_role=current_user.role,
        )
    except AuthorizationException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to manage this branch.",
        ) from exc

    except PersistenceDataException as exc:
        if str(exc) == "Branch not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return _to_response(branch)