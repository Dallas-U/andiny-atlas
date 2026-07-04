from fastapi import FastAPI

from app.api.support import router as support_router

app = FastAPI(
    title="Andiny Atlas",
    version="0.2.0"
)

app.include_router(
    support_router,
    prefix="/support",
    tags=["Support"]
)


@app.get("/")
def root():

    return {
        "message":
        "Welcome to Andiny Atlas"
    }


@app.get("/health")
def health():

    return {
        "status":
        "running",

        "service":
        "Atlas Core"
    }