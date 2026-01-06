"""Tests for service layer."""
import pytest
from app.services import LeaderboardService, create_leaderboard_service
from app.repository_db import DatabaseLeaderboardRepository
from app.models import ScoreSubmission, GameMode
from app.exceptions import ScoreInvalidError, UsernameInvalidError, DuplicateSubmissionError
from app.config import settings


@pytest.mark.asyncio
class TestLeaderboardService:
    """Tests for LeaderboardService."""
    
    async def test_get_leaderboard(self, db_session, test_scores):
        """Test getting leaderboard through service."""
        repo = DatabaseLeaderboardRepository(db_session)
        service = create_leaderboard_service(repo)
        
        entries, total = await service.get_leaderboard(limit=10, offset=0)
        
        assert total >= 3
        assert len(entries) >= 3
    
    async def test_submit_score_valid(self, db_session):
        """Test submitting a valid score."""
        repo = DatabaseLeaderboardRepository(db_session)
        service = create_leaderboard_service(repo)
        
        submission = ScoreSubmission(
            username="NEWPLAYER",
            score=250,
            mode="walls"
        )
        
        entry = await service.submit_score(submission)
        
        assert entry.username == "NEWPLAYER"
        assert entry.score == 250
        assert entry.mode == "walls"
    
    async def test_submit_score_invalid_range(self, db_session):
        """Test submitting score outside valid range."""
        repo = DatabaseLeaderboardRepository(db_session)
        service = create_leaderboard_service(repo)
        
        # Score too high
        submission = ScoreSubmission(
            username="PLAYER1",
            score=settings.max_score + 1,
            mode="walls"
        )
        
        with pytest.raises(ScoreInvalidError):
            await service.submit_score(submission)
        
        # Score too low
        submission = ScoreSubmission(
            username="PLAYER1",
            score=settings.min_score - 1,
            mode="walls"
        )
        
        with pytest.raises(ScoreInvalidError):
            await service.submit_score(submission)
    
    async def test_submit_score_duplicate(self, db_session):
        """Test submitting duplicate score."""
        repo = DatabaseLeaderboardRepository(db_session)
        service = create_leaderboard_service(repo)
        
        submission = ScoreSubmission(
            username="PLAYER1",
            score=250,
            mode="walls"
        )
        
        # First submission
        await service.submit_score(submission)
        
        # Duplicate submission (should fail)
        with pytest.raises(DuplicateSubmissionError):
            await service.submit_score(submission)
    
    async def test_get_user_scores(self, db_session, test_user, test_scores):
        """Test getting user scores through service."""
        repo = DatabaseLeaderboardRepository(db_session)
        service = create_leaderboard_service(repo)
        
        entries, total = await service.get_user_scores(
            username=test_user.username,
            limit=10,
            offset=0
        )
        
        assert total == 3
        assert len(entries) == 3
    
    async def test_get_stats(self, db_session, test_scores):
        """Test getting statistics through service."""
        repo = DatabaseLeaderboardRepository(db_session)
        service = create_leaderboard_service(repo)
        
        stats = await service.get_stats()
        
        assert stats["total_scores"] >= 3
        assert stats["average_score"] > 0
        assert stats["top_score"] > 0

