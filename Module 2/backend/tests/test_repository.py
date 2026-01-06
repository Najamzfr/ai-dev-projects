"""Tests for database repository."""
import pytest
from app.repository_db import DatabaseLeaderboardRepository
from app.models import GameMode


@pytest.mark.asyncio
class TestDatabaseLeaderboardRepository:
    """Tests for DatabaseLeaderboardRepository."""
    
    async def test_get_leaderboard(self, db_session, test_scores):
        """Test getting leaderboard."""
        repo = DatabaseLeaderboardRepository(db_session)
        entries, total = await repo.get_leaderboard(limit=10, offset=0)
        
        assert total >= 3
        assert len(entries) >= 3
        assert all(entry.score >= 0 for entry in entries)
    
    async def test_get_leaderboard_with_mode_filter(self, db_session, test_scores):
        """Test getting leaderboard with mode filter."""
        repo = DatabaseLeaderboardRepository(db_session)
        entries, total = await repo.get_leaderboard(
            limit=10,
            offset=0,
            mode=GameMode.WALLS
        )
        
        assert all(entry.mode == "walls" for entry in entries)
    
    async def test_get_leaderboard_pagination(self, db_session, test_scores):
        """Test leaderboard pagination."""
        repo = DatabaseLeaderboardRepository(db_session)
        
        # First page
        entries1, total1 = await repo.get_leaderboard(limit=2, offset=0)
        assert len(entries1) <= 2
        assert total1 >= 3
        
        # Second page
        entries2, total2 = await repo.get_leaderboard(limit=2, offset=2)
        assert len(entries2) <= 2
        assert total2 == total1
    
    async def test_get_user_scores(self, db_session, test_user, test_scores):
        """Test getting user scores."""
        repo = DatabaseLeaderboardRepository(db_session)
        entries, total = await repo.get_user_scores(
            username=test_user.username,
            limit=10,
            offset=0
        )
        
        assert total == 3
        assert len(entries) == 3
        assert all(entry.username == test_user.username for entry in entries)
    
    async def test_get_or_create_user(self, db_session):
        """Test getting or creating user."""
        repo = DatabaseLeaderboardRepository(db_session)
        
        # Create new user
        user1 = await repo.get_or_create_user("NEWUSER")
        assert user1.username == "NEWUSER"
        assert user1.id is not None
        
        # Get existing user
        user2 = await repo.get_or_create_user("NEWUSER")
        assert user2.id == user1.id
    
    async def test_add_score(self, db_session, test_user):
        """Test adding a score."""
        repo = DatabaseLeaderboardRepository(db_session)
        
        entry = await repo.add_score(
            username=test_user.username,
            score=300,
            mode=GameMode.WALLS
        )
        
        assert entry.username == test_user.username
        assert entry.score == 300
        assert entry.mode == "walls"
        assert entry.id is not None
    
    async def test_check_duplicate_submission(self, db_session, test_user):
        """Test duplicate submission detection."""
        repo = DatabaseLeaderboardRepository(db_session)
        
        # Add first score
        await repo.add_score(
            username=test_user.username,
            score=250,
            mode=GameMode.WALLS
        )
        
        # Check for duplicate (should be True within 1 minute)
        is_duplicate = await repo.check_duplicate_submission(
            username=test_user.username,
            score=250,
            mode=GameMode.WALLS,
            within_minutes=1
        )
        
        assert is_duplicate is True
    
    async def test_get_stats(self, db_session, test_user, test_scores):
        """Test getting statistics."""
        repo = DatabaseLeaderboardRepository(db_session)
        stats = await repo.get_stats()
        
        assert "total_players" in stats
        assert "total_scores" in stats
        assert "average_score" in stats
        assert "top_score" in stats
        assert stats["total_scores"] >= 3

