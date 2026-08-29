from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from random import Random

from app.data.demo_users import (
    INVESTIGATORS,
    SUPPORT_AGENTS,
)

_rng = Random(42)


@dataclass(frozen=True)
class DemoInvestigation:
    case_id: str
    timestamp: str
    customer_name: str
    phone_number: str
    created_by: str
    investigator: str
    category: str
    department: str
    status: str
    reason: str
    next_action: str


CUSTOMER_FIRST_NAMES = [
    "Amina",
    "Chinedu",
    "Grace",
    "Ibrahim",
    "Joy",
    "Kelechi",
    "Musa",
    "Ngozi",
    "Samuel",
    "Tolu",
]

CUSTOMER_LAST_NAMES = [
    "Adeyemi",
    "Bello",
    "Eze",
    "Ibrahim",
    "Johnson",
    "Nwosu",
    "Okafor",
    "Okon",
    "Olawale",
    "Yusuf",
]

CATEGORIES = [
    (
        "Payment Dispute",
        "OPS",
        "Resolved",
        "Transaction reversal completed",
        "Notify customer of successful reversal",
    ),
    (
        "Account Access",
        "SUP",
        "Waiting",
        "Customer verification pending",
        "Await identity confirmation",
    ),
    (
        "Fraud Investigation",
        "FRAUD",
        "Escalated",
        "Suspicious transaction pattern detected",
        "Escalate to fraud operations manager",
    ),
    (
        "Identity Verification",
        "COMP",
        "Technical Investigation",
        "KYC validation requires manual review",
        "Perform enhanced verification checks",
    ),
    (
        "Merchant Dispute",
        "OPS",
        "Resolved",
        "Merchant reconciliation completed",
        "Close merchant dispute case",
    ),
    (
        "Regulatory Review",
        "COMP",
        "Escalated",
        "Compliance exception requires approval",
        "Route to compliance leadership",
    ),
]


def _customer_name(index: int) -> str:
    first = CUSTOMER_FIRST_NAMES[
        index % len(CUSTOMER_FIRST_NAMES)
    ]
    last = CUSTOMER_LAST_NAMES[
        (index * 3)
        % len(CUSTOMER_LAST_NAMES)
    ]
    return f"{first} {last}"


def _phone(index: int) -> str:
    return f"0802{index:07d}"


def generate_demo_investigations(
    count: int = 100,
) -> list[DemoInvestigation]:
    base_date = datetime.now(
        timezone.utc,
    ) - timedelta(days=90)

    investigations: list[DemoInvestigation] = []

    investigators = [
        investigator.name
        for investigator in INVESTIGATORS
    ]

    support_agents = [
        agent.name
        for agent in SUPPORT_AGENTS
    ]

    for index in range(count):
        category = CATEGORIES[
            index % len(CATEGORIES)
        ]

        created_at = (
            base_date
            + timedelta(
                days=index % 90,
                hours=index % 8,
                minutes=index % 60,
            )
        )

        investigations.append(
            DemoInvestigation(
                case_id=f"AFS-{created_at.year}-{index + 1:04d}",
                timestamp=created_at.isoformat(),
                customer_name=_customer_name(index),
                phone_number=_phone(index),
                created_by=support_agents[
                    index % len(support_agents)
                ],
                investigator=investigators[
                    index % len(investigators)
                ],
                category=category[0],
                department=category[1],
                status=category[2],
                reason=category[3],
                next_action=category[4],
            )
        )

    return investigations


DEMO_INVESTIGATIONS = (
    generate_demo_investigations()
)