from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class EnterpriseAnalyticsSummary:
    """
    Executive summary metrics for an enterprise scope
    (organization, branch, or department).
    """

    total_cases: int
    resolved_cases: int
    waiting_cases: int
    technical_investigation_cases: int
    escalated_cases: int
    resolution_rate: float
    escalation_rate: float


@dataclass(slots=True)
class BranchAnalyticsSummary:
    """
    Operational summary for a branch.
    """

    branch_id: str
    branch_name: str
    total_cases: int
    resolved_cases: int
    escalation_rate: float


@dataclass(slots=True)
class DepartmentAnalyticsSummary:
    """
    Operational summary for a department.
    """

    department_id: str
    department_name: str
    total_cases: int
    resolved_cases: int
    escalation_rate: float