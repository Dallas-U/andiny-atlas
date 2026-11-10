from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher


# Keep bcrypt hash creation compatible with the existing cost and prefix.
password_hasher = BcryptHasher(rounds=12, prefix="2b")

# Verification supports both legacy bcrypt and Argon2id hashes.
# This phase does not enable automatic hash upgrades.
password_verifier = PasswordHash(
    (
        Argon2Hasher(),
        BcryptHasher(),
    ),
)


def hash_password(password: str) -> str:
    """Return a bcrypt hash using the established cost and prefix."""

    return password_hasher.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """Verify a password against a supported stored hash."""

    return password_verifier.verify(
        plain_password,
        hashed_password,
    )
