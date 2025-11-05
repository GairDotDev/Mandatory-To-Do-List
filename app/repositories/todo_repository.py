"""
Todo repository for database operations.

This module provides data access layer for todo-related operations.
"""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Todo


class TodoRepository:
    """Repository for todo database operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, todo_id: int, user_id: int) -> Optional[Todo]:
        """Get todo by ID, ensuring it belongs to the user."""
        result = await self.db.execute(
            select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all_by_user(self, user_id: int) -> List[Todo]:
        """Get all todos for a user."""
        result = await self.db.execute(
            select(Todo)
            .where(Todo.user_id == user_id)
            .order_by(Todo.created_at.desc())
        )
        return list(result.scalars().all())
    
    async def create(self, user_id: int, title: str, description: Optional[str] = None) -> Todo:
        """Create a new todo."""
        todo = Todo(user_id=user_id, title=title, description=description)
        self.db.add(todo)
        await self.db.flush()
        await self.db.refresh(todo)
        return todo
    
    async def update(
        self,
        todo: Todo,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> Todo:
        """Update a todo."""
        if title is not None:
            todo.title = title
        if description is not None:
            todo.description = description
        if completed is not None:
            todo.completed = completed
        
        await self.db.flush()
        await self.db.refresh(todo)
        return todo
    
    async def delete(self, todo: Todo) -> None:
        """Delete a todo."""
        await self.db.delete(todo)
        await self.db.flush()

