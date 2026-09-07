from pathlib import Path

from pydantic import (
    Field,
    SecretStr,
    field_validator,
    model_validator,
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


BASE_DIR = Path(__file__).resolve().parents[2]

ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    """Application configuration and deployment safety settings."""

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(
        default="Andiny Atlas",
        alias="APP_NAME",
    )

    app_version: str = Field(
        default="0.19.0",
        alias="APP_VERSION",
    )

    environment: str = Field(
        default="development",
        alias="ENVIRONMENT",
    )

    atlas_environment: str = Field(
        default="development",
        alias="ATLAS_ENV",
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

    @field_validator("environment")
    @classmethod
    def validate_environment(
        cls,
        value: str,
    ) -> str:
        """Validate the application deployment environment."""

        normalized_value = value.strip().lower()

        allowed_environments = {
            "development",
            "testing",
            "staging",
            "production",
        }

        if normalized_value not in allowed_environments:
            raise ValueError(
                "Invalid ENVIRONMENT. Allowed values are: "
                "development, testing, staging, production."
            )

        return normalized_value

    @field_validator("atlas_environment")
    @classmethod
    def validate_atlas_environment(
        cls,
        value: str,
    ) -> str:
        """Validate the Andiny Atlas runtime environment."""

        normalized_value = value.strip().lower()

        allowed_environments = {
            "development",
            "demo",
            "test",
        }

        if normalized_value not in allowed_environments:
            raise ValueError(
                "Invalid ATLAS_ENV. Allowed values are: "
                "development, demo, test."
            )

        return normalized_value

    @field_validator("jwt_secret_key")
    @classmethod
    def validate_jwt_secret_key(
        cls,
        value: str,
    ) -> str:
        """Ensure that the JWT secret is never empty."""

        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError(
                "JWT_SECRET_KEY must not be empty."
            )

        return normalized_value

    @field_validator("access_token_expire_minutes")
    @classmethod
    def validate_access_token_expiry(
        cls,
        value: int,
    ) -> int:
        """Ensure that access tokens have a positive lifetime."""

        if value <= 0:
            raise ValueError(
                "ACCESS_TOKEN_EXPIRE_MINUTES must be "
                "greater than zero."
            )

        return value

    @model_validator(mode="after")
    def validate_production_configuration(
        self,
    ) -> "Settings":
        """
        Apply deployment-level safety checks.

        Production environments must not permit
        development-only or demo behavior.
        """

        if self.environment == "production":

            if self.atlas_environment == "demo":
                raise ValueError(
                    "ATLAS_ENV cannot be set to demo "
                    "in production."
                )

            if self.allow_development_seed:
                raise ValueError(
                    "ALLOW_DEVELOPMENT_SEED must be disabled "
                    "in production."
                )

            if len(self.jwt_secret_key) < 32:
                raise ValueError(
                    "JWT_SECRET_KEY must contain at least "
                    "32 characters in production."
                )

        return self

    @property
    def is_development(self) -> bool:
        """Return whether the application is in development mode."""

        return self.environment == "development"

    @property
    def is_testing(self) -> bool:
        """Return whether the application is in testing mode."""

        return self.environment == "testing"

    @property
    def is_staging(self) -> bool:
        """Return whether the application is in staging mode."""

        return self.environment == "staging"

    @property
    def is_production(self) -> bool:
        """Return whether the application is in production mode."""

        return self.environment == "production"

    @property
    def sqlite_database_name(self) -> str:
        """Return the database name for the active runtime."""

        if self.atlas_environment == "demo":
            return "atlas_demo.db"

        if self.atlas_environment == "test":
            return "atlas_test.db"

        return "andiny_atlas.db"


settings = Settings()