from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EnterpriseUser:
    user_id: str
    name: str
    role: str
    department: str
    region: str | None = None
    specialization: str | None = None


EXECUTIVES: list[EnterpriseUser] = [
    EnterpriseUser(
        "exec-ceo",
        "Dallas Uzo",
        "Chief Executive Officer",
        "EXEC",
    ),
    EnterpriseUser(
        "exec-coo",
        "Amaka Okafor",
        "Chief Operations Officer",
        "OPS",
    ),
    EnterpriseUser(
        "exec-cco",
        "Tunde Adeyemi",
        "Chief Compliance Officer",
        "COMP",
    ),
    EnterpriseUser(
        "exec-cro",
        "Ifeoma Nwosu",
        "Chief Risk Officer",
        "RISK",
    ),
    EnterpriseUser(
        "exec-cto",
        "Chinedu Eze",
        "Chief Technology Officer",
        "TECH",
    ),
    EnterpriseUser(
        "exec-investigations",
        "Fatima Bello",
        "Director of Investigations",
        "FRAUD",
    ),
    EnterpriseUser(
        "exec-support",
        "Kunle Adebayo",
        "Head of Customer Support",
        "SUP",
    ),
    EnterpriseUser(
        "exec-office",
        "Zainab Ibrahim",
        "Head of Executive Office",
        "ADMIN",
    ),
]


MANAGERS: list[EnterpriseUser] = [
    EnterpriseUser(
        "mgr-ops",
        "Grace Johnson",
        "Operations Manager",
        "OPS",
    ),
    EnterpriseUser(
        "mgr-support",
        "Emeka Obi",
        "Support Operations Manager",
        "SUP",
    ),
    EnterpriseUser(
        "mgr-compliance",
        "Aisha Mohammed",
        "Compliance Manager",
        "COMP",
    ),
    EnterpriseUser(
        "mgr-fraud",
        "Victor Umeh",
        "Fraud Investigation Manager",
        "FRAUD",
    ),
    EnterpriseUser(
        "mgr-risk",
        "Ruth Ogunleye",
        "Risk Operations Manager",
        "RISK",
    ),
    EnterpriseUser(
        "mgr-tech",
        "David Okorie",
        "Technology Operations Manager",
        "TECH",
    ),
]


INVESTIGATORS: list[EnterpriseUser] = [
    EnterpriseUser(
        "inv-001",
        "Chioma Eze",
        "Senior Investigator",
        "FRAUD",
        specialization="Financial Fraud",
    ),
    EnterpriseUser(
        "inv-002",
        "Samuel Peters",
        "Senior Investigator",
        "FRAUD",
        specialization="Digital Payments",
    ),
    EnterpriseUser(
        "inv-003",
        "Halima Yusuf",
        "Senior Investigator",
        "COMP",
        specialization="Identity Verification",
    ),
    EnterpriseUser(
        "inv-004",
        "Kenneth Nnamdi",
        "Senior Investigator",
        "OPS",
        specialization="Transaction Anomalies",
    ),
    EnterpriseUser(
        "inv-005",
        "Oluchi Nwankwo",
        "Senior Investigator",
        "OPS",
        specialization="Merchant Disputes",
    ),
    EnterpriseUser(
        "inv-006",
        "Abdul Salisu",
        "Senior Investigator",
        "COMP",
        specialization="Regulatory Escalations",
    ),
    EnterpriseUser(
        "inv-007",
        "Blessing Edet",
        "Senior Investigator",
        "FRAUD",
        specialization="Account Compromise",
    ),
    EnterpriseUser(
        "inv-008",
        "Michael Afolabi",
        "Senior Investigator",
        "OPS",
        specialization="Operational Investigations",
    ),
]


AUDITORS: list[EnterpriseUser] = [
    EnterpriseUser(
        "audit-001",
        "Ngozi Ibe",
        "Senior Compliance Officer",
        "COMP",
    ),
    EnterpriseUser(
        "audit-002",
        "Yusuf Abdullahi",
        "AML Compliance Officer",
        "COMP",
    ),
    EnterpriseUser(
        "audit-003",
        "Patience Okon",
        "KYC Compliance Officer",
        "COMP",
    ),
    EnterpriseUser(
        "audit-004",
        "Henry Ojo",
        "Internal Auditor",
        "COMP",
    ),
    EnterpriseUser(
        "audit-005",
        "Esther Bassey",
        "Risk Auditor",
        "RISK",
    ),
    EnterpriseUser(
        "audit-006",
        "Oluwaseun Ajayi",
        "Governance Auditor",
        "COMP",
    ),
]


SUPERVISORS: list[EnterpriseUser] = [
    EnterpriseUser(
        "sup-001",
        "Joy Ekanem",
        "Support Supervisor",
        "SUP",
        region="Lagos",
    ),
    EnterpriseUser(
        "sup-002",
        "Paul Chukwu",
        "Support Supervisor",
        "SUP",
        region="Abuja",
    ),
    EnterpriseUser(
        "sup-003",
        "Mary Bello",
        "Support Supervisor",
        "SUP",
        region="South West",
    ),
    EnterpriseUser(
        "sup-004",
        "Isaac Danjuma",
        "Support Supervisor",
        "SUP",
        region="North Central",
    ),
]


SUPPORT_AGENTS: list[EnterpriseUser] = [
    EnterpriseUser(
        "agent-001",
        "Adeola Martins",
        "Senior Support Agent",
        "SUP",
    ),
    EnterpriseUser(
        "agent-002",
        "Chika Ugo",
        "Senior Support Agent",
        "SUP",
    ),
    EnterpriseUser(
        "agent-003",
        "Fatimah Aliyu",
        "Senior Support Agent",
        "SUP",
    ),
    EnterpriseUser(
        "agent-004",
        "Emmanuel Essien",
        "Senior Support Agent",
        "SUP",
    ),
    EnterpriseUser(
        "agent-005",
        "Ogechi Okafor",
        "Senior Support Agent",
        "SUP",
    ),
    EnterpriseUser(
        "agent-006",
        "Haruna Garba",
        "Senior Support Agent",
        "SUP",
    ),
    EnterpriseUser(
        "agent-007",
        "Janet Ndukwe",
        "Senior Support Agent",
        "SUP",
    ),
    EnterpriseUser(
        "agent-008",
        "Tope Akinola",
        "Senior Support Agent",
        "SUP",
    ),
]


ALL_USERS: list[EnterpriseUser] = (
    EXECUTIVES
    + MANAGERS
    + INVESTIGATORS
    + AUDITORS
    + SUPERVISORS
    + SUPPORT_AGENTS
)


def get_user(
    user_id: str,
) -> EnterpriseUser:
    for user in ALL_USERS:
        if user.user_id == user_id:
            return user

    raise KeyError(
        f"Unknown enterprise user: {user_id}"
    )