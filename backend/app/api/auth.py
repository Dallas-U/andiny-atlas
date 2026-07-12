from fastapi import APIRouter, Depends, status

from app.dependencies import get_auth_service
from app.models.user import (
    Token,
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.services.auth_service import AuthService

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register User",
    description="Creates a new Andiny Atlas user account.",
)
def register_user(
    request: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
):

    return auth_service.register_user(request)


@router.post(
    "/login",
    response_model=Token,
    summary="Authenticate User",
    description="Authenticates a user and returns a JWT access token.",
)
def login(
    request: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
):

    return auth_service.create_token(request)
