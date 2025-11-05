"""
Redis cache utilities.

This module provides Redis connection and caching utilities.
Note: Redis instance runs on external infrastructure server.
"""

from typing import Optional

import redis.asyncio as redis
from redis.asyncio import Redis

from app.core.config import settings

_redis_client: Optional[Redis] = None


async def get_redis() -> Optional[Redis]:
    """Get Redis client instance."""
    global _redis_client
    
    if not settings.REDIS_ENABLED:
        return None
    
    if _redis_client is None:
        try:
            _redis_client = await redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
            )
        except Exception:
            # If Redis is unavailable, log but don't fail
            # Application should work without cache
            return None
    
    return _redis_client


async def close_redis() -> None:
    """Close Redis connection."""
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None


class CacheKeys:
    """Cache key prefixes and utilities."""
    
    USER_PREFIX = "user:"
    TODO_PREFIX = "todo:"
    USER_TODOS_PREFIX = "user_todos:"
    RATE_LIMIT_PREFIX = "rate_limit:"
    
    @staticmethod
    def user_key(user_id: int) -> str:
        """Get cache key for user."""
        return f"{CacheKeys.USER_PREFIX}{user_id}"
    
    @staticmethod
    def todo_key(todo_id: int) -> str:
        """Get cache key for todo."""
        return f"{CacheKeys.TODO_PREFIX}{todo_id}"
    
    @staticmethod
    def user_todos_key(user_id: int) -> str:
        """Get cache key for user's todos list."""
        return f"{CacheKeys.USER_TODOS_PREFIX}{user_id}"
    
    @staticmethod
    def rate_limit_key(identifier: str, action: str) -> str:
        """Get cache key for rate limiting."""
        return f"{CacheKeys.RATE_LIMIT_PREFIX}{action}:{identifier}"

