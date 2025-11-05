"""
Authentication service layer.

This module provides business logic for authentication operations
including user registration, login, and token management.
"""

from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import ConflictException, UnauthorizedException
from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas import LoginResponse, RegisterRequest, UserResponse


class AuthService:
    """Service for authentication operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
    
    async def register(self, request: RegisterRequest) -> UserResponse:
        """Register a new user."""
        # Check if user already exists
        if await self.user_repo.exists_by_email(request.email):
            raise ConflictException("User with this email already exists")
        
        # Hash password
        password_hash = hash_password(request.password)
        
        # Create user
        user = await self.user_repo.create(request.email, password_hash)
        
        return UserResponse.model_validate(user)
    
    async def login(self, email: str, password: str) -> LoginResponse:
        """Authenticate user and return access token."""
        # Get user by email
        user = await self.user_repo.get_by_email(email)
        
        if user is None:
            # Use generic message to prevent user enumeration
            raise UnauthorizedException("Invalid email or password")
        
        # Verify password
        if not verify_password(password, user.password_hash):
            raise UnauthorizedException("Invalid email or password")
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.id, "email": user.email},
            expires_delta=access_token_expires,
        )
        
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.model_validate(user),
        )

