"""
Rate limiting middleware.

This module implements rate limiting using Redis to prevent abuse.
"""

from typing import Optional

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.cache import CacheKeys, get_redis
from app.core.config import settings
from app.core.exceptions import RateLimitException


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting requests."""
    
    async def dispatch(self, request: Request, call_next):
        """Apply rate limiting to request."""
        if not settings.RATE_LIMIT_ENABLED:
            return await call_next(request)
        
        # Skip rate limiting for health checks
        if request.url.path in ["/healthz", "/readyz"]:
            return await call_next(request)
        
        # Get identifier (IP address or user ID)
        identifier = request.client.host if request.client else "unknown"
        
        # Try to get user ID from token if available
        user_id = None
        auth_header = request.headers.get("authorization")
        if auth_header:
            try:
                from app.core.security import decode_access_token
                scheme, token = auth_header.split(" ", 1)
                if scheme.lower() == "bearer":
                    payload = decode_access_token(token)
                    user_id = payload.get("sub")
            except Exception:
                pass
        
        # Use user ID if available, otherwise use IP
        identifier = str(user_id) if user_id else identifier
        
        # Determine action type
        action = self._get_action(request.url.path, request.method)
        
        if action:
            # Check rate limit
            if await self._check_rate_limit(identifier, action):
                raise RateLimitException(
                    message="Rate limit exceeded",
                    details={"retry_after": 60},
                )
        
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_PER_MINUTE)
        
        return response
    
    def _get_action(self, path: str, method: str) -> Optional[str]:
        """Determine action type for rate limiting."""
        if path == "/api/v1/auth/login" and method == "POST":
            return "login"
        elif path == "/api/v1/auth/register" and method == "POST":
            return "register"
        elif path.startswith("/api/v1/"):
            return "api"
        return None
    
    async def _check_rate_limit(self, identifier: str, action: str) -> bool:
        """Check if rate limit is exceeded."""
        redis_client = await get_redis()
        
        if not redis_client:
            # If Redis is unavailable, don't rate limit
            return False
        
        try:
            cache_key = CacheKeys.rate_limit_key(identifier, action)
            
            # Determine limit and window based on action
            if action == "login":
                limit = settings.RATE_LIMIT_LOGIN_ATTEMPTS
                window = settings.RATE_LIMIT_LOGIN_WINDOW_MINUTES * 60
            elif action == "register":
                limit = settings.RATE_LIMIT_REGISTRATION_ATTEMPTS
                window = settings.RATE_LIMIT_REGISTRATION_WINDOW_HOURS * 3600
            else:
                limit = settings.RATE_LIMIT_PER_MINUTE
                window = 60
            
            # Get current count
            current = await redis_client.get(cache_key)
            count = int(current) if current else 0
            
            if count >= limit:
                return True
            
            # Increment count
            await redis_client.incr(cache_key)
            await redis_client.expire(cache_key, window)
            
            return False
        except Exception:
            # If Redis fails, allow request (fail open)
            return False

