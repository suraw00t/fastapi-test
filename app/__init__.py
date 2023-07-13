from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api import init_router
from app.core.config import get_app_settings
from app.models import init_beanie


def create_app() -> FastAPI:
    settings = get_app_settings()
    settings.configure_logging()

    app = FastAPI(**settings.fastapi_kwargs)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def init_app():
        await init_router(app, settings)
        await init_beanie(settings)

    return app
