from pydantic import BaseModel


class Statistics(BaseModel):
    total_cases: int
    resolved_cases: int
    pending_cases: int
    escalated_cases: int
