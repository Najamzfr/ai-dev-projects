"""Main FastAPI application entry point."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime, timezone
import os
import logging

from app.config import settings
from app.logging_config import setup_logging
from app.middleware import RequestIDMiddleware, LoggingMiddleware
from app.exceptions import (
    APIException,
    api_exception_handler,
    validation_exception_handler,
    http_exception_handler,
    general_exception_handler,
)
from app.api.v1.router import router as api_v1_router
from app.models import HealthResponse
from app.database import init_db, close_db, check_db_health
from app.rate_limit import setup_rate_limiting
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Check if static files exist (production mode with frontend)
STATIC_DIR = "static"
HAS_STATIC_FILES = os.path.exists(STATIC_DIR) and os.path.isdir(STATIC_DIR)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info("Starting Snake Game API...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Static files mode: {'Enabled' if HAS_STATIC_FILES else 'Disabled (API only)'}")
    await init_db()
    logger.info("Application started successfully!")
    yield
    # Shutdown
    logger.info("Shutting down...")
    await close_db()
    logger.info("Application shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="Snake Game API",
    description="Backend API for Snake Game Leaderboard",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=settings.allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.add_middleware(RequestIDMiddleware)
app.add_middleware(LoggingMiddleware)

# Setup rate limiting
setup_rate_limiting(app)

# Register exception handlers
app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Mount API routes
# When serving static files, API is under /api prefix
# When API-only mode, API is at root with /api/v1 prefix
if HAS_STATIC_FILES:
    # Production mode with frontend
    logger.info("Mounting API at /api/v1")
    app.include_router(api_v1_router, prefix="/api")
else:
    # Development mode - API only
    logger.info("Mounting API at /api/v1 (API-only mode)")
    app.include_router(api_v1_router)

# Health check endpoint (no DB dependency)
@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# Database health check endpoint
@app.get("/health/db", tags=["health"])
async def health_check_db():
    """Database health check endpoint."""
    is_healthy = await check_db_health()
    return {
        "status": "healthy" if is_healthy else "unhealthy",
        "db_connected": is_healthy,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """Root endpoint."""
    if HAS_STATIC_FILES:
        # Serve frontend index.html
        return FileResponse(os.path.join(STATIC_DIR, "index.html"))
    else:
        # API info for API-only mode
        return {
            "message": "Snake Game API",
            "version": "1.0.0",
            "docs": "/docs",
        }


# Serve static files if they exist (production mode)
if HAS_STATIC_FILES:
    logger.info("Setting up static file serving...")
    
    # Mount static assets (JS, CSS, images)
    app.mount("/assets", StaticFiles(directory=os.path.join(STATIC_DIR, "assets")), name="assets")
    
    # Serve favicon if it exists
    @app.get("/favicon.ico")
    async def favicon():
        """Serve favicon."""
        favicon_path = os.path.join(STATIC_DIR, "favicon.ico")
        if os.path.exists(favicon_path):
            return FileResponse(favicon_path)
        return {"error": "Not found"}
    
    # Catch-all route for React Router (SPA)
    # This must be last to not override other routes
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """Serve React app for all non-API routes."""
        # Check if it's a file in static directory
        file_path = os.path.join(STATIC_DIR, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        
        # Otherwise, serve index.html for client-side routing
        return FileResponse(os.path.join(STATIC_DIR, "index.html"))
    
    logger.info("Static file serving configured successfully")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "development",
    )
