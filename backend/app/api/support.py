from fastapi import APIRouter

from app.models.support_case import SupportCase
from app.services.workflow_engine import WorkflowEngine

router = APIRouter()

engine = WorkflowEngine()


@router.post("/investigate")
def investigate(case: SupportCase):

    return engine.investigate(case)