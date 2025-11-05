"""
Application configuration management.

This module handles all configuration settings using Pydantic settings
for validation and type safety.
"""

from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with validation."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    DEBUG: bool = Field(default=False, description="Debug mode")
    SECRET_KEY: str = Field(..., description="Secret key for JWT signing")
    PROJECT_NAME: str = Field(default="Todo API", description="Project name")
    VERSION: str = Field(default="1.0.0", description="API version")

    # Server
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")

    # Database
    DATABASE_URL: str = Field(
        ...,
        description="PostgreSQL database connection URL",
    )

    # Redis
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL",
    )
    REDIS_ENABLED: bool = Field(default=True, description="Enable Redis caching")

    # Security
    ALLOWED_HOSTS: List[str] = Field(
        default_factory=lambda: ["localhost", "127.0.0.1"],
        description="Allowed host headers",
    )
    CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://localhost:3001"],
        description="CORS allowed origins",
    )

    # JWT
    JWT_SECRET_KEY: str = Field(..., description="JWT secret key")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=1440, description="JWT access token expiration in minutes"
    )

    # Password
    PASSWORD_MIN_LENGTH: int = Field(default=12, description="Minimum password length")
    PASSWORD_REQUIRE_UPPERCASE: bool = Field(
        default=True, description="Require uppercase in password"
    )
    PASSWORD_REQUIRE_LOWERCASE: bool = Field(
        default=True, description="Require lowercase in password"
    )
    PASSWORD_REQUIRE_NUMBER: bool = Field(
        default=True, description="Require number in password"
    )
    PASSWORD_REQUIRE_SPECIAL: bool = Field(
        default=True, description="Require special character in password"
    )
    BCRYPT_ROUNDS: int = Field(default=12, description="Bcrypt rounds")

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = Field(default=True, description="Enable rate limiting")
    RATE_LIMIT_PER_MINUTE: int = Field(
        default=100, description="Requests per minute per user"
    )
    RATE_LIMIT_LOGIN_ATTEMPTS: int = Field(
        default=5, description="Login attempts per window"
    )
    RATE_LIMIT_LOGIN_WINDOW_MINUTES: int = Field(
        default=15, description="Login rate limit window in minutes"
    )
    RATE_LIMIT_REGISTRATION_ATTEMPTS: int = Field(
        default=3, description="Registration attempts per window"
    )
    RATE_LIMIT_REGISTRATION_WINDOW_HOURS: int = Field(
        default=1, description="Registration rate limit window in hours"
    )

    @field_validator("SECRET_KEY", "JWT_SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Validate secret key strength."""
        if len(v) < 32:
            raise ValueError("Secret key must be at least 32 characters")
        return v

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate database URL format."""
        if not v.startswith(("postgresql://", "postgresql+asyncpg://")):
            raise ValueError("Database URL must start with postgresql:// or postgresql+asyncpg://")
        return v

    @field_validator("PASSWORD_MIN_LENGTH")
    @classmethod
    def validate_password_length(cls, v: int) -> int:
        """Validate password minimum length."""
        if v < 8:
            raise ValueError("Password minimum length must be at least 8")
        return v


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()

