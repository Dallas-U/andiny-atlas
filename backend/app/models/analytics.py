from datetime import date
from enum import StrEnum

from pydantic import BaseModel, Field, model_validator


class AnalyticsInterval(StrEnum):
    """Supported time-grouping intervals for analytics."""

    DAY = "day"
    WEEK = "week"
    MONTH = "month"


class InvestigationAnalyticsQuery(BaseModel):
    """Validated filters for investigation analytics."""

    start_date: date
    end_date: date
    interval: AnalyticsInterval = AnalyticsInterval.DAY

    @model_validator(mode="after")
    def validate_date_range(self):
        if self.end_date < self.start_date:
            raise ValueError(
                "end_date must be on or after start_date."
            )

        return self


class InvestigationAnalyticsKpis(BaseModel):
    """High-level investigation analytics metrics."""

    total_cases: int = Field(ge=0)
    resolved_cases: int = Field(ge=0)
    waiting_cases: int = Field(ge=0)
    technical_investigation_cases: int = Field(ge=0)
    escalated_cases: int = Field(ge=0)

    resolution_rate: float = Field(
        ge=0,
        le=100,
    )

    escalation_rate: float = Field(
        ge=0,
        le=100,
    )


class StatusDistributionItem(BaseModel):
    """One investigation-status distribution value."""

    status: str
    count: int = Field(ge=0)
    percentage: float = Field(
        ge=0,
        le=100,
    )


class InvestigationTrendItem(BaseModel):
    """Investigation volume grouped into one time bucket."""

    period: str
    count: int = Field(ge=0)


class InvestigatorWorkloadItem(BaseModel):
    """Investigation volume created by one application user."""

    investigator_id: str
    investigator_name: str
    count: int = Field(ge=0)


class InvestigationAnalyticsResponse(BaseModel):
    """Operational analytics for an inclusive date range."""

    start_date: date
    end_date: date
    interval: AnalyticsInterval

    kpis: InvestigationAnalyticsKpis

    status_distribution: list[
        StatusDistributionItem
    ]

    trend: list[
        InvestigationTrendItem
    ]

    investigator_workload: list[
        InvestigatorWorkloadItem
    ]