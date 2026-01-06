"""Database configuration and session management."""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import StaticPool
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Create async engine
# Convert sqlite:// to sqlite+aiosqlite:// for async support
database_url = settings.database_url
if database_url.startswith("sqlite"):
    database_url = database_url.replace("sqlite://", "sqlite+aiosqlite://", 1)
    # SQLite doesn't support connection pooling - use StaticPool
    engine = create_async_engine(
        database_url,
        echo=settings.environment == "development",  # Log SQL queries in development
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    # PostgreSQL/MySQL support connection pooling
    engine = create_async_engine(
        database_url,
        echo=settings.environment == "development",
        pool_size=settings.database_pool_size_min,
        max_overflow=settings.database_pool_size_max - settings.database_pool_size_min,
        pool_pre_ping=True,  # Verify connections before using
    )

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """Dependency for getting database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database (create tables)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized")


async def close_db():
    """Close database connections."""
    await engine.dispose()
    logger.info("Database connections closed")


async def check_db_health() -> bool:
    """Check if database is accessible."""
    try:
        from sqlalchemy import text
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
            await session.commit()
            return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False

