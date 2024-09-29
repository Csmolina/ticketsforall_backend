import os
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
import jwt
import datetime
from unittest.mock import patch

import pytest
from adapters.src.jwt import create_jwt_token, verify_jwt_token


def test_create_jwt_token():
    email = "test@example.com"
    name = "Test User"
    role = "user"
    picture = "http://example.com/picture.jpg"
    secret_key = "test_secret_key"
    date_now = datetime.datetime.now()
    with patch.dict(os.environ, {"SECRET_KEY": secret_key}):
        token = create_jwt_token(email, name, role, picture)
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        exp_date = datetime.datetime.fromtimestamp(decoded_token["exp"])
        assert decoded_token["email"] == email
        assert decoded_token["name"] == name
        assert decoded_token["role"] == role
        assert decoded_token["picture"] == picture
        assert "exp" in decoded_token
        assert isinstance(decoded_token["exp"], int)
        assert exp_date > date_now


def test_verify_jwt_token_valid():
    secret_key = "test_secret_key"
    email = "test@example.com"
    name = "Test User"
    role = "user"
    picture = "http://example.com/picture.jpg"
    expiration_time = datetime.datetime.now() + datetime.timedelta(hours=6)
    payload = {
        "email": email,
        "name": name,
        "role": role,
        "picture": picture,
        "exp": expiration_time,
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

    with patch.dict(os.environ, {"SECRET_KEY": secret_key}):
        result = verify_jwt_token(credentials)
        assert result["email"] == email
        assert result["name"] == name
        assert result["role"] == role
        assert result["picture"] == picture


def test_verify_jwt_token_expired():
    secret_key = "test_secret_key"
    email = "test@example.com"
    name = "Test User"
    role = "user"
    picture = "http://example.com/picture.jpg"
    expiration_time = datetime.datetime.now() - datetime.timedelta(hours=1)
    payload = {
        "email": email,
        "name": name,
        "role": role,
        "picture": picture,
        "exp": expiration_time,
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

    with patch.dict(os.environ, {"SECRET_KEY": secret_key}):
        with pytest.raises(HTTPException) as excinfo:
            verify_jwt_token(credentials)
        assert excinfo.value.status_code == 401
        assert excinfo.value.detail == "Token has expired"


def test_verify_jwt_token_invalid():
    secret_key = "test_secret_key"
    invalid_token = "invalid_token"
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer", credentials=invalid_token
    )

    with patch.dict(os.environ, {"SECRET_KEY": secret_key}):
        with pytest.raises(HTTPException) as excinfo:
            verify_jwt_token(credentials)
        assert excinfo.value.status_code == 403
        assert excinfo.value.detail == "Invalid token"
