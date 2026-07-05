from fastapi import APIRouter

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