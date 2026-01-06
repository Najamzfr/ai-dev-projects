"""API v1 router."""
from fastapi import APIRouter
from app.api.v1 import leaderboard

router = APIRouter(prefix="/api/v1")

router.include_router(leaderboard.router)

