from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr

from app.repositories.organization_repository import OrganizationRepository
from app.services.organization_service import OrganizationService

router = APIRouter()


class CreateOrganizationRequest(BaseModel):
    name: str
    code: str
    industry: str
    contact_email: EmailStr


class OrganizationResponse(BaseModel):
    organization_id: str
    name: str
    code: str
    industry: str
    contact_email: EmailStr
    is_active: bool


@router.post(
    "/",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create organization",
    description="Provision a new organization tenant in Andiny Atlas.",
)
def create_organization(
    request: CreateOrganizationRequest,
):

    service = OrganizationService(
        OrganizationRepository(),
    )

    organization = service.create_organization(
        name=request.name,
        code=request.code,
        industry=request.industry,
        contact_email=request.contact_email,
    )

    return OrganizationResponse(
        organization_id=organization.organization_id,
        name=organization.name,
        code=organization.code,
        industry=organization.industry,
        contact_email=organization.contact_email,
        is_active=organization.is_active,
    )


@router.get(
    "/",
    response_model=list[OrganizationResponse],
    summary="List organizations",
    description="Return all organizations registered in Andiny Atlas.",
)
def list_organizations():

    service = OrganizationService(
        OrganizationRepository(),
    )

    organizations = service.list_organizations()

    return [
        OrganizationResponse(
            organization_id=item.organization_id,
            name=item.name,
            code=item.code,
            industry=item.industry,
            contact_email=item.contact_email,
            is_active=item.is_active,
        )
        for item in organizations
    ]


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
    summary="Get organization",
    description="Return a single organization by its identifier.",
)
def get_organization(
    organization_id: str,
):

    service = OrganizationService(
        OrganizationRepository(),
    )

    organization = service.get_organization(
        organization_id,
    )

    if organization is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found.",
        )

    return OrganizationResponse(
        organization_id=organization.organization_id,
        name=organization.name,
        code=organization.code,
        industry=organization.industry,
        contact_email=organization.contact_email,
        is_active=organization.is_active,
    )