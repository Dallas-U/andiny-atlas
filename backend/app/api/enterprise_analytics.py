from __future__ import annotations

from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.domain import User
from app.repositories.enterprise_analytics_repository import (
    EnterpriseAnalyticsRepository,
)
from app.services.enterprise_analytics_service import (
    EnterpriseAnalyticsService,
)

router = APIRouter()


def _get_service() -> EnterpriseAnalyticsService:
    return EnterpriseAnalyticsService(
        EnterpriseAnalyticsRepository(),
    )


@router.get(
    "/organization/{organization_id}",
    summary="Organization executive analytics",
    description=(
        "Return executive KPI metrics for an organization. "
        "Customer users may only access their own organization."
    ),
)
def get_organization_analytics(
    organization_id: str,
    current_user: User = Depends(get_current_user),
    service: EnterpriseAnalyticsService = Depends(_get_service),
):

    summary = service.get_organization_summary(
        organization_id,
        current_user=current_user,
    )

    return {
        "organization_id": organization_id,
        "kpis": {
            "total_cases": summary.total_cases,
            "resolved_cases": summary.resolved_cases,
            "waiting_cases": summary.waiting_cases,
            "technical_investigation_cases": (
                summary.technical_investigation_cases
            ),
            "escalated_cases": summary.escalated_cases,
            "resolution_rate": summary.resolution_rate,
            "escalation_rate": summary.escalation_rate,
        },
    }


@router.get(
    "/organization/{organization_id}/branches",
    summary="Branch executive analytics",
    description=(
        "Return executive metrics for branches within an organization."
    ),
)
def get_branch_analytics(
    organization_id: str,
    current_user: User = Depends(get_current_user),
    service: EnterpriseAnalyticsService = Depends(_get_service),
):

    summaries = service.get_branch_summaries(
        organization_id,
        current_user=current_user,
    )

    return {
        "organization_id": organization_id,
        "branches": [
            {
                "branch_id": item.branch_id,
                "branch_name": item.branch_name,
                "total_cases": item.total_cases,
                "resolved_cases": item.resolved_cases,
                "escalation_rate": item.escalation_rate,
            }
            for item in summaries
        ],
    }


@router.get(
    "/branch/{branch_id}/departments",
    summary="Department executive analytics",
    description=(
        "Return executive metrics for departments within a branch."
    ),
)
def get_department_analytics(
    branch_id: str,
    current_user: User = Depends(get_current_user),
    service: EnterpriseAnalyticsService = Depends(_get_service),
):

    summaries = service.get_department_summaries(
        branch_id,
        current_user=current_user,
    )

    return {
        "branch_id": branch_id,
        "departments": [
            {
                "department_id": item.department_id,
                "department_name": item.department_name,
                "total_cases": item.total_cases,
                "resolved_cases": item.resolved_cases,
                "escalation_rate": item.escalation_rate,
            }
            for item in summaries
        ],
    }