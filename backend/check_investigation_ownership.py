from sqlalchemy import text

from app.database.session import SessionLocal


CASE_ID = "d565dd4a-a5d1-4d5a-9cc8-a58ef042da5f"


session = SessionLocal()

try:
    result = session.execute(
        text(
            """
            SELECT
                case_id,
                organization_id,
                branch_id,
                department_id
            FROM investigations
            WHERE case_id = :case_id
            """
        ),
        {"case_id": CASE_ID},
    )

    print(result.all())

finally:
    session.close()