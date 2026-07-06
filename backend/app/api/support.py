from fastapi import APIRouter, Depends, HTTPException, Query
from app.dependencies import (
    get_case_manager,
    get_workflow_engine,
)
from app.models.statistics import Statistics

from app.models.support_case import SupportCase
from app.models.case_response import CaseResponse
from app.services.workflow_engine import WorkflowEngine
from app.services.case_manager import CaseManager

router = APIRouter()


@router.post("/investigate", response_model=CaseResponse)
def investigate(
    case: SupportCase,
    engine: WorkflowEngine = Depends(get_workflow_engine),
    case_manager: CaseManager = Depends(get_case_manager),
):

    result = engine.investigate(case)

    saved_case = case_manager.save_case(
        customer_name=case.customer_name, phone_number=case.phone_number, result=result
    )

    return saved_case


@router.get("/cases", response_model=list[CaseResponse])
def get_all_cases(
    customer_name: str | None = Query(default=None),
    phone_number: str | None = Query(default=None),
    case_manager: CaseManager = Depends(get_case_manager),
):

    return case_manager.search_cases(
        customer_name=customer_name, phone_number=phone_number
    )


@router.get("/cases/{case_id}", response_model=CaseResponse)
def get_case(
    case_id: str,
    case_manager: CaseManager = Depends(get_case_manager),
):

    case = case_manager.get_case_by_id(case_id)

    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")

    return case


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
