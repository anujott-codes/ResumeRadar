from fastapi import APIRouter

from src.backend.schemas.response_schema import HealthResponse

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health_check():
    try:
        return {"status": "ok"}
    except Exception:
        return {"status": "down"}
