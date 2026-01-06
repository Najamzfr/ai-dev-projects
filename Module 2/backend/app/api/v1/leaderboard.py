"""Leaderboard API endpoints."""
from fastapi import APIRouter, Query, Path, Depends, Request
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    LeaderboardEntry,
    ScoreSubmission,
    PaginatedResponse,
    PaginationMeta,
    GameMode,
)
from app.services import create_leaderboard_service, LeaderboardService
from app.repository_db import DatabaseLeaderboardRepository
from app.database import get_db
from app.exceptions import NotFoundError
from app.rate_limit import score_submission_limit

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


def get_leaderboard_service(
    db: AsyncSession = Depends(get_db),
) -> LeaderboardService:
    """Dependency to get leaderboard service with database repository."""
    repository = DatabaseLeaderboardRepository(db)
    return create_leaderboard_service(repository)


@router.get("", response_model=PaginatedResponse)
async def get_leaderboard(
    limit: int = Query(default=10, ge=1, le=100, description="Number of results"),
    offset: int = Query(default=0, ge=0, description="Offset for pagination"),
    mode: Optional[GameMode] = Query(default=None, description="Filter by game mode"),
    sort: str = Query(default="score", pattern="^(score|date)$", description="Sort order"),
    service: LeaderboardService = Depends(get_leaderboard_service),
):
    """Get leaderboard entries with pagination and filtering."""
    entries, total = await service.get_leaderboard(limit, offset, mode, sort)
    
    return PaginatedResponse(
        data=entries,
        meta=PaginationMeta(
            total=total,
            limit=limit,
            offset=offset,
            has_more=(offset + limit) < total,
        ),
    )


@router.post("", response_model=LeaderboardEntry, status_code=201)
@score_submission_limit  # Rate limit score submissions
async def submit_score(
    request: Request,
    submission: ScoreSubmission,
    service: LeaderboardService = Depends(get_leaderboard_service),
):
    """Submit a new score to the leaderboard."""
    entry = await service.submit_score(submission)
    return entry


@router.get("/stats/summary", response_model=dict)
async def get_stats(
    service: LeaderboardService = Depends(get_leaderboard_service),
):
    """Get aggregate statistics."""
    stats = await service.get_stats()
    return stats


@router.get("/{username}", response_model=PaginatedResponse)
async def get_user_scores(
    username: str = Path(..., description="Username to get scores for"),
    limit: int = Query(default=10, ge=1, le=100, description="Number of results"),
    offset: int = Query(default=0, ge=0, description="Offset for pagination"),
    mode: Optional[GameMode] = Query(default=None, description="Filter by game mode"),
    service: LeaderboardService = Depends(get_leaderboard_service),
):
    """Get scores for a specific user."""
    entries, total = await service.get_user_scores(username, limit, offset, mode)
    
    if total == 0:
        raise NotFoundError(f"No scores found for user: {username}")
    
    return PaginatedResponse(
        data=entries,
        meta=PaginationMeta(
            total=total,
            limit=limit,
            offset=offset,
            has_more=(offset + limit) < total,
        ),
    )

