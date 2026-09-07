from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.core.settings import Settings


def create_settings(
    **overrides,
) -> Settings:
    """
    Create isolated Settings instances for deployment
    configuration tests.

    Environment variables are supplied directly so tests
    do not depend on the local backend .env file.
    """

    values = {
        "APP_NAME": "Andiny Atlas",
        "APP_VERSION": "0.19.0",
        "ENVIRONMENT": "development",
        "ATLAS_ENV": "development",
        "LOG_LEVEL": "INFO",
        "JWT_SECRET_KEY": (
            "development-test-secret-key-"
            "with-sufficient-length"
        ),
        "JWT_ALGORITHM": "HS256",
        "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
        "JWT_ISSUER": "AndinyAtlas",
        "ALLOW_DEVELOPMENT_SEED": "false",
    }

    values.update(overrides)

    return Settings(**values)


def test_valid_development_configuration() -> None:
    """Development configuration is accepted."""

    settings = create_settings()

    assert settings.is_development is True
    assert settings.is_production is False


def test_valid_testing_configuration() -> None:
    """Testing configuration is accepted."""

    settings = create_settings(
        ENVIRONMENT="testing",
    )

    assert settings.is_testing is True


def test_valid_staging_configuration() -> None:
    """Staging configuration is accepted."""

    settings = create_settings(
        ENVIRONMENT="staging",
    )

    assert settings.is_staging is True


def test_valid_production_configuration() -> None:
    """Valid production configuration is accepted."""

    settings = create_settings(
        ENVIRONMENT="production",
        JWT_SECRET_KEY=(
            "production-secret-key-with-at-"
            "least-thirty-two-characters"
        ),
        ALLOW_DEVELOPMENT_SEED="false",
    )

    assert settings.is_production is True


def test_invalid_environment_is_rejected() -> None:
    """Unsupported deployment environments are rejected."""

    with pytest.raises(ValidationError):
        create_settings(
            ENVIRONMENT="invalid",
        )


def test_invalid_atlas_environment_is_rejected() -> None:
    """Unsupported Atlas runtime environments are rejected."""

    with pytest.raises(ValidationError):
        create_settings(
            ATLAS_ENV="production",
        )


def test_empty_jwt_secret_is_rejected() -> None:
    """An empty JWT secret must never be accepted."""

    with pytest.raises(ValidationError):
        create_settings(
            JWT_SECRET_KEY="",
        )


def test_zero_token_expiry_is_rejected() -> None:
    """Token expiry must be greater than zero."""

    with pytest.raises(ValidationError):
        create_settings(
            ACCESS_TOKEN_EXPIRE_MINUTES="0",
        )


def test_negative_token_expiry_is_rejected() -> None:
    """Negative token expiry must be rejected."""

    with pytest.raises(ValidationError):
        create_settings(
            ACCESS_TOKEN_EXPIRE_MINUTES="-30",
        )


def test_production_development_seed_is_rejected() -> None:
    """Development seed data cannot be enabled in production."""

    with pytest.raises(ValidationError):
        create_settings(
            ENVIRONMENT="production",
            ALLOW_DEVELOPMENT_SEED="true",
        )


def test_weak_production_jwt_secret_is_rejected() -> None:
    """Production requires a sufficiently strong JWT secret."""

    with pytest.raises(ValidationError):
        create_settings(
            ENVIRONMENT="production",
            JWT_SECRET_KEY="weak-secret",
        )


def test_demo_environment_uses_demo_database() -> None:
    """Demo mode uses the dedicated demo database."""

    settings = create_settings(
        ATLAS_ENV="demo",
    )

    assert settings.sqlite_database_name == (
        "atlas_demo.db"
    )


def test_development_environment_uses_default_database() -> None:
    """Development mode uses the standard Atlas database."""

    settings = create_settings(
        ATLAS_ENV="development",
    )

    assert settings.sqlite_database_name == (
        "andiny_atlas.db"
    )