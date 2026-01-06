"""Database repository implementation."""
from typing import List, Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models_db import User, Score, GameModeEnum
from app.models import LeaderboardEntry, GameMode


class DatabaseLeaderboardRepository:
    """Database repository for leaderboard data."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_leaderboard(
        self,
        limit: int = 10,
        offset: int = 0,
        mode: Optional[GameMode] = None,
        sort: str = "score",
    ) -> tuple[List[LeaderboardEntry], int]:
        """Get leaderboard entries with pagination and filtering."""
        # Build query
        query = select(Score, User.username).join(User, Score.user_id == User.id)
        
        # Filter by mode if specified
        if mode:
            db_mode = GameModeEnum.WALLS if mode == GameMode.WALLS else GameModeEnum.WALLS_THROUGH
            query = query.where(Score.mode == db_mode)
        
        # Filter active users only
        query = query.where(User.is_active == True)
        
        # Get total count (before sorting and pagination)
        count_base = select(Score.id).join(User, Score.user_id == User.id).where(User.is_active == True)
        if mode:
            db_mode = GameModeEnum.WALLS if mode == GameMode.WALLS else GameModeEnum.WALLS_THROUGH
            count_base = count_base.where(Score.mode == db_mode)
        count_query = select(func.count()).select_from(count_base.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar() or 0
        
        # Sort
        if sort == "score":
            query = query.order_by(Score.score.desc(), Score.date.desc())
        elif sort == "date":
            query = query.order_by(Score.date.desc(), Score.score.desc())
        
        # Apply pagination
        query = query.limit(limit).offset(offset)
        
        # Execute query
        result = await self.session.execute(query)
        rows = result.all()
        
        # Convert to LeaderboardEntry
        entries = [
            LeaderboardEntry(
                id=score.id,
                username=username,
                score=score.score,
                mode=score.mode.value,
                date=score.date.isoformat() if isinstance(score.date, datetime) else score.date,
            )
            for score, username in rows
        ]
        
        return entries, total
    
    async def get_user_scores(
        self,
        username: str,
        limit: int = 10,
        offset: int = 0,
        mode: Optional[GameMode] = None,
    ) -> tuple[List[LeaderboardEntry], int]:
        """Get scores for a specific user."""
        # Build query
        query = (
            select(Score, User.username)
            .join(User, Score.user_id == User.id)
            .where(User.username.ilike(username))
            .where(User.is_active == True)
        )
        
        if mode:
            db_mode = GameModeEnum.WALLS if mode == GameMode.WALLS else GameModeEnum.WALLS_THROUGH
            query = query.where(Score.mode == db_mode)
        
        # Get total count (before sorting and pagination)
        count_base = (
            select(Score.id)
            .join(User, Score.user_id == User.id)
            .where(User.username.ilike(username))
            .where(User.is_active == True)
        )
        if mode:
            db_mode = GameModeEnum.WALLS if mode == GameMode.WALLS else GameModeEnum.WALLS_THROUGH
            count_base = count_base.where(Score.mode == db_mode)
        count_query = select(func.count()).select_from(count_base.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar() or 0
        
        # Sort by score descending
        query = query.order_by(Score.score.desc(), Score.date.desc())
        
        # Apply pagination
        query = query.limit(limit).offset(offset)
        
        # Execute query
        result = await self.session.execute(query)
        rows = result.all()
        
        # Convert to LeaderboardEntry
        entries = [
            LeaderboardEntry(
                id=score.id,
                username=username,
                score=score.score,
                mode=score.mode.value,
                date=score.date.isoformat() if isinstance(score.date, datetime) else score.date,
            )
            for score, username in rows
        ]
        
        return entries, total
    
    async def get_or_create_user(self, username: str) -> User:
        """Get existing user or create new one."""
        # Normalize username
        username = username.strip().upper()
        
        # Try to get existing user
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        user = result.scalar_one_or_none()
        
        if user:
            return user
        
        # Create new user
        user = User(username=username)
        self.session.add(user)
        await self.session.flush()  # Flush to get ID
        return user
    
    async def add_score(
        self,
        username: str,
        score: int,
        mode: GameMode,
    ) -> LeaderboardEntry:
        """Add a new score entry."""
        # Get or create user
        user = await self.get_or_create_user(username)
        
        # Convert mode
        db_mode = GameModeEnum.WALLS if mode == GameMode.WALLS else GameModeEnum.WALLS_THROUGH
        
        # Create score
        score_obj = Score(
            user_id=user.id,
            score=score,
            mode=db_mode,
        )
        self.session.add(score_obj)
        await self.session.flush()  # Flush to get ID
        
        # Convert to LeaderboardEntry
        entry = LeaderboardEntry(
            id=score_obj.id,
            username=user.username,
            score=score_obj.score,
            mode=score_obj.mode.value,
            date=score_obj.date.isoformat() if isinstance(score_obj.date, datetime) else score_obj.date,
        )
        
        return entry
    
    async def check_duplicate_submission(
        self,
        username: str,
        score: int,
        mode: GameMode,
        within_minutes: int = 1,
    ) -> bool:
        """Check if the same score was submitted recently."""
        username = username.strip().upper()
        db_mode = GameModeEnum.WALLS if mode == GameMode.WALLS else GameModeEnum.WALLS_THROUGH
        
        # Get user
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            return False
        
        # Check for recent submission
        cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=within_minutes)
        query = (
            select(func.count(Score.id))
            .where(Score.user_id == user.id)
            .where(Score.score == score)
            .where(Score.mode == db_mode)
            .where(Score.created_at >= cutoff_time)
        )
        
        result = await self.session.execute(query)
        count = result.scalar() or 0
        
        return count > 0
    
    async def get_stats(self) -> dict:
        """Get aggregate statistics."""
        # Total players (active users)
        total_players_result = await self.session.execute(
            select(func.count(User.id)).where(User.is_active == True)
        )
        total_players = total_players_result.scalar() or 0
        
        # Total scores
        total_scores_result = await self.session.execute(
            select(func.count(Score.id))
        )
        total_scores = total_scores_result.scalar() or 0
        
        # Average score
        avg_score_result = await self.session.execute(
            select(func.avg(Score.score))
        )
        avg_score = avg_score_result.scalar() or 0.0
        
        # Top score
        top_score_result = await self.session.execute(
            select(func.max(Score.score))
        )
        top_score = top_score_result.scalar() or 0
        
        return {
            "total_players": total_players,
            "total_scores": total_scores,
            "average_score": round(float(avg_score) if avg_score else 0, 2),
            "top_score": top_score or 0,
        }

