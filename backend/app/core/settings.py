import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    """Application configuration."""

    app_name: str = os.getenv("APP_NAME", "Andiny Atlas")

    app_version: str = os.getenv("APP_VERSION", "0.12.0")

    environment: str = os.getenv("ENVIRONMENT", "development")

    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    database_path: Path = Path(
        os.getenv(
            "DATABASE_PATH",
            "data/investigations.json",
        )
    )


settings = Settings()
