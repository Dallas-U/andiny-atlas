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
