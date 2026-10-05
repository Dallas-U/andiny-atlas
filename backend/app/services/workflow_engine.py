from app.core.constants import InvestigationStatus
from app.logging.logger import logger
from app.models.case_response import InvestigationResult
from app.models.support_case import SupportCase
from app.models.workflow import (
    WorkflowDecision,
    WorkflowExecution,
    WorkflowOutcome,
    WorkflowDefinition,
    WorkflowCheckResult,
)
from app.services.legacy_workflow_adapter import LegacyWorkflowAdapter


class WorkflowEngine:
    """Execute organization-defined investigation workflows.

    The engine owns execution mechanics. Workflow definitions provide the
    meaning and order of the checks. No industry-specific business logic is
    permitted in this core path.
    """

    def investigate(
        self,
        case: SupportCase,
    ) -> InvestigationResult:
        execution = self.execute(case)
        return InvestigationResult(
            status=InvestigationStatus(execution.outcome.status),
            reason=execution.outcome.reason,
            next_action=execution.outcome.next_action,
        )

    def execute(self, case: SupportCase) -> WorkflowExecution:
        workflow, values = self._resolve_workflow(case)

        logger.info(
            "Workflow investigation started for customer '%s' using workflow '%s'.",
            case.customer_name,
            workflow.workflow_id,
        )

        results: list[WorkflowCheckResult] = []
        failed_required: list[str] = []

        for check in workflow.checks:
            passed = values.get(check.key, False)
            results.append(
                WorkflowCheckResult(
                    key=check.key,
                    passed=passed,
                    evidence=[f"check:{check.key}"],
                )
            )
            if check.required and not passed:
                failed_required.append(check.key)

        if failed_required:
            decision = WorkflowDecision(
                outcome="review_required",
                reason="One or more required investigation checks were not satisfied.",
                supporting_checks=failed_required,
            )
            outcome = WorkflowOutcome(
                status=InvestigationStatus.TECHNICAL_INVESTIGATION.value,
                reason=decision.reason,
                next_action="Review the relevant source evidence and complete the outstanding check.",
            )
        else:
            decision = WorkflowDecision(
                outcome="resolved",
                reason="All required investigation checks were satisfied.",
                supporting_checks=[result.key for result in results],
            )
            outcome = WorkflowOutcome(
                status=InvestigationStatus.RESOLVED.value,
                reason=decision.reason,
                next_action="No further action required.",
            )

        return WorkflowExecution(
            workflow_id=workflow.workflow_id,
            workflow_version=workflow.version,
            checks=results,
            decision=decision,
            outcome=outcome,
        )

    @staticmethod
    def _resolve_workflow(
        case: SupportCase,
    ) -> tuple[WorkflowDefinition, dict[str, bool]]:
        if case.workflow_definition is not None:
            return case.workflow_definition, case.checks

        if case.checks:
            workflow_id = case.workflow_definition_id or "inline-workflow"
            workflow = WorkflowDefinition(
                workflow_id=workflow_id,
                name="Inline investigation workflow",
                version="1",
                checks=[
                    {
                        "key": key,
                        "label": key.replace("_", " ").title(),
                        "description": f"Evaluate the configured check: {key}.",
                    }
                    for key in case.checks
                ],
            )
            return workflow, case.checks

        return LegacyWorkflowAdapter.to_workflow(case)
