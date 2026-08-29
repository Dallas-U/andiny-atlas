from __future__ import annotations

from datetime import datetime, timedelta
from uuid import uuid4

from app.core.constants import InvestigationStatus
from app.domain import Case, Customer, InvestigationResult
from app.repositories.case_repository import CaseRepository


def seed_demo_environment() -> None:
    repository = CaseRepository()

    existing_cases = repository.get_all_cases()

    if existing_cases:
        print(
            f"Demo seed skipped: {len(existing_cases)} existing cases found."
        )
        return

    organizations = [
        "Sterling Bank",
        "Airtel Nigeria",
        "Lagos State Government",
        "Zenith Insurance",
        "Atlantic Health Group",
    ]

    departments = [
        "Fraud Operations",
        "Customer Experience",
        "Enterprise Risk",
        "Compliance",
        "Digital Banking",
    ]

    statuses = [
        InvestigationStatus.RESOLVED,
        InvestigationStatus.WAITING,
        InvestigationStatus.TECHNICAL_INVESTIGATION,
        InvestigationStatus.ESCALATED,
    ]

    base_time = datetime.utcnow() - timedelta(days=60)

    for index in range(100):
        organization = organizations[index % len(organizations)]
        department = departments[index % len(departments)]
        status = statuses[index % len(statuses)]

        customer = Customer(
            name=f"{organization} Customer {index + 1}",
            phone_number=f"080{70000000 + index:08d}",
        )

        result = InvestigationResult(
            status=status,
            reason=f"{department} investigation review completed.",
            next_action="Executive review pending"
            if status is InvestigationStatus.ESCALATED
            else "No further action required",
        )

        case = Case(
            case_id=str(uuid4()),
            timestamp=base_time + timedelta(hours=index * 6),
            customer=customer,
            created_by=department,
            result=result,
        )

        repository.create_case(case)

    print("Seeded 100 demonstration investigations.")


if __name__ == "__main__":
    seed_demo_environment()