from app.repositories.case_repository import CaseRepository
from app.services.case_manager import CaseManager
from app.services.workflow_engine import WorkflowEngine


class ServiceContainer:
    """Creates and owns application services."""

    def __init__(self):

        self.case_repository = CaseRepository()

        self.workflow_engine = WorkflowEngine()

        self.case_manager = CaseManager(
            repository=self.case_repository,
        )


container = ServiceContainer()
