from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import (
    get_auth_service,
    get_current_user,
)
from app.domain import User
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


@router.post(
    "/token",
    response_model=Token,
    summary="OAuth2 Token",
    description="Authenticates using the OAuth2 password flow for Swagger UI.",
)
def login_for_access_token(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
    auth_service: AuthService = Depends(get_auth_service),
):
    request = UserLogin(
        email=form_data.username,
        password=form_data.password,
    )

    return auth_service.create_token(request)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Current User",
    description="Returns the authenticated user.",
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user