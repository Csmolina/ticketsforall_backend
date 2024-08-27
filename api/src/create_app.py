from api.src.routers import health_check_router
from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(health_check_router, tags=["health_check"])
    return app
