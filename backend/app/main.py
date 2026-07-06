from fastapi import FastAPI

from app.api.support import router as support_router

app = FastAPI(
    title="Andiny Atlas",
    description="""
Andiny Atlas is an AI-powered investigation engine for support agents.

## Features

- Investigate customer support cases
- Store investigation history
- Search previous investigations
- Retrieve cases by ID
- View investigation statistics
""",
    version="0.6.0",
    contact={
        "name": "Dallas Uzo",
    },
)

app.include_router(support_router, prefix="/support", tags=["Support"])


@app.get("/", summary="Root Endpoint", description="Returns a welcome message.")
def root():

    return {"message": "Welcome to Andiny Atlas"}


@app.get(
    "/health",
    summary="Health Check",
    description="Returns the current application status.",
)
def health():

    return {"status": "running", "service": "Atlas Core"}
