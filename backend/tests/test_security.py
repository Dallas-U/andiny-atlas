from app.core.security import (
    hash_password,
    verify_password,
)


def test_hash_password_creates_different_value():

    password = "MyPassword123"

    hashed = hash_password(password)

    assert hashed != password


def test_verify_password_accepts_correct_password():

    password = "MyPassword123"

    hashed = hash_password(password)

    assert verify_password(
        password,
        hashed,
    )


def test_verify_password_rejects_wrong_password():

    hashed = hash_password("MyPassword123")

    assert not verify_password(
        "WrongPassword",
        hashed,
    )

def test_verify_password_accepts_bcrypt_hash():
    from pwdlib.hashers.bcrypt import BcryptHasher

    password = "BcryptCompatibilityTest123!"
    hashed = BcryptHasher(rounds=12, prefix="2b").hash(password)

    assert verify_password(password, hashed)
    assert not verify_password("WrongPassword123!", hashed)


def test_verify_password_accepts_argon2id_hash():
    from pwdlib.hashers.argon2 import Argon2Hasher

    password = "Argon2CompatibilityTest123!"
    hashed = Argon2Hasher().hash(password)

    assert verify_password(password, hashed)
    assert not verify_password("WrongPassword123!", hashed)
