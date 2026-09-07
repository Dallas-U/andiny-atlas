import pytest
from pydantic import ValidationError

from app.core.settings import Settings


def test_development_configuration_is_valid() -> None:
    """A valid development configuration is accepted."""

    settings = Settings(
        APP_NAME="Andiny Atlas",
        APP_VERSION="0.19.0",
        ENVIRONMENT="development",
        ATLAS_ENV="development",
        JWT_SECRET_KEY="development-secret",
        ALLOW_DEVELOPMENT_SEED=True,
    )

    assert settings.is_development is True


def test_production_configuration_requires_jwt_secret() -> None:
    """Production must reject an empty JWT secret."""

    with pytest.raises(ValidationError):
        Settings(
            APP_NAME="Andiny Atlas",
            APP_VERSION="0.19.0",
            ENVIRONMENT="production",
            ATLAS_ENV="development",
            JWT_SECRET_KEY="   ",
            ALLOW_DEVELOPMENT_SEED=False,
        )


def test_production_configuration_rejects_development_seed() -> None:
    """Production must not allow development seed data."""

    with pytest.raises(ValidationError):
        Settings(
            APP_NAME="Andiny Atlas",
            APP_VERSION="0.19.0",
            ENVIRONMENT="production",
            ATLAS_ENV="development",
            JWT_SECRET_KEY=(
                "production-secret-key-with-at-"
                "least-thirty-two-characters"
            ),
            ALLOW_DEVELOPMENT_SEED=True,
        )


def test_production_configuration_rejects_demo_environment() -> None:
    """Production must not run using the demo Atlas environment."""

    with pytest.raises(ValidationError):
        Settings(
            APP_NAME="Andiny Atlas",
            APP_VERSION="0.19.0",
            ENVIRONMENT="production",
            ATLAS_ENV="demo",
            JWT_SECRET_KEY=(
                "production-secret-key-with-at-"
                "least-thirty-two-characters"
            ),
            ALLOW_DEVELOPMENT_SEED=False,
        )


def test_invalid_environment_is_rejected() -> None:
    """Unsupported deployment environments are rejected."""

    with pytest.raises(ValidationError):
        Settings(
            APP_NAME="Andiny Atlas",
            APP_VERSION="0.19.0",
            ENVIRONMENT="invalid",
            ATLAS_ENV="development",
            JWT_SECRET_KEY="development-secret",
            ALLOW_DEVELOPMENT_SEED=False,
        )


def test_invalid_atlas_environment_is_rejected() -> None:
    """Unsupported Atlas runtime environments are rejected."""

    with pytest.raises(ValidationError):
        Settings(
            APP_NAME="Andiny Atlas",
            APP_VERSION="0.19.0",
            ENVIRONMENT="development",
            ATLAS_ENV="invalid",
            JWT_SECRET_KEY="development-secret",
            ALLOW_DEVELOPMENT_SEED=False,
        )