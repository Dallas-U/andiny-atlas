from app.models.case_response import InvestigationResult
from app.models.support_case import SupportCase


class WorkflowEngine:

    def investigate(
        self,
        case: SupportCase,
    ) -> InvestigationResult:

        if not case.payment_verified:
            return InvestigationResult(
                status="Resolved",
                reason="Payment has not been verified.",
                next_action="Ask customer to verify payment.",
            )

        if not case.extension_triggered:
            return InvestigationResult(
                status="Technical Investigation",
                reason="No extension trigger found.",
                next_action="Investigate Intelligra trigger.",
            )

        if not case.api_success:
            return InvestigationResult(
                status="Technical Investigation",
                reason="API execution failed.",
                next_action="Review API logs.",
            )

        if not case.skg_success:
            return InvestigationResult(
                status="Technical Investigation",
                reason="Samsung Knox did not acknowledge request.",
                next_action="Retry through SKG portal.",
            )

        if not case.device_online:
            return InvestigationResult(
                status="Waiting",
                reason="Device has not connected.",
                next_action="Ask customer to enable mobile data.",
            )

        if not case.sim_slot_one:
            return InvestigationResult(
                status="Waiting",
                reason="SIM is not in Slot 1.",
                next_action="Move SIM to Slot 1.",
            )

        if not case.mobile_data_on:
            return InvestigationResult(
                status="Waiting",
                reason="Mobile Data is OFF.",
                next_action="Enable Mobile Data.",
            )

        return InvestigationResult(
            status="Resolved",
            reason="Device should unlock successfully.",
            next_action="No further action required.",
        )
