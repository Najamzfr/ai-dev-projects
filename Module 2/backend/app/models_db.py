"""SQLAlchemy database models."""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.database import Base


class GameModeEnum(str, enum.Enum):
    """Game mode enumeration for database."""
    WALLS = "walls"
    WALLS_THROUGH = "walls-through"


class User(Base):
    """User model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationship to scores
    scores = relationship("Score", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class Score(Base):
    """Score model."""
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Integer, nullable=False, index=True)
    mode = Column(Enum(GameModeEnum), nullable=False, index=True)
    date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationship to user
    user = relationship("User", back_populates="scores")

    def __repr__(self):
        return f"<Score(id={self.id}, user_id={self.user_id}, score={self.score}, mode='{self.mode}')>"


# Composite indexes for common queries
Index(
    "idx_user_mode_score",
    Score.user_id,
    Score.mode,
    Score.score.desc()
)

Index(
    "idx_mode_score_date",
    Score.mode,
    Score.score.desc(),
    Score.date.desc()
)

Index(
    "idx_date_desc",
    Score.date.desc()
)

