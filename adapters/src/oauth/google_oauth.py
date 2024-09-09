import os
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request

oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.environ.get("OAUTH_CLIENT_ID"),
    client_secret=os.environ.get("OAUTH_CLIENT_SECRET"),
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    access_token_url="https://accounts.google.com/o/oauth2/token",
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri=os.environ.get("OAUTH_REDIRECT_URI"),
    client_kwargs={"scope": "openid profile email"},
)


async def get_google_user_data(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)
    return user_info
