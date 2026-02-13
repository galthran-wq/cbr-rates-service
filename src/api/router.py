from fastapi import APIRouter

from src.api.endpoints import health, rates

router = APIRouter()
router.include_router(health.router, tags=["health"])
router.include_router(rates.router, tags=["rates"])
