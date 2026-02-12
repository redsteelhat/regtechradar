"""Health check route."""
from fastapi import APIRouter

router = APIRouter()


@router.get("")
def health() -> dict:
    """Liveness check."""
    return {"status": "ok"}
