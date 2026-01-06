"""Tests for Pydantic models."""
import pytest
from app.models import ScoreSubmission, LeaderboardEntry, GameMode
from pydantic import ValidationError


class TestScoreSubmission:
    """Tests for ScoreSubmission model."""
    
    def test_valid_submission(self):
        """Test valid score submission."""
        submission = ScoreSubmission(
            username="PLAYER1",
            score=250,
            mode="walls"
        )
        assert submission.username == "PLAYER1"
        assert submission.score == 250
        assert submission.mode == "walls"
    
    def test_username_validation(self):
        """Test username validation."""
        # Valid username
        submission = ScoreSubmission(
            username="PLAYER_1",
            score=100,
            mode="walls"
        )
        assert submission.username == "PLAYER_1"
        
        # Username too short
        with pytest.raises(ValidationError):
            ScoreSubmission(username="A", score=100, mode="walls")
        
        # Username too long
        with pytest.raises(ValidationError):
            ScoreSubmission(username="A" * 21, score=100, mode="walls")
    
    def test_score_validation(self):
        """Test score validation."""
        # Valid score
        submission = ScoreSubmission(
            username="PLAYER1",
            score=0,
            mode="walls"
        )
        assert submission.score == 0
        
        # Negative score
        with pytest.raises(ValidationError):
            ScoreSubmission(username="PLAYER1", score=-1, mode="walls")
        
        # Score too high
        with pytest.raises(ValidationError):
            ScoreSubmission(username="PLAYER1", score=1000000, mode="walls")
    
    def test_mode_validation(self):
        """Test game mode validation."""
        # Valid modes
        submission1 = ScoreSubmission(
            username="PLAYER1",
            score=100,
            mode="walls"
        )
        assert submission1.mode == "walls"
        
        submission2 = ScoreSubmission(
            username="PLAYER1",
            score=100,
            mode="walls-through"
        )
        assert submission2.mode == "walls-through"
        
        # Invalid mode
        with pytest.raises(ValidationError):
            ScoreSubmission(username="PLAYER1", score=100, mode="invalid")


class TestLeaderboardEntry:
    """Tests for LeaderboardEntry model."""
    
    def test_valid_entry(self):
        """Test valid leaderboard entry."""
        entry = LeaderboardEntry(
            username="PLAYER1",
            score=250,
            mode="walls",
            date="2024-01-15T10:30:00Z"
        )
        assert entry.username == "PLAYER1"
        assert entry.score == 250
        assert entry.mode == "walls"

