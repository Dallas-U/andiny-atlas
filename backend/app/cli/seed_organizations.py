from datetime import UTC, datetime
from uuid import uuid4

from app.domain.organization import Organization
from app.repositories.organization_repository import OrganizationRepository


def seed_organizations() -> None:
    repository = OrganizationRepository()

    if repository.list_all():
        print("Organization seed skipped: organizations already exist.")
        return

    organizations = [
        Organization(
            organization_id=str(uuid4()),
            name="Airtel Nigeria",
            code="AIRTEL",
            industry="Telecommunications",
            contact_email="admin@airtel.demo",
            is_active=True,
            created_at=datetime.now(UTC),
        ),
        Organization(
            organization_id=str(uuid4()),
            name="Sterling Bank",
            code="STERLING",
            industry="Banking",
            contact_email="admin@sterling.demo",
            is_active=True,
            created_at=datetime.now(UTC),
        ),
        Organization(
            organization_id=str(uuid4()),
            name="Lagos State Government",
            code="LASG",
            industry="Government",
            contact_email="admin@lasg.demo",
            is_active=True,
            created_at=datetime.now(UTC),
        ),
        Organization(
            organization_id=str(uuid4()),
            name="Zenith Insurance",
            code="ZENITH",
            industry="Insurance",
            contact_email="admin@zenith.demo",
            is_active=True,
            created_at=datetime.now(UTC),
        ),
        Organization(
            organization_id=str(uuid4()),
            name="Atlantic Health Group",
            code="ATLANTIC",
            industry="Healthcare",
            contact_email="admin@atlantic.demo",
            is_active=True,
            created_at=datetime.now(UTC),
        ),
    ]

    for organization in organizations:
        repository.create(organization)

    print(f"Seeded {len(organizations)} organizations.")


if __name__ == "__main__":
    seed_organizations()