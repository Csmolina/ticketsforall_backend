import os
from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse

from adapters.src.oauth import oauth, get_user_info_from_google
from core.src.use_cases.user.create.request import CreateUserRequest
from adapters.src.jwt import create_jwt_token
from factories.use_cases.user import get_or_create_user_use_case


google_auth_router = APIRouter(prefix="/google", tags=["google_login"])


@google_auth_router.get("/auth/login")
async def google_login(request: Request):
    try:
        redirect_uri = os.getenv("REDIRECT_URI")
        return await oauth.google.authorize_redirect(request, redirect_uri)
    except Exception as e:
        return {"error": str(e)}


@google_auth_router.get("/auth/callback")
async def google_callback(request: Request, response: Response):
    token = await oauth.google.authorize_access_token(request)
    user_info = await get_user_info_from_google(token)

    email = user_info.get("email")
    name = user_info.get("name")
    picture = user_info.get("picture")

    user_from_db = get_or_create_user_use_case().__call__(
        CreateUserRequest(name=name, email=email)
    )

    role = user_from_db.user.user_type

    jwt_token = create_jwt_token(email=email, name=name, role=role, picture=picture)

    response = RedirectResponse(url=os.getenv("REDIRECT_RESPONSE"), status_code=302)
    response.set_cookie(
        key="jwt_token",
        value=jwt_token,
        secure=False,
        samesite="Lax",
    )
    return response
