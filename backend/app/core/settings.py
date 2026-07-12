from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    app_name: str = Field(
        default="Andiny Atlas",
        alias="APP_NAME",
    )

    app_version: str = Field(
        default="0.18.0",
        alias="APP_VERSION",
    )

    environment: str = Field(
        default="development",
        alias="ENVIRONMENT",
    )

    log_level: str = Field(
        default="INFO",
        alias="LOG_LEVEL",
    )

    database_path: Path = Field(
        default=Path("data/investigations.json"),
        alias="DATABASE_PATH",
    )

    jwt_secret_key: str = Field(
        alias="JWT_SECRET_KEY",
    )

    jwt_algorithm: str = Field(
        default="HS256",
        alias="JWT_ALGORITHM",
    )

    access_token_expire_minutes: int = Field(
        default=30,
        alias="ACCESS_TOKEN_EXPIRE_MINUTES",
    )

    jwt_issuer: str = Field(
        default="AndinyAtlas",
        alias="JWT_ISSUER",
    )


settings = Settings()
