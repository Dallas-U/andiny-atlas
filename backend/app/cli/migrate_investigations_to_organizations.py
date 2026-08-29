from sqlalchemy import select

from app.database.models import Investigation, Organization
from app.database.session import SessionLocal


ORGANIZATION_NAME_MAP = {
    "Airtel Nigeria": "Airtel Nigeria",
    "Sterling Bank": "Sterling Bank",
    "Lagos State Government": "Lagos State Government",
    "Zenith Insurance": "Zenith Insurance",
    "Atlantic Health Group": "Atlantic Health Group",
}


def migrate() -> None:
    with SessionLocal() as session:
        organizations = session.scalars(select(Organization)).all()

        organization_lookup = {
            organization.name: organization.organization_id
            for organization in organizations
        }

        investigations = session.scalars(select(Investigation)).all()

        updated = 0

        for investigation in investigations:
            for prefix, organization_name in ORGANIZATION_NAME_MAP.items():
                if investigation.customer_name.startswith(prefix):
                    investigation.organization_id = organization_lookup.get(
                        organization_name
                    )
                    updated += 1
                    break

        session.commit()

    print(
        f"Linked {updated} investigations to organizations."
    )


if __name__ == "__main__":
    migrate()