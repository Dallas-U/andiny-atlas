from fastapi import APIRouter, Depends

from app.dependencies import require_system_governor
from app.domain import User
from app.repositories.analytics_repository import AnalyticsRepository

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
)


@router.get(
    "/organization-overview",
    dependencies=[
        Depends(require_system_governor),
    ],
)
def get_organization_overview(
    current_user: User = Depends(require_system_governor),
):
    """
    Return investigation metrics grouped by organization.

    This is a platform-level dashboard and is restricted to Super Admin.
    """

    repository = AnalyticsRepository()

    return repository.get_organization_overview()