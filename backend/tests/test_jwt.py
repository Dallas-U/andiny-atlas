import pytest

from app.core.jwt import (
    create_access_token,
    decode_access_token,
)


def test_create_and_decode_access_token():

    token = create_access_token("user-001")

    payload = decode_access_token(token)

    assert payload["sub"] == "user-001"
    assert payload["iss"] == "AndinyAtlas"
    assert "iat" in payload
    assert "exp" in payload


def test_decode_access_token_rejects_invalid_token():

    with pytest.raises(
        ValueError,
        match="Invalid or expired access token.",
    ):
        decode_access_token("invalid-token")
