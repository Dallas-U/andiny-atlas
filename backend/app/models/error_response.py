from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Represents a standardized API error."""

    code: str
    message: str


class ErrorResponse(BaseModel):
    """Standard API error response."""

    error: ErrorDetail
