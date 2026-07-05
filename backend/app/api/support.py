from fastapi import APIRouter, HTTPException

from app.models.support_case import SupportCase
from app.services.workflow_engine import WorkflowEngine
from app.services.case_manager import CaseManager

router = APIRouter()

engine = WorkflowEngine()
case_manager = CaseManager()


@router.post("/investigate")
def investigate(case: SupportCase):

    result = engine.investigate(case)

    saved_case = case_manager.save_case(
        customer_name=case.customer_name,
        phone_number=case.phone_number,
        result=result
    )

    return saved_case
@router.get("/cases")
@router.get("/cases/{case_id}")
def get_case(case_id: str):

    case = case_manager.get_case_by_id(case_id)

    if case is None:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    return case
def get_all_cases():

    return case_manager.get_all_cases()