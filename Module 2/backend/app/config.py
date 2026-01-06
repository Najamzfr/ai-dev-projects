"""Application configuration using pydantic-settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # Server
    port: int = 8000
    host: str = "0.0.0.0"
    environment: str = "development"  # development, staging, production
    
    # Database (for future use)
    database_url: str = "sqlite:///./snake_game.db"
    
    @field_validator('database_url')
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate database URL format."""
        valid_schemes = ['sqlite://', 'sqlite+aiosqlite://', 'postgresql://', 'postgresql+asyncpg://', 'mysql://']
        if not any(v.startswith(scheme) for scheme in valid_schemes):
            raise ValueError(
                f"database_url must start with one of: {', '.join(valid_schemes)}"
            )
        return v
    database_pool_size_min: int = 5
    database_pool_size_max: int = 20
    
    # CORS
    cors_origins: List[str] = ["http://localhost:8080", "http://localhost:5173"]
    allow_credentials: bool = True
    
    # Logging
    log_level: str = "INFO"  # DEBUG, INFO, WARNING, ERROR
    log_format: str = "text"  # text for development (readable), json for production
    
    # Security
    rate_limit_per_minute: int = 60
    max_score: int = 999999
    min_score: int = 0
    
    # Optional: Redis for caching
    redis_url: str = ""
    cache_ttl_seconds: int = 30
    
    def get_cors_origins(self) -> List[str]:
        """Get CORS origins, handling comma-separated string."""
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return self.cors_origins


# Global settings instance
settings = Settings()

