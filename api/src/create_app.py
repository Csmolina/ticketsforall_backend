from contextlib import asynccontextmanager
from typing import AsyncGenerator
from api.src.routers import health_check_router, user_router
from fastapi import FastAPI
from adapters.src.repositories import Connection, SessionManager, SQLConnection


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    connection: Connection = SQLConnection()
    SessionManager.initialize_session(connection)
    yield
    SessionManager.close_session()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(health_check_router, tags=["health_check"])
    app.include_router(user_router, tags=["users"])
    return app
