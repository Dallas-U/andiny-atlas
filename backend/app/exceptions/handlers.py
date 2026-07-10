from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.exceptions import (
    CaseNotFoundException,
    PersistenceDataException,
)
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


async def persistence_data_handler(
    request: Request,
    exc: PersistenceDataException,
):
    """Handle invalid persisted investigation data."""

    error = ErrorDetail(
        code="PERSISTENCE_DATA_ERROR",
        message=str(exc),
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": error.model_dump(),
        },
    )
