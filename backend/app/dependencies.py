from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.jwt import decode_access_token
from app.database.models import User
from app.exceptions.exceptions import (
    InactiveUserException,
    InvalidTokenException,
)
from app.repositories.case_repository import CaseRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.case_manager import CaseManager
from app.services.workflow_engine import WorkflowEngine

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login",
    auto_error=False,
)


def get_workflow_engine() -> WorkflowEngine:
    return WorkflowEngine()


def get_case_repository() -> CaseRepository:
    return CaseRepository()


def get_case_manager() -> CaseManager:
    repository = get_case_repository()
    return CaseManager(repository)


def get_user_repository() -> UserRepository:
    return UserRepository()


def get_auth_service() -> AuthService:
    repository = get_user_repository()
    return AuthService(repository)


def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    """Resolve the authenticated user from a bearer token."""

    if token is None:
        raise InvalidTokenException()

    try:
        payload = decode_access_token(token)

    except ValueError as exc:
        raise InvalidTokenException() from exc

    user_id = payload.get("sub")

    if not isinstance(user_id, str) or not user_id:
        raise InvalidTokenException()

    user = auth_service.get_user_by_id(user_id)

    if user is None:
        raise InvalidTokenException()

    if not user.is_active:
        raise InactiveUserException()

    return user
