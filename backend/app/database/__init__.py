from app.database.database import Base
from app.database.models import Investigation
from app.database.session import engine


def initialize_database() -> None:
    """Create all database tables."""

    Base.metadata.create_all(bind=engine)
