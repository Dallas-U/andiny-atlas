from fastapi import APIRouter, Depends, Query

from app.database.models import User
from app.dependencies import (
    get_case_manager,
    get_current_user,
    get_workflow_engine,
)
from app.models.case_response import CaseResponse
from app.models.error_response import ErrorResponse
from app.models.statistics import Statistics
from app.models.support_case import SupportCase
from app.services.case_manager import CaseManager
from app.services.workflow_engine import WorkflowEngine

router = APIRouter(
    dependencies=[
        Depends(get_current_user),
    ],
)


@router.post(
    "/investigate",
    response_model=CaseResponse,
)
def investigate(
    case: SupportCase,
    engine: WorkflowEngine = Depends(get_workflow_engine),
    case_manager: CaseManager = Depends(get_case_manager),
    current_user: User = Depends(get_current_user),
):

    return case_manager.investigate_case(
        case,
        engine,
        current_user,
    )


@router.get(
    "/cases",
    response_model=list[CaseResponse],
)
def get_all_cases(
    customer_name: str | None = Query(default=None),
    phone_number: str | None = Query(default=None),
    case_manager: CaseManager = Depends(get_case_manager),
):

    return case_manager.search_cases(
        customer_name=customer_name,
        phone_number=phone_number,
    )


@router.get(
    "/cases/{case_id}",
    response_model=CaseResponse,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Case not found",
        }
    },
)
def get_case(
    case_id: str,
    case_manager: CaseManager = Depends(get_case_manager),
):

    return case_manager.get_case_by_id(case_id)


@router.get(
    "/statistics",
    response_model=Statistics,
    summary="Get Investigation Statistics",
    description="Returns summary statistics for all investigations.",
)
def get_statistics(
    case_manager: CaseManager = Depends(get_case_manager),
):

    return case_manager.get_statistics()
