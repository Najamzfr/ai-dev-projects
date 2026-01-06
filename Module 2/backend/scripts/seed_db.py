"""Script to seed the database with initial data."""
import asyncio
from sqlalchemy import select
from app.database import AsyncSessionLocal, init_db
from app.models_db import User, Score, GameModeEnum
from datetime import datetime, timedelta, timezone


async def seed_database():
    """Seed database with initial test data."""
    await init_db()
    
    async with AsyncSessionLocal() as session:
        # Create test users
        users_data = [
            {"username": "PLAYER1", "scores": [250, 180, 120]},
            {"username": "GAMER42", "scores": [200, 150]},
            {"username": "SNAKEMASTER", "scores": [300, 250, 200]},
            {"username": "RETRO_FAN", "scores": [150, 100]},
            {"username": "ARCADE_PRO", "scores": [220, 180, 140]},
        ]
        
        for user_data in users_data:
            # Get or create user
            result = await session.execute(
                select(User).where(User.username == user_data["username"])
            )
            user = result.scalar_one_or_none()
            
            if not user:
                # Create user
                user = User(username=user_data["username"])
                session.add(user)
                await session.flush()
            
            # Add scores
            for i, score_value in enumerate(user_data["scores"]):
                mode = GameModeEnum.WALLS if i % 2 == 0 else GameModeEnum.WALLS_THROUGH
                score = Score(
                    user_id=user.id,
                    score=score_value,
                    mode=mode,
                    date=datetime.now(timezone.utc) - timedelta(days=len(user_data["scores"]) - i),
                )
                session.add(score)
        
        await session.commit()
        print("Database seeded successfully!")


if __name__ == "__main__":
    asyncio.run(seed_database())

