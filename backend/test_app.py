from fastapi import FastAPI, APIRouter

app = FastAPI()

router = APIRouter()

@router.get("/hello")
def hello():
    return {"message": "Hello"}

app.include_router(router, prefix="/test")