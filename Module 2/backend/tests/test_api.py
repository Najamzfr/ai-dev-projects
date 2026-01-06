"""Tests for API endpoints."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestHealthEndpoints:
    """Tests for health check endpoints."""
    
    async def test_health_check(self, client: AsyncClient):
        """Test basic health check."""
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    async def test_db_health_check(self, client: AsyncClient):
        """Test database health check."""
        response = await client.get("/health/db")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "db_connected" in data


@pytest.mark.asyncio
class TestLeaderboardEndpoints:
    """Tests for leaderboard endpoints."""
    
    async def test_get_leaderboard(self, client: AsyncClient, test_scores):
        """Test getting leaderboard."""
        response = await client.get("/api/v1/leaderboard")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "meta" in data
        assert len(data["data"]) > 0
        assert data["meta"]["total"] > 0
    
    async def test_get_leaderboard_with_params(self, client: AsyncClient, test_scores):
        """Test getting leaderboard with query parameters."""
        response = await client.get(
            "/api/v1/leaderboard",
            params={"limit": 5, "offset": 0, "mode": "walls", "sort": "score"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) <= 5
    
    async def test_submit_score(self, client: AsyncClient):
        """Test submitting a score."""
        response = await client.post(
            "/api/v1/leaderboard",
            json={
                "username": "TESTPLAYER",
                "score": 300,
                "mode": "walls"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "TESTPLAYER"
        assert data["score"] == 300
        assert data["mode"] == "walls"
    
    async def test_submit_score_invalid(self, client: AsyncClient):
        """Test submitting invalid score."""
        # Score too high
        response = await client.post(
            "/api/v1/leaderboard",
            json={
                "username": "TESTPLAYER",
                "score": 9999999,
                "mode": "walls"
            }
        )
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
    
    async def test_get_user_scores(self, client: AsyncClient, test_user, test_scores):
        """Test getting user scores."""
        response = await client.get(f"/api/v1/leaderboard/{test_user.username}")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) > 0
        assert all(entry["username"] == test_user.username for entry in data["data"])
    
    async def test_get_user_scores_not_found(self, client: AsyncClient):
        """Test getting scores for non-existent user."""
        response = await client.get("/api/v1/leaderboard/NONEXISTENT")
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
    
    async def test_get_stats(self, client: AsyncClient, test_scores):
        """Test getting statistics."""
        response = await client.get("/api/v1/leaderboard/stats/summary")
        assert response.status_code == 200
        data = response.json()
        assert "total_players" in data
        assert "total_scores" in data
        assert "average_score" in data
        assert "top_score" in data

