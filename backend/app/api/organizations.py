from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

from app.dependencies import require_super_admin
from app.domain import User
from app.exceptions.exceptions import PersistenceDataException
from app.repositories.organization_repository import (
    OrganizationRepository,
)
from app.services.organization_service import (
    OrganizationService,
)


router = APIRouter()


class CreateOrganizationRequest(BaseModel):
    name: str
    code: str
    industry: str
    contact_email: EmailStr


class UpdateOrganizationConfigurationRequest(BaseModel):
    """
    Request used to update configurable organization fields.

    Organization identity, code, lifecycle status,
    and creation metadata are intentionally excluded.
    """

    name: str
    industry: str
    contact_email: EmailStr


class OrganizationResponse(BaseModel):
    organization_id: str
    name: str
    code: str
    industry: str
    contact_email: EmailStr
    is_active: bool


def _get_organization_service() -> OrganizationService:
    return OrganizationService(
        OrganizationRepository(),
    )


def _to_response(
    organization,
) -> OrganizationResponse:
    return OrganizationResponse(
        organization_id=organization.organization_id,
        name=organization.name,
        code=organization.code,
        industry=organization.industry,
        contact_email=organization.contact_email,
        is_active=organization.is_active,
    )


@router.post(
    "/",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create organization",
    description=(
        "Provision a new organization tenant. "
        "Restricted to Super Admin platform governance."
    ),
)
def create_organization(
    request: CreateOrganizationRequest,
    _current_user: User = Depends(
        require_super_admin,
    ),
    service: OrganizationService = Depends(
        _get_organization_service,
    ),
) -> OrganizationResponse:

    try:
        organization = service.create_organization(
            name=request.name,
            code=request.code,
            industry=request.industry,
            contact_email=str(
                request.contact_email,
            ),
        )
    except PersistenceDataException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return _to_response(organization)


@router.get(
    "/",
    response_model=list[OrganizationResponse],
    summary="List organizations",
    description=(
        "Return organizations registered in Andiny Atlas. "
        "Restricted to Super Admin platform governance."
    ),
)
def list_organizations(
    _current_user: User = Depends(
        require_super_admin,
    ),
    service: OrganizationService = Depends(
        _get_organization_service,
    ),
) -> list[OrganizationResponse]:

    organizations = service.list_organizations()

    return [
        _to_response(item)
        for item in organizations
    ]


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
    summary="Get organization",
    description=(
        "Return an organization by identifier. "
        "Restricted to Super Admin platform governance."
    ),
)
def get_organization(
    organization_id: str,
    _current_user: User = Depends(
        require_super_admin,
    ),
    service: OrganizationService = Depends(
        _get_organization_service,
    ),
) -> OrganizationResponse:

    organization = service.get_organization(
        organization_id,
    )

    if organization is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found.",
        )

    return _to_response(organization)


@router.patch(
    "/{organization_id}/configuration",
    response_model=OrganizationResponse,
    summary="Update organization configuration",
    description=(
        "Update configurable organization profile fields. "
        "Organization identity, organization code, lifecycle "
        "status, and creation metadata cannot be modified "
        "through this endpoint. Restricted to Super Admin "
        "platform governance."
    ),
)
def update_organization_configuration(
    organization_id: str,
    request: UpdateOrganizationConfigurationRequest,
    _current_user: User = Depends(
        require_super_admin,
    ),
    service: OrganizationService = Depends(
        _get_organization_service,
    ),
) -> OrganizationResponse:

    try:
        organization = (
            service.update_organization_configuration(
                organization_id=organization_id,
                name=request.name,
                industry=request.industry,
                contact_email=str(
                    request.contact_email,
                ),
            )
        )

    except PersistenceDataException as exc:
        if str(exc) == "Organization not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return _to_response(organization)


@router.patch(
    "/{organization_id}/activate",
    response_model=OrganizationResponse,
    summary="Activate organization",
    description=(
        "Activate a customer organization tenant. "
        "Restricted to Super Admin platform governance."
    ),
)
def activate_organization(
    organization_id: str,
    _current_user: User = Depends(
        require_super_admin,
    ),
    service: OrganizationService = Depends(
        _get_organization_service,
    ),
) -> OrganizationResponse:

    try:
        organization = service.activate_organization(
            organization_id,
        )

    except PersistenceDataException as exc:
        if str(exc) == "Organization not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return _to_response(organization)


@router.patch(
    "/{organization_id}/deactivate",
    response_model=OrganizationResponse,
    summary="Deactivate organization",
    description=(
        "Deactivate a customer organization tenant. "
        "Restricted to Super Admin platform governance. "
        "Inactive organizations will lose operational "
        "access when tenant access enforcement is applied."
    ),
)
def deactivate_organization(
    organization_id: str,
    _current_user: User = Depends(
        require_super_admin,
    ),
    service: OrganizationService = Depends(
        _get_organization_service,
    ),
) -> OrganizationResponse:

    try:
        organization = service.deactivate_organization(
            organization_id,
        )

    except PersistenceDataException as exc:
        if str(exc) == "Organization not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return _to_response(organization)