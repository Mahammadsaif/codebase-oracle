from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import settings
from app.api import health

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def create_application() -> FastAPI:
    """Application factory pattern for dependency injection."""
    application = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify exact origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    application.include_router(health.router, prefix=settings.API_V1_STR, tags=["health"])

    return application

app = create_application()

@app.on_event("startup")
async def startup_event():
    """Runs when application starts."""
    logger.info("Starting Codebase Oracle API")

@app.on_event("shutdown")
async def shutdown_event():
    """Runs when application shuts down."""
    logger.info("Shutting down Codebase Oracle API")