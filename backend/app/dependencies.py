from app.repositories.case_repository import CaseRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.case_manager import CaseManager
from app.services.workflow_engine import WorkflowEngine


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
