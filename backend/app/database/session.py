from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.settings import settings


DATA_DIRECTORY = Path("data")
DATA_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)


DATABASE_URL = (
    f"sqlite:///./data/{settings.sqlite_database_name}"
)


engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)


SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    expire_on_commit=False,
)