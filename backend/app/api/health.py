"""
Health check endpoints
"""
from fastapi import APIRouter
from datetime import datetime
from app.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


@router.get("/config")
async def get_config():
    """Get non-sensitive configuration"""
    return {
        "llm_model": settings.llm_model,
        "max_research_iterations": settings.max_research_iterations,
        "max_sources_per_query": settings.max_sources_per_query,
    }
