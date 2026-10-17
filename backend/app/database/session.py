from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker

from app.core.settings import settings


DATABASE_URL = settings.resolved_database_url
database_url = make_url(DATABASE_URL)

connect_args = {}

if database_url.get_backend_name() == "sqlite":
    DATA_DIRECTORY = Path("data")
    DATA_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )
    connect_args = {
        "check_same_thread": False,
    }


engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
)


SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    expire_on_commit=False,
)
