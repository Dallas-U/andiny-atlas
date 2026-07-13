from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.exceptions import (
    CaseNotFoundException,
    InactiveUserException,
    InvalidCredentialsException,
    InvalidTokenException,
    PersistenceDataException,
    UserAlreadyExistsException,
    UserNotFoundException,
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
    """Handle persistence failures."""

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


async def invalid_credentials_handler(
    request: Request,
    exc: InvalidCredentialsException,
):
    """Handle invalid login credentials."""

    error = ErrorDetail(
        code="INVALID_CREDENTIALS",
        message=str(exc),
    )

    return JSONResponse(
        status_code=401,
        content={
            "error": error.model_dump(),
        },
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )


async def invalid_token_handler(
    request: Request,
    exc: InvalidTokenException,
):
    """Handle invalid or expired access tokens."""

    error = ErrorDetail(
        code="INVALID_TOKEN",
        message=str(exc),
    )

    return JSONResponse(
        status_code=401,
        content={
            "error": error.model_dump(),
        },
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )


async def user_already_exists_handler(
    request: Request,
    exc: UserAlreadyExistsException,
):
    """Handle duplicate user registration."""

    error = ErrorDetail(
        code="USER_ALREADY_EXISTS",
        message=str(exc),
    )

    return JSONResponse(
        status_code=409,
        content={
            "error": error.model_dump(),
        },
    )


async def user_not_found_handler(
    request: Request,
    exc: UserNotFoundException,
):
    """Handle missing application users."""

    error = ErrorDetail(
        code="USER_NOT_FOUND",
        message=str(exc),
    )

    return JSONResponse(
        status_code=404,
        content={
            "error": error.model_dump(),
        },
    )


async def inactive_user_handler(
    request: Request,
    exc: InactiveUserException,
):
    """Handle authentication attempts by inactive users."""

    error = ErrorDetail(
        code="INACTIVE_USER",
        message=str(exc),
    )

    return JSONResponse(
        status_code=403,
        content={
            "error": error.model_dump(),
        },
    )
