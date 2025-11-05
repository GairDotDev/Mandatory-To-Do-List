"""
Authentication and authorization dependencies.

This module provides FastAPI dependencies for authentication and
getting the current user from JWT tokens.
"""

from typing import Annotated, Optional

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import UnauthorizedException
from app.core.security import decode_access_token
from app.models import User
from app.repositories.user_repository import UserRepository


async def get_current_user(
    authorization: Annotated[Optional[str], Header()] = None,
    db: AsyncSession = Depends(get_db),
) -> User:
    """Get current authenticated user from JWT token."""
    if not authorization:
        raise UnauthorizedException("Authorization header required")
    
    try:
        scheme, token = authorization.split(" ", 1)
        if scheme.lower() != "bearer":
            raise UnauthorizedException("Invalid authorization scheme")
    except ValueError:
        raise UnauthorizedException("Invalid authorization header format")
    
    try:
        payload = decode_access_token(token)
        user_id: int = payload.get("sub")
        if user_id is None:
            raise UnauthorizedException("Invalid token payload")
    except ValueError:
        raise UnauthorizedException("Invalid or expired token")
    
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    
    if user is None:
        raise UnauthorizedException("User not found")
    
    return user

