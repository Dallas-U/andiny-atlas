from datetime import date

from app.repositories.analytics_repository import AnalyticsRepository
from fastapi import APIRouter, Depends, Query

from app.dependencies import (
    get_analytics_service,
    get_current_user,
    require_system_governor,
)
from app.domain import User
from app.models.analytics import (
    AnalyticsInterval,
    InvestigationAnalyticsResponse,
)
from app.services.analytics_service import AnalyticsService

router = APIRouter()


@router.get(
    "/overview",
    response_model=InvestigationAnalyticsResponse,
    summary="Investigation analytics overview",
    description=(
        "Return tenant-scoped investigation analytics for the "
        "authenticated user's organization."
    ),
)
def analytics_overview(
    start_date: date = Query(...),
    end_date: date = Query(...),
    interval: AnalyticsInterval = Query(
        AnalyticsInterval.DAY,
    ),
    current_user: User = Depends(get_current_user),
    service: AnalyticsService = Depends(get_analytics_service),
):

    kpis = service.get_kpis(
        start_date,
        end_date,
        current_user=current_user,
    )

    status_distribution = service.get_status_distribution(
        start_date,
        end_date,
        current_user=current_user,
    )

    trend = service.get_trend(
        start_date,
        end_date,
        interval,
        current_user=current_user,
    )

    investigator_workload = service.get_investigator_workload(
        start_date,
        end_date,
        current_user=current_user,
    )

    return InvestigationAnalyticsResponse(
        start_date=start_date,
        end_date=end_date,
        interval=interval,
        kpis=kpis,
        status_distribution=status_distribution,
        trend=trend,
        investigator_workload=investigator_workload,
    )


@router.get(
    "/organizations",
    dependencies=[
        Depends(require_system_governor),
    ],
    summary="Organization analytics",
    description=(
        "Return organization-level analytics across the Atlas platform. "
        "Super Admin only."
    ),
)
def organization_analytics(
    current_user: User = Depends(require_system_governor),
):

    service = AnalyticsService(
        AnalyticsRepository(),
    )

    return service.repository.get_organization_overview()