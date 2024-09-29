from fastapi import HTTPException, Depends, status

from adapters.src.jwt import verify_jwt_token


def verify_admin_user(payload: dict = Depends(verify_jwt_token)):
    if payload["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this resource",
        )
    return payload
