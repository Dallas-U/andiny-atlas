import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.support import router as support_router
from app.core.logging import setup_logging
from app.core.settings import settings
from app.exceptions.exceptions import (
    CaseNotFoundException,
    PersistenceDataException,
)
from app.exceptions.handlers import (
    case_not_found_handler,
    persistence_data_handler,
)

# Initialize logging
setup_logging()

# Create a logger for this module
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


# Create the FastAPI application
app = FastAPI(
    lifespan=lifespan,
    title=settings.app_name,
    description="""
Andiny Atlas is an AI-powered investigation engine for support agents.

## Features

- Investigate customer support cases
- Store investigation history
- Search previous investigations
- Retrieve cases by ID
- View investigation statistics
""",
    version=settings.app_version,
    contact={
        "name": "Dallas Uzo",
    },
)

app.add_exception_handler(
    CaseNotFoundException,
    case_not_found_handler,
)

app.add_exception_handler(
    PersistenceDataException,
    persistence_data_handler,
)

app.include_router(
    support_router,
    prefix="/support",
    tags=["Support"],
)


@app.get(
    "/",
    summary="Root Endpoint",
    description="Returns a welcome message.",
)
def root():

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

    return {
        "status": "running",
        "service": settings.app_name,
        "environment": settings.environment,
        "version": settings.app_version,
    }
