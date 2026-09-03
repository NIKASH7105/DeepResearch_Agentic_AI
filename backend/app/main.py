"""
Main FastAPI application
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.api import research, health

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management for the application"""
    # Startup
    logger.info("Starting DeepResearch Agent API")
    yield
    # Shutdown
    logger.info("Shutting down DeepResearch Agent API")


# Create FastAPI app
app = FastAPI(
    title="DeepResearch Agent API",
    description="Autonomous AI Research & Report Generation System",
    version="1.0.0",
    lifespan=lifespan
)

# ── CORS must be the FIRST (outermost) middleware ──────────────────────────
# Build a broad allowed-origins list that always includes common dev ports
_base_origins = settings.cors_origins_list
_dev_origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]
_allowed_origins = list(dict.fromkeys(_base_origins + _dev_origins))  # dedup, preserve order

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)

# ── Explicit OPTIONS catch-all ─────────────────────────────────────────────
# Ensures preflight requests always return 200 even if a route's body
# validation would otherwise produce a 400 before CORS headers are applied.
@app.options("/{rest_of_path:path}")
async def preflight_handler(rest_of_path: str, request: Request) -> Response:
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Max-Age": "600",
        },
    )

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(research.router, prefix="/api/research", tags=["research"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "DeepResearch Agent API",
        "version": "1.0.0",
        "status": "running"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
