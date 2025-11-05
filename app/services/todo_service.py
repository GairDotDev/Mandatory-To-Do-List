"""
Todo service layer.

This module provides business logic for todo operations including
CRUD operations with caching support.
"""

from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.cache import CacheKeys, get_redis
from app.core.exceptions import NotFoundException
from app.models import Todo, User
from app.repositories.todo_repository import TodoRepository
from app.schemas import TodoCreate, TodoResponse, TodoUpdate


class TodoService:
    """Service for todo operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.todo_repo = TodoRepository(db)
    
    async def get_all(self, user: User) -> List[TodoResponse]:
        """Get all todos for a user with caching."""
        redis_client = await get_redis()
        cache_key = CacheKeys.user_todos_key(user.id)
        
        # Try cache first
        if redis_client:
            try:
                cached = await redis_client.get(cache_key)
                if cached:
                    # In production, use proper deserialization
                    # For now, bypass cache and fetch from DB
                    pass
            except Exception:
                # Cache error shouldn't break the app
                pass
        
        # Fetch from database
        todos = await self.todo_repo.get_all_by_user(user.id)
        
        # Cache result
        if redis_client:
            try:
                # In production, serialize properly
                # For now, cache with short TTL
                await redis_client.setex(cache_key, 60, "cached")
            except Exception:
                pass
        
        return [TodoResponse.model_validate(todo) for todo in todos]
    
    async def get_by_id(self, todo_id: int, user: User) -> TodoResponse:
        """Get a todo by ID."""
        redis_client = await get_redis()
        cache_key = CacheKeys.todo_key(todo_id)
        
        # Try cache first
        if redis_client:
            try:
                cached = await redis_client.get(cache_key)
                if cached:
                    # In production, use proper deserialization
                    pass
            except Exception:
                pass
        
        todo = await self.todo_repo.get_by_id(todo_id, user.id)
        
        if todo is None:
            raise NotFoundException("Todo not found")
        
        # Cache result
        if redis_client:
            try:
                await redis_client.setex(cache_key, 300, "cached")
            except Exception:
                pass
        
        return TodoResponse.model_validate(todo)
    
    async def create(self, request: TodoCreate, user: User) -> TodoResponse:
        """Create a new todo."""
        todo = await self.todo_repo.create(user.id, request.title, request.description)
        
        # Invalidate user's todos cache
        redis_client = await get_redis()
        if redis_client:
            try:
                cache_key = CacheKeys.user_todos_key(user.id)
                await redis_client.delete(cache_key)
            except Exception:
                pass
        
        return TodoResponse.model_validate(todo)
    
    async def update(self, todo_id: int, request: TodoUpdate, user: User) -> TodoResponse:
        """Update a todo."""
        todo = await self.todo_repo.get_by_id(todo_id, user.id)
        
        if todo is None:
            raise NotFoundException("Todo not found")
        
        # Update fields
        await self.todo_repo.update(
            todo,
            title=request.title,
            description=request.description,
            completed=request.completed,
        )
        
        # Invalidate caches
        redis_client = await get_redis()
        if redis_client:
            try:
                await redis_client.delete(CacheKeys.todo_key(todo_id))
                await redis_client.delete(CacheKeys.user_todos_key(user.id))
            except Exception:
                pass
        
        return TodoResponse.model_validate(todo)
    
    async def delete(self, todo_id: int, user: User) -> None:
        """Delete a todo."""
        todo = await self.todo_repo.get_by_id(todo_id, user.id)
        
        if todo is None:
            raise NotFoundException("Todo not found")
        
        await self.todo_repo.delete(todo)
        
        # Invalidate caches
        redis_client = await get_redis()
        if redis_client:
            try:
                await redis_client.delete(CacheKeys.todo_key(todo_id))
                await redis_client.delete(CacheKeys.user_todos_key(user.id))
            except Exception:
                pass

