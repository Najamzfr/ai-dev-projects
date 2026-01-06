"""Pydantic models for request/response validation."""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from datetime import datetime, timezone
from enum import Enum


class GameMode(str, Enum):
    """Game mode enumeration."""
    WALLS = "walls"
    WALLS_THROUGH = "walls-through"


class LeaderboardEntry(BaseModel):
    """Leaderboard entry model."""
    id: Optional[int] = None
    username: str = Field(..., min_length=2, max_length=20)
    score: int = Field(..., ge=0, le=999999)
    mode: GameMode
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "PLAYER1",
                "score": 250,
                "mode": "walls",
                "date": "2024-01-15T10:30:00Z",
            }
        }


class ScoreSubmission(BaseModel):
    """Score submission model."""
    username: str = Field(..., min_length=2, max_length=20)
    score: int = Field(..., ge=0, le=999999)
    mode: GameMode
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Validate username format."""
        v = v.strip().upper()
        # Allow alphanumeric and underscore only
        if not v.replace("_", "").isalnum():
            raise ValueError("Username must contain only alphanumeric characters and underscores")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "PLAYER1",
                "score": 250,
                "mode": "walls",
            }
        }


class PaginationMeta(BaseModel):
    """Pagination metadata."""
    total: int
    limit: int
    offset: int
    has_more: bool


class PaginatedResponse(BaseModel):
    """Paginated response model."""
    data: list[LeaderboardEntry]
    meta: PaginationMeta


class ErrorResponse(BaseModel):
    """Standardized error response model."""
    error: dict[str, Any]
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid request data",
                    "details": {},
                }
            }
        }


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: str
    version: str = "1.0.0"

