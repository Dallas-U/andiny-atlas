from app.core.constants import InvestigationStatus
from app.logging.logger import logger
from app.models.case_response import InvestigationResult
from app.models.support_case import SupportCase


class WorkflowEngine:

    def investigate(
        self,
        case: SupportCase,
    ) -> InvestigationResult:

        logger.info(
            "Workflow investigation started for customer '%s'.",
            case.customer_name,
        )

        if not case.payment_verified:

            logger.info("Payment verification failed.")

            return InvestigationResult(
                status=InvestigationStatus.RESOLVED,
                reason="Payment has not been verified.",
                next_action="Ask customer to verify payment.",
            )

        logger.info("Payment verification passed.")

        if not case.extension_triggered:

            logger.info("Extension trigger not found.")

            return InvestigationResult(
                status=InvestigationStatus.TECHNICAL_INVESTIGATION,
                reason="No extension trigger found.",
                next_action="Investigate Intelligra trigger.",
            )

        logger.info("Extension trigger verified.")

        if not case.api_success:

            logger.info("API execution failed.")

            return InvestigationResult(
                status=InvestigationStatus.TECHNICAL_INVESTIGATION,
                reason="API execution failed.",
                next_action="Review API logs.",
            )

        logger.info("API execution successful.")

        if not case.skg_success:

            logger.info("Samsung Knox acknowledgement failed.")

            return InvestigationResult(
                status=InvestigationStatus.TECHNICAL_INVESTIGATION,
                reason="Samsung Knox did not acknowledge request.",
                next_action="Retry through SKG portal.",
            )

        logger.info("Samsung Knox acknowledged the request.")

        if not case.device_online:

            logger.info("Device is offline.")

            return InvestigationResult(
                status=InvestigationStatus.WAITING,
                reason="Device has not connected.",
                next_action="Ask customer to enable mobile data.",
            )

        logger.info("Device is online.")

        if not case.sim_slot_one:

            logger.info("SIM card is not in Slot 1.")

            return InvestigationResult(
                status=InvestigationStatus.WAITING,
                reason="SIM is not in Slot 1.",
                next_action="Move SIM to Slot 1.",
            )

        logger.info("SIM card detected in Slot 1.")

        if not case.mobile_data_on:

            logger.info("Mobile data is OFF.")

            return InvestigationResult(
                status=InvestigationStatus.WAITING,
                reason="Mobile Data is OFF.",
                next_action="Enable Mobile Data.",
            )

        logger.info("Mobile data is ON.")
        logger.info("Workflow investigation completed successfully.")

        return InvestigationResult(
            status=InvestigationStatus.RESOLVED,
            reason="Device should unlock successfully.",
            next_action="No further action required.",
        )
