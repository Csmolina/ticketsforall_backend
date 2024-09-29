from contextlib import asynccontextmanager
import os
from typing import AsyncGenerator
from api.src.routers import health_check_router, user_router, google_auth_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from adapters.src.repositories import Connection, SessionManager, SQLConnection
from starlette.middleware.sessions import SessionMiddleware
from factories.config.cors import cors_config


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    connection: Connection = SQLConnection()
    SessionManager.initialize_session(connection)
    yield
    SessionManager.close_session()


def create_app() -> FastAPI:
    secret_key = os.getenv("SECRET_KEY")
    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        SessionMiddleware,
        secret_key=secret_key,
    )
    cors_data = cors_config()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_data["allow_origins"],
        allow_credentials=cors_data["allow_credentials"],
        allow_methods=cors_data["allow_methods"],
        allow_headers=cors_data["allow_headers"],
    )
    app.include_router(health_check_router, tags=["health_check"])
    app.include_router(user_router, tags=["users"])
    app.include_router(google_auth_router, tags=["google_login"])
    return app
