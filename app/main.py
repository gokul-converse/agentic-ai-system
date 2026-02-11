from fastapi import FastAPI
from app.api.router import router as api_router
from app.config.logging import setup_logging
from app.utils.logger import logger
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings

def create_app() -> FastAPI:

    # Setup logging
    setup_logging()

    app = FastAPI(
        title="Agentic AI Platform",
        version="1.0.0"
    )

    app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

    # Register API routes
    app.include_router(api_router)

    logger.info("Application startup complete")

    return app

app = create_app()
