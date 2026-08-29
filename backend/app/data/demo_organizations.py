from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Department:
    code: str
    name: str
    executive_owner: str


@dataclass(frozen=True)
class Organization:
    code: str
    name: str
    industry: str
    headquarters: str
    employee_count: int
    branch_count: int


ANDINY_FINANCIAL_SERVICES = Organization(
    code="AFS",
    name="Andiny Financial Services",
    industry="Financial Services / Digital Banking",
    headquarters="Lagos, Nigeria",
    employee_count=1250,
    branch_count=12,
)


DEPARTMENTS: list[Department] = [
    Department(
        code="EXEC",
        name="Executive Office",
        executive_owner="Dallas Uzo",
    ),
    Department(
        code="OPS",
        name="Operations",
        executive_owner="Amaka Okafor",
    ),
    Department(
        code="COMP",
        name="Compliance",
        executive_owner="Tunde Adeyemi",
    ),
    Department(
        code="RISK",
        name="Risk Management",
        executive_owner="Ifeoma Nwosu",
    ),
    Department(
        code="TECH",
        name="Technology",
        executive_owner="Chinedu Eze",
    ),
    Department(
        code="FRAUD",
        name="Fraud Investigation",
        executive_owner="Fatima Bello",
    ),
    Department(
        code="SUP",
        name="Customer Support",
        executive_owner="Kunle Adebayo",
    ),
    Department(
        code="ADMIN",
        name="Executive Administration",
        executive_owner="Zainab Ibrahim",
    ),
]


def get_department(
    code: str,
) -> Department:
    for department in DEPARTMENTS:
        if department.code == code:
            return department

    raise KeyError(
        f"Unknown department: {code}"
    )