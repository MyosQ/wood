from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from backend.api import abin, grunddata, raster
from backend.core.config import get_settings
from backend.core.logging import setup_logging
from backend.core.middleware import error_handler_middleware, request_id_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    settings = get_settings()
    setup_logging(debug=settings.debug)
    yield


app = FastAPI(
    title=get_settings().app_title,
    description="Backend API for accessing Skogsstyrelsen forest data APIs",
    version=get_settings().app_version,
    lifespan=lifespan,
)

# Error handling middleware (register first, runs second)
app.middleware("http")(error_handler_middleware)

# Request ID middleware (register second, runs first for proper tracing)
app.middleware("http")(request_id_middleware)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(raster.router)
app.include_router(grunddata.router)
app.include_router(abin.router)


@app.get("/")
def read_root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "Skogsstyrelsen API Gateway", "version": get_settings().app_version}


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


def main() -> None:
    """Entry point for running the application."""
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info",
    )


if __name__ == "__main__":
    main()
