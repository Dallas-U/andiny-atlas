from app.core.constants import InvestigationStatus
from app.models.support_case import SupportCase
from app.models.workflow import WorkflowCheck, WorkflowDefinition
from app.services.workflow_engine import WorkflowEngine


def build_case(**overrides) -> SupportCase:
    payload = {
        "customer_name": "Neutral Test Subject",
        "phone_number": "08000000000",
        "country": "Nigeria",
        "organization_id": "org-a",
    }
    payload.update(overrides)
    return SupportCase(**payload)


def test_generic_workflow_executes_without_telecom_fields():
    case = build_case(
        workflow_definition=WorkflowDefinition(
            workflow_id="claims-exception-v1",
            name="Claims Exception",
            version="1",
            checks=[
                WorkflowCheck(
                    key="claim_identified",
                    label="Claim identified",
                    description="Confirm the claim record is identified.",
                ),
                WorkflowCheck(
                    key="policy_validated",
                    label="Policy validated",
                    description="Confirm the policy is valid.",
                ),
            ],
        ),
        checks={
            "claim_identified": True,
            "policy_validated": True,
        },
    )

    execution = WorkflowEngine().execute(case)

    assert execution.workflow_id == "claims-exception-v1"
    assert execution.outcome.status == InvestigationStatus.RESOLVED.value
    assert [item.key for item in execution.checks] == [
        "claim_identified",
        "policy_validated",
    ]
    assert all(item.passed for item in execution.checks)


def test_generic_workflow_failed_check_is_explainable():
    case = build_case(
        workflow_definition=WorkflowDefinition(
            workflow_id="delivery-exception-v1",
            name="Delivery Exception",
            version="1",
            checks=[
                WorkflowCheck(
                    key="shipment_identified",
                    label="Shipment identified",
                    description="Confirm shipment identity.",
                ),
                WorkflowCheck(
                    key="delivery_status_verified",
                    label="Delivery status verified",
                    description="Confirm the current delivery status.",
                ),
            ],
        ),
        checks={
            "shipment_identified": True,
            "delivery_status_verified": False,
        },
    )

    execution = WorkflowEngine().execute(case)

    assert execution.outcome.status == InvestigationStatus.TECHNICAL_INVESTIGATION.value
    assert execution.decision.outcome == "review_required"
    assert execution.decision.supporting_checks == [
        "delivery_status_verified",
    ]


def test_generic_inline_checks_work_without_a_named_workflow_definition():
    case = build_case(
        workflow_definition_id="payments-exception-v1",
        checks={
            "transaction_verified": True,
            "merchant_account_valid": True,
        },
    )

    execution = WorkflowEngine().execute(case)

    assert execution.workflow_id == "payments-exception-v1"
    assert execution.outcome.status == InvestigationStatus.RESOLVED.value


def test_legacy_input_isolated_to_compatibility_boundary():
    case = build_case(
        payment_verified=True,
        extension_triggered=True,
        api_success=True,
        skg_success=True,
        device_online=True,
        sim_slot_one=True,
        mobile_data_on=True,
    )

    execution = WorkflowEngine().execute(case)

    assert execution.workflow_id == "legacy-compatibility"
    assert execution.outcome.status == InvestigationStatus.RESOLVED.value
    assert all(item.passed for item in execution.checks)
