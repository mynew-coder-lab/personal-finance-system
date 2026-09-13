"""
FastAPI application entry point.

Configures:
- CORS middleware
- Health check endpoint
- Global exception handling
- Startup/shutdown logging
- API router mounting (added as routes are built)
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.backend.config import settings
from app.backend.database.database import engine
from app.backend.routes.auth import router as auth_router
from app.backend.utils.logging import logger


# ── Lifespan ─────────────────────────────────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    logger.info(
        "Starting %s [env=%s, debug=%s]",
        settings.APP_NAME,
        settings.APP_ENV,
        settings.DEBUG,
    )
    yield
    logger.info("Shutting down %s", settings.APP_NAME)
    engine.dispose()


# ── Application ──────────────────────────────────────────────────


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── API Routers ──────────────────────────────────────────────────

app.include_router(auth_router, prefix=settings.API_V1_STR)


# ── Global Exception Handler ────────────────────────────────────


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch unhandled exceptions, log diagnostics, return safe message."""
    logger.error(
        "Unhandled exception on %s %s: %s",
        request.method,
        request.url.path,
        str(exc),
        exc_info=True,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred"},
    )


# ── Health Check ─────────────────────────────────────────────────


@app.get("/health", tags=["Health"])
def health_check():
    """
    Application health check.

    Returns application status and database connectivity.
    """
    db_status = "healthy"
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as e:
        logger.error("Database health check failed: %s", str(e))
        db_status = "unhealthy"

    overall = "healthy" if db_status == "healthy" else "degraded"

    return {
        "status": overall,
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "database": db_status,
    }


# ── Root ─────────────────────────────────────────────────────────


@app.get("/", tags=["Root"])
def root():
    """API root — basic information."""
    return {
        "app": settings.APP_NAME,
        "version": "0.1.0",
        "docs": "/docs",
    }
