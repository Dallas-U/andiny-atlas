from enum import StrEnum

from pydantic import BaseModel, Field

from app.core.constants import InvestigationStatus


class SortOrder(StrEnum):
    """Supported sort directions."""

    ASC = "asc"
    DESC = "desc"


class CaseSortField(StrEnum):
    """Supported investigation sort fields."""

    TIMESTAMP = "timestamp"
    CUSTOMER_NAME = "customer_name"
    PHONE_NUMBER = "phone_number"
    STATUS = "status"
    CREATED_BY = "created_by"


class CaseQuery(BaseModel):
    """Validated investigation query options."""

    page: int = Field(
        default=1,
        ge=1,
    )

    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
    )

    customer_name: str | None = None
    phone_number: str | None = None
    created_by: str | None = None
    status: InvestigationStatus | None = None

    sort_by: CaseSortField = CaseSortField.TIMESTAMP
    sort_order: SortOrder = SortOrder.DESC
