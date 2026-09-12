import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi import HTTPException
from sqlalchemy import text

from app.database.session import engine

from app.api.admin import router as admin_router
from app.api.analytics import router as analytics_router
from app.api.auth import router as auth_router
from app.api.branches import router as branches_router
from app.api.departments import router as departments_router
from app.api.enterprise_analytics import (
    router as enterprise_analytics_router,
)
from app.api.exports import router as exports_router
from app.api.onboarding import router as onboarding_router
from app.api.organization_analytics import (
    router as organization_analytics_router,
)
from app.api.organizations import router as organizations_router
from app.api.reports import router as reports_router
from app.api.support import router as support_router
from app.core.logging import setup_logging
from app.core.settings import settings
from app.exceptions.exceptions import (
    AuthorizationException,
    CaseNotFoundException,
    InactiveUserException,
    InvalidCredentialsException,
    InvalidTokenException,
    PersistenceDataException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.exceptions.handlers import (
    authorization_handler,
    case_not_found_handler,
    inactive_user_handler,
    invalid_credentials_handler,
    invalid_token_handler,
    persistence_data_handler,
    user_already_exists_handler,
    user_not_found_handler,
)


setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Manage application startup and shutdown."""

    logger.info(
        "%s v%s starting in %s mode",
        settings.app_name,
        settings.app_version,
        settings.environment,
    )

    yield

    logger.info(
        "%s shutting down",
        settings.app_name,
    )


app = FastAPI(
    lifespan=lifespan,
    title=settings.app_name,
    description="""
Andiny Atlas is an AI-powered investigation engine for support agents.

## Features

- Register and authenticate application users
- Issue and validate JWT access tokens
- Identify authenticated users
- Administer application users securely
- Investigate customer support cases
- Store investigation history
- Search previous investigations
- Retrieve cases by ID
- View investigation statistics
- Generate investigation reports
- Export reports and analytics
- Maintain immutable export audit records
- Support enterprise organization structures
- Support organization, branch, and department isolation
""",
    version=settings.app_version,
    contact={
        "name": "Dallas Uzo",
    },
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_exception_handler(
    CaseNotFoundException,
    case_not_found_handler,
)

app.add_exception_handler(
    PersistenceDataException,
    persistence_data_handler,
)

app.add_exception_handler(
    InvalidCredentialsException,
    invalid_credentials_handler,
)

app.add_exception_handler(
    InvalidTokenException,
    invalid_token_handler,
)

app.add_exception_handler(
    UserAlreadyExistsException,
    user_already_exists_handler,
)

app.add_exception_handler(
    UserNotFoundException,
    user_not_found_handler,
)

app.add_exception_handler(
    InactiveUserException,
    inactive_user_handler,
)

app.add_exception_handler(
    AuthorizationException,
    authorization_handler,
)


app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"],
)

app.include_router(
    support_router,
    prefix="/support",
    tags=["Investigations"],
)

app.include_router(
    admin_router,
    prefix="/admin",
    tags=["Administration"],
)

app.include_router(
    reports_router,
    prefix="/reports",
    tags=["Reports"],
)

app.include_router(
    analytics_router,
    prefix="/analytics",
    tags=["Analytics"],
)

app.include_router(
    branches_router,
    prefix="/branches",
    tags=["Branches"],
)

app.include_router(
    organizations_router,
    prefix="/organizations",
    tags=["Organizations"],
)

app.include_router(
    departments_router,
    prefix="/departments",
    tags=["Departments"],
)

app.include_router(
    onboarding_router,
    prefix="/onboarding",
    tags=["Onboarding"],
)

app.include_router(
    exports_router,
    prefix="/exports",
    tags=["Exports"],
)

app.include_router(
    enterprise_analytics_router,
    prefix="/enterprise-analytics",
    tags=["Enterprise Analytics"],
)

app.include_router(
    organization_analytics_router,
)


@app.get(
    "/",
    summary="Root Endpoint",
    description="Returns a welcome message.",
)
def root():
    """Return basic application information."""

    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
    }


@app.get(
    "/health",
    summary="Health Check",
    description="Returns the current application status.",
)
def health():
    """Return the general application health status."""

    return {
        "status": "running",
        "service": settings.app_name,
        "environment": settings.environment,
        "version": settings.app_version,
    }


@app.get(
    "/health/live",
    summary="Liveness Check",
    description="Confirms that the application process is running.",
)
def liveness():
    """Return the application liveness status."""

    return {
        "status": "alive",
        "service": settings.app_name,
        "environment": settings.environment,
        "version": settings.app_version,
    }


@app.get(
    "/health/ready",
    summary="Readiness Check",
    description="Confirms that the application and database are ready to serve requests.",
)
def readiness():
    """Return the application readiness status."""

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "ready",
            "database": "available",
            "service": settings.app_name,
            "environment": settings.environment,
            "version": settings.app_version,
        }

    except Exception as exc:
        logger.exception("Database readiness check failed.")

        raise HTTPException(
            status_code=503,
            detail={
                "status": "not_ready",
                "database": "unavailable",
                "service": settings.app_name,
                "environment": settings.environment,
                "version": settings.app_version,
            },
        ) from exc