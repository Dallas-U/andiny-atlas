from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.exceptions import CaseNotFoundException
from app.models.error_response import ErrorDetail


async def case_not_found_handler(
    request: Request,
    exc: CaseNotFoundException,
):
    """Handle missing investigation cases."""

    error = ErrorDetail(
        code="CASE_NOT_FOUND",
        message=str(exc),
    )

    return JSONResponse(
        status_code=404,
        content={
            "error": error.model_dump(),
        },
    )
