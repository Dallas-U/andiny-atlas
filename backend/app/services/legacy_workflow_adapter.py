from app.models.support_case import SupportCase
from app.models.workflow import WorkflowCheck, WorkflowDefinition


class LegacyWorkflowAdapter:
    """Translate the pre-refactor boolean investigation shape into generic checks.

    This is a temporary compatibility boundary. The generic WorkflowEngine must
    never depend on the legacy field names directly.
    """

    _CHECKS = (
        ("payment_verified", "Required record verification", "Confirm the relevant record is verified."),
        ("extension_triggered", "Exception trigger", "Confirm the configured exception trigger occurred."),
        ("api_success", "Relevant service response", "Confirm the relevant service response completed successfully."),
        ("skg_success", "Required verification step", "Confirm the required verification step completed."),
        ("device_online", "Operational channel availability", "Confirm the relevant operational channel is available."),
        ("sim_slot_one", "Account or case identity", "Confirm the correct account or case identity is established."),
        ("mobile_data_on", "Required service condition", "Confirm the required service condition is satisfied."),
    )

    @classmethod
    def to_workflow(cls, case: SupportCase) -> tuple[WorkflowDefinition, dict[str, bool]]:
        checks = [
            WorkflowCheck(
                key=key,
                label=label,
                description=description,
            )
            for key, label, description in cls._CHECKS
        ]

        values = {
            key: bool(getattr(case, key))
            for key, _, _ in cls._CHECKS
        }

        return (
            WorkflowDefinition(
                workflow_id="legacy-compatibility",
                name="Legacy investigation compatibility workflow",
                version="1",
                checks=checks,
            ),
            values,
        )
