from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(default="Andiny Atlas", alias="APP_NAME")
    app_version: str = Field(default="0.18.0", alias="APP_VERSION")

    environment: str = Field(
        default="development",
        alias="ENVIRONMENT",
    )

    atlas_environment: str = Field(
        default="development",
        alias="ATLAS_ENV",
    )

    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    database_path: Path = Field(
        default=Path("data/investigations.json"),
        alias="DATABASE_PATH",
    )

    jwt_secret_key: str = Field(alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=30,
        alias="ACCESS_TOKEN_EXPIRE_MINUTES",
    )
    jwt_issuer: str = Field(default="AndinyAtlas", alias="JWT_ISSUER")

    allow_development_seed: bool = Field(
        default=False,
        alias="ALLOW_DEVELOPMENT_SEED",
    )

    seed_super_admin_name: str = Field(
        default="Development Super Administrator",
        alias="SEED_SUPER_ADMIN_NAME",
    )
    seed_super_admin_email: str = Field(
        default="superadmin@andiny.local",
        alias="SEED_SUPER_ADMIN_EMAIL",
    )
    seed_super_admin_password: SecretStr | None = Field(
        default=None,
        alias="SEED_SUPER_ADMIN_PASSWORD",
    )

    seed_admin_name: str = Field(
        default="Development Administrator",
        alias="SEED_ADMIN_NAME",
    )
    seed_admin_email: str = Field(
        default="admin@andiny.local",
        alias="SEED_ADMIN_EMAIL",
    )
    seed_admin_password: SecretStr | None = Field(
        default=None,
        alias="SEED_ADMIN_PASSWORD",
    )

    seed_supervisor_name: str = Field(
        default="Development Supervisor",
        alias="SEED_SUPERVISOR_NAME",
    )
    seed_supervisor_email: str = Field(
        default="supervisor@andiny.local",
        alias="SEED_SUPERVISOR_EMAIL",
    )
    seed_supervisor_password: SecretStr | None = Field(
        default=None,
        alias="SEED_SUPERVISOR_PASSWORD",
    )

    seed_agent_name: str = Field(
        default="Development Agent",
        alias="SEED_AGENT_NAME",
    )
    seed_agent_email: str = Field(
        default="agent@andiny.local",
        alias="SEED_AGENT_EMAIL",
    )
    seed_agent_password: SecretStr | None = Field(
        default=None,
        alias="SEED_AGENT_PASSWORD",
    )

    @property
    def sqlite_database_name(self) -> str:
        if self.atlas_environment.lower() == "demo":
            return "atlas_demo.db"
        return "andiny_atlas.db"


settings = Settings()