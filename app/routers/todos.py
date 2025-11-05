"""
Todo router.

This module handles todo-related endpoints including CRUD operations.
"""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import TodoCreate, TodoResponse, TodoUpdate
from app.services.todo_service import TodoService

router = APIRouter()


@router.get(
    "",
    response_model=List[TodoResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all todos",
    description="Retrieve all todos for the authenticated user",
)
async def get_todos(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[TodoResponse]:
    """Get all todos for the current user."""
    todo_service = TodoService(db)
    return await todo_service.get_all(current_user)


@router.get(
    "/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK,
    summary="Get todo by ID",
    description="Retrieve a specific todo by ID",
)
async def get_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TodoResponse:
    """Get a specific todo by ID."""
    todo_service = TodoService(db)
    return await todo_service.get_by_id(todo_id, current_user)


@router.post(
    "",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new todo",
    description="Create a new todo item",
)
async def create_todo(
    request: TodoCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TodoResponse:
    """Create a new todo."""
    todo_service = TodoService(db)
    return await todo_service.create(request, current_user)


@router.put(
    "/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a todo",
    description="Update an existing todo item",
)
async def update_todo(
    todo_id: int,
    request: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TodoResponse:
    """Update a todo."""
    todo_service = TodoService(db)
    return await todo_service.update(todo_id, request, current_user)


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a todo",
    description="Delete a todo item",
)
async def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a todo."""
    todo_service = TodoService(db)
    await todo_service.delete(todo_id, current_user)

