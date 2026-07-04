class WorkflowEngine:

    def investigate(self, case):

        if not case.payment_verified:
            return {
                "status": "Resolved",
                "reason": "Payment has not been verified.",
                "next_action": "Ask customer to verify payment."
            }

        if not case.extension_triggered:
            return {
                "status": "Technical Investigation",
                "reason": "No extension trigger found.",
                "next_action": "Investigate Intelligra trigger."
            }

        if not case.api_success:
            return {
                "status": "Technical Investigation",
                "reason": "API execution failed.",
                "next_action": "Review API logs."
            }

        if not case.skg_success:
            return {
                "status": "Technical Investigation",
                "reason": "Samsung Knox did not acknowledge request.",
                "next_action": "Retry through SKG portal."
            }

        if not case.device_online:
            return {
                "status": "Waiting",
                "reason": "Device has not connected.",
                "next_action": "Ask customer to enable mobile data."
            }

        if not case.sim_slot_one:
            return {
                "status": "Waiting",
                "reason": "SIM is not in Slot 1.",
                "next_action": "Move SIM to Slot 1."
            }

        if not case.mobile_data_on:
            return {
                "status": "Waiting",
                "reason": "Mobile Data is OFF.",
                "next_action": "Enable Mobile Data."
            }

        return {
            "status": "Resolved",
            "reason": "Device should unlock successfully.",
            "next_action": "No further action required."
        }