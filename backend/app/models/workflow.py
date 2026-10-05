from pydantic import BaseModel, Field


class WorkflowCheck(BaseModel):
    """A domain-neutral verification step in a workflow definition."""

    key: str = Field(min_length=1, max_length=100)
    label: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=500)
    required: bool = True


class WorkflowDefinition(BaseModel):
    """Configuration describing how an investigation is executed."""

    workflow_id: str = Field(min_length=1, max_length=150)
    name: str = Field(min_length=1, max_length=200)
    version: str = Field(default="1", min_length=1, max_length=50)
    checks: list[WorkflowCheck] = Field(default_factory=list)


class WorkflowCheckResult(BaseModel):
    """Result of executing one workflow check."""

    key: str
    passed: bool
    evidence: list[str] = Field(default_factory=list)


class WorkflowDecision(BaseModel):
    """Explainable decision produced from workflow execution."""

    outcome: str
    reason: str
    supporting_checks: list[str] = Field(default_factory=list)


class WorkflowOutcome(BaseModel):
    """Operational outcome and next action for an investigation."""

    status: str
    reason: str
    next_action: str


class WorkflowExecution(BaseModel):
    """Domain-neutral execution record used by the investigation engine."""

    workflow_id: str
    workflow_version: str
    checks: list[WorkflowCheckResult]
    decision: WorkflowDecision
    outcome: WorkflowOutcome
