from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.dependencies import (
    get_onboarding_service,
    require_super_admin,
)
from app.domain import User
from app.models.onboarding import (
    CreateCustomerOrganizationRequest,
    OnboardedOrganizationResponse,
)
from app.services.onboarding_service import OnboardingService


router = APIRouter()


@router.post(
    "/organizations",
    response_model=OnboardedOrganizationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Provision Customer Organization",
    description=(
        "Provision a new customer organization and its initial "
        "Customer Administrator. Restricted to Super Admin."
    ),
)
def provision_customer_organization(
    request: CreateCustomerOrganizationRequest,
    current_user: User = Depends(
        require_super_admin,
    ),
    service: OnboardingService = Depends(
        get_onboarding_service,
    ),
) -> OnboardedOrganizationResponse:

    return service.provision_customer_organization(
        request,
        current_user=current_user,
    )