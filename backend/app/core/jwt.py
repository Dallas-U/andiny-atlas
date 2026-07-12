from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt

from app.core.settings import settings


def create_access_token(
    subject: str,
) -> str:
    """Create a signed JWT access token."""

    issued_at = datetime.now(UTC)
    expires_at = issued_at + timedelta(
        minutes=settings.access_token_expire_minutes,
    )

    payload = {
        "sub": subject,
        "iat": issued_at,
        "exp": expires_at,
        "iss": settings.jwt_issuer,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(
    token: str,
) -> dict:
    """Decode and validate a JWT access token."""

    try:
        return jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
            issuer=settings.jwt_issuer,
        )

    except JWTError as exc:
        raise ValueError("Invalid or expired access token.") from exc
