from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.dependencies import (
    get_user_administration_service,
    require_system_governor,
    require_user_administrator,
)
from app.domain import User
from app.models.admin import (
    AdminUserListResponse,
    AdminUserResponse,
    ChangeUserRoleRequest,
    CreateAdminUserRequest,
)
from app.services.user_administration_service import (
    UserAdministrationService,
)

router = APIRouter()


@router.post(
    "/users",
    response_model=AdminUserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Provision User",
    description=(
        "Provision a new Andiny Atlas application user. "
        "Customer administrators can only provision users "
        "inside their authenticated organization. "
        "Super Admin can provision platform or customer users."
    ),
)
def create_user(
    request: CreateAdminUserRequest,
    current_user: User = Depends(
        require_user_administrator,
    ),
    service: UserAdministrationService = Depends(
        get_user_administration_service,
    ),
) -> AdminUserResponse:

    user = service.create_user(
        request,
        current_user=current_user,
    )

    return AdminUserResponse.model_validate(user)


@router.get(
    "/users",
    response_model=AdminUserListResponse,
    summary="List Users",
    description=(
        "Returns a paginated list of users visible to the "
        "authenticated administrator. Customer administrators "
        "are restricted to their own organization."
    ),
)
def list_users(
    page: Annotated[
        int,
        Query(
            ge=1,
            description="Page number.",
        ),
    ] = 1,
    page_size: Annotated[
        int,
        Query(
            ge=1,
            le=100,
            description="Maximum number of users returned per page.",
        ),
    ] = 20,
    current_user: User = Depends(
        require_user_administrator,
    ),
    service: UserAdministrationService = Depends(
        get_user_administration_service,
    ),
) -> AdminUserListResponse:

    result = service.list_users(
        current_user=current_user,
        page=page,
        page_size=page_size,
    )

    return AdminUserListResponse(
        users=[
            AdminUserResponse.model_validate(user)
            for user in result.users
        ],
        page=result.page,
        page_size=result.page_size,
        total=result.total,
        total_pages=result.total_pages,
    )


@router.get(
    "/users/{user_id}",
    response_model=AdminUserResponse,
    responses={
        404: {
            "description": (
                "User not found or outside the authenticated "
                "organization."
            ),
        },
    },
    summary="Get User",
    description=(
        "Return a user visible to the authenticated administrator."
    ),
)
def get_user(
    user_id: str,
    current_user: User = Depends(
        require_user_administrator,
    ),
    service: UserAdministrationService = Depends(
        get_user_administration_service,
    ),
) -> AdminUserResponse:

    user = service.get_user(
        user_id=user_id,
        current_user=current_user,
    )

    if user is None:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return AdminUserResponse.model_validate(user)


@router.patch(
    "/users/{user_id}/role",
    response_model=AdminUserResponse,
    responses={
        403: {
            "description": (
                "Forbidden. Only Super Admin can change roles, "
                "and a Super Admin cannot change their own role."
            ),
        },
        404: {
            "description": "User not found.",
        },
    },
    summary="Change User Role",
    description=(
        "Change an application's user authorization role. "
        "Restricted to Super Admin. A Super Admin cannot "
        "change their own role."
    ),
)
def change_user_role(
    user_id: str,
    request: ChangeUserRoleRequest,
    current_user: User = Depends(
        require_system_governor,
    ),
    service: UserAdministrationService = Depends(
        get_user_administration_service,
    ),
) -> AdminUserResponse:

    user = service.change_role(
        user_id=user_id,
        role=request.role,
        current_user_id=current_user.id,
        current_user=current_user,
    )

    return AdminUserResponse.model_validate(user)


@router.post(
    "/users/{user_id}/activate",
    response_model=AdminUserResponse,
    responses={
        404: {
            "description": (
                "User not found or outside the authenticated "
                "organization."
            ),
        },
    },
    summary="Activate User",
    description=(
        "Activate a user visible to the authenticated administrator."
    ),
)
def activate_user(
    user_id: str,
    current_user: User = Depends(
        require_user_administrator,
    ),
    service: UserAdministrationService = Depends(
        get_user_administration_service,
    ),
) -> AdminUserResponse:

    user = service.activate_user(
        user_id=user_id,
        current_user=current_user,
    )

    return AdminUserResponse.model_validate(user)


@router.post(
    "/users/{user_id}/deactivate",
    response_model=AdminUserResponse,
    responses={
        403: {
            "description": (
                "Forbidden. A user cannot deactivate "
                "their own account."
            ),
        },
        404: {
            "description": (
                "User not found or outside the authenticated "
                "organization."
            ),
        },
    },
    summary="Deactivate User",
    description=(
        "Deactivate a user visible to the authenticated administrator. "
        "Users cannot deactivate their own account."
    ),
)
def deactivate_user(
    user_id: str,
    current_user: User = Depends(
        require_user_administrator,
    ),
    service: UserAdministrationService = Depends(
        get_user_administration_service,
    ),
) -> AdminUserResponse:

    user = service.deactivate_user(
        user_id=user_id,
        current_user_id=current_user.id,
        current_user=current_user,
    )

    return AdminUserResponse.model_validate(user)