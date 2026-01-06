"""Service layer for business logic."""
from typing import List, Optional, Protocol
from app.models import LeaderboardEntry, ScoreSubmission, GameMode
from app.exceptions import (
    ScoreInvalidError,
    UsernameInvalidError,
    DuplicateSubmissionError,
    RateLimitError,
)
from app.config import settings
from app.security import validate_username, validate_score, sanitize_username


class LeaderboardRepositoryProtocol(Protocol):
    """Protocol for leaderboard repository."""
    
    async def get_leaderboard(
        self,
        limit: int,
        offset: int,
        mode: Optional[GameMode],
        sort: str,
    ) -> tuple[List[LeaderboardEntry], int]:
        ...
    
    async def get_user_scores(
        self,
        username: str,
        limit: int,
        offset: int,
        mode: Optional[GameMode],
    ) -> tuple[List[LeaderboardEntry], int]:
        ...
    
    async def add_score(
        self,
        username: str,
        score: int,
        mode: GameMode,
    ) -> LeaderboardEntry:
        ...
    
    async def check_duplicate_submission(
        self,
        username: str,
        score: int,
        mode: GameMode,
        within_minutes: int,
    ) -> bool:
        ...
    
    async def get_stats(self) -> dict:
        ...


class LeaderboardService:
    """Service for leaderboard operations."""
    
    def __init__(self, repository: LeaderboardRepositoryProtocol):
        self.repository = repository
    
    async def get_leaderboard(
        self,
        limit: int = 10,
        offset: int = 0,
        mode: Optional[GameMode] = None,
        sort: str = "score",
    ) -> tuple[List[LeaderboardEntry], int]:
        """Get leaderboard entries."""
        # Validate limit
        if limit < 1 or limit > 100:
            limit = 10
        if offset < 0:
            offset = 0
        
        return await self.repository.get_leaderboard(limit, offset, mode, sort)
    
    async def get_user_scores(
        self,
        username: str,
        limit: int = 10,
        offset: int = 0,
        mode: Optional[GameMode] = None,
    ) -> tuple[List[LeaderboardEntry], int]:
        """Get scores for a specific user."""
        if limit < 1 or limit > 100:
            limit = 10
        if offset < 0:
            offset = 0
        
        return await self.repository.get_user_scores(username, limit, offset, mode)
    
    async def submit_score(self, submission: ScoreSubmission) -> LeaderboardEntry:
        """Submit a new score."""
        # Sanitize and validate username
        username = sanitize_username(submission.username)
        is_valid, error_msg = validate_username(username)
        if not is_valid:
            raise UsernameInvalidError(error_msg or "Invalid username")
        
        # Validate score range
        is_valid, error_msg = validate_score(
            submission.score,
            settings.min_score,
            settings.max_score
        )
        if not is_valid:
            raise ScoreInvalidError(error_msg or "Invalid score")
        
        # Check for duplicate submission
        is_duplicate = await self.repository.check_duplicate_submission(
            username, submission.score, submission.mode, within_minutes=1
        )
        if is_duplicate:
            raise DuplicateSubmissionError(
                "Same score submitted recently. Please wait before submitting again."
            )
        
        # Save to repository (repository handles entry creation)
        saved_entry = await self.repository.add_score(
            username=username,
            score=submission.score,
            mode=submission.mode,
        )
        
        return saved_entry
    
    async def get_stats(self) -> dict:
        """Get aggregate statistics."""
        return await self.repository.get_stats()


# Service factory function (will be used with dependency injection)
def create_leaderboard_service(repository: LeaderboardRepositoryProtocol) -> LeaderboardService:
    """Create a leaderboard service with the given repository."""
    return LeaderboardService(repository)

