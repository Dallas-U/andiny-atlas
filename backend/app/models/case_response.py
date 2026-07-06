from pydantic import BaseModel


class InvestigationResult(BaseModel):

    status: str
    reason: str
    next_action: str


class CaseResponse(BaseModel):

    case_id: str
    timestamp: str
    customer_name: str
    phone_number: str
    result: InvestigationResult
