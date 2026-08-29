from datetime import date

from pydantic import BaseModel, Field, model_validator

from app.core.constants import InvestigationStatus
from app.models.case_response import CaseResponse


class InvestigationReportQuery(BaseModel):
    """Validated filters for an investigation summary report."""

    start_date: date
    end_date: date
    status: InvestigationStatus | None = None

    @model_validator(mode="after")
    def validate_date_range(self):
        if self.end_date < self.start_date:
            raise ValueError(
                "end_date must be on or after start_date."
            )

        return self


class InvestigationReportSummary(BaseModel):
    """Summary totals for an investigation report."""

    total_cases: int = Field(ge=0)
    resolved_cases: int = Field(ge=0)
    waiting_cases: int = Field(ge=0)
    technical_investigation_cases: int = Field(ge=0)
    escalated_cases: int = Field(ge=0)


class InvestigationReportResponse(BaseModel):
    """Investigation report data for a selected period."""

    start_date: date
    end_date: date
    applied_status: InvestigationStatus | None
    summary: InvestigationReportSummary
    items: list[CaseResponse]