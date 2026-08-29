from app.database.session import SessionLocal
from sqlalchemy import text

session = SessionLocal()
try:
    tables = session.execute(
        text("SELECT name FROM sqlite_master WHERE type='table'")
    ).all()
    print(tables)
finally:
    session.close()
