from fastapi import APIRouter, status
from datetime import datetime

router = APIRouter()

@router.get(
    "/health",
    summary="Health check",
    description="Check if the API is running properly",
    response_description="API status and timestamp"
)
async def health_check():
    """Comprehensive health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "codebase-oracle-api"
    }