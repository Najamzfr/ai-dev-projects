"""Pytest configuration and fixtures."""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.models_db import User, Score, GameModeEnum
from main import app


# Test database URL (in-memory SQLite)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False,
)

# Create test session factory
TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture
async def db_session():
    """Create a test database session."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def override_get_db(db_session):
    """Override the get_db dependency."""
    async def _get_db():
        yield db_session
    return _get_db


@pytest.fixture
async def client(override_get_db):
    """Create a test client."""
    app.dependency_overrides[get_db] = override_get_db
    from httpx import AsyncClient
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(db_session):
    """Create a test user."""
    user = User(username="TESTUSER")
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def test_scores(db_session, test_user):
    """Create test scores."""
    scores = [
        Score(user_id=test_user.id, score=250, mode=GameModeEnum.WALLS),
        Score(user_id=test_user.id, score=180, mode=GameModeEnum.WALLS_THROUGH),
        Score(user_id=test_user.id, score=120, mode=GameModeEnum.WALLS),
    ]
    for score in scores:
        db_session.add(score)
    await db_session.flush()
    return scores

