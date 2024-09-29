import datetime
import os

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt


def create_jwt_token(email: str, name: str, role: str, picture: str):
    secret_key = os.getenv("SECRET_KEY")
    expiration_time = datetime.datetime.now() + datetime.timedelta(hours=6)
    payload = {
        "email": email,
        "name": name,
        "role": role,
        "picture": picture,
        "exp": expiration_time,
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    ALGORITHM = "HS256"
    secret_key = os.getenv("SECRET_KEY")
    token = credentials.credentials
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")
