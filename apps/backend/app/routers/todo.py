from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from app.services.todo_service import TodoService

router = APIRouter()


@router.get("/", response_model=List[TodoResponse])
async def get_todos():
    """Get all todos"""
    service = TodoService()
    return await service.get_all_todos()


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int):
    """Get a specific todo by ID"""
    service = TodoService()
    todo = await service.get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo


@router.post("/", response_model=TodoResponse)
async def create_todo(todo: TodoCreate):
    """Create a new todo"""
    service = TodoService()
    return await service.create_todo(todo)


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, todo: TodoUpdate):
    """Update an existing todo"""
    service = TodoService()
    updated_todo = await service.update_todo(todo_id, todo)
    if not updated_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return updated_todo


@router.delete("/{todo_id}")
async def delete_todo(todo_id: int):
    """Delete a todo"""
    service = TodoService()
    deleted = await service.delete_todo(todo_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return {"message": "Todo deleted successfully"}


@router.patch("/{todo_id}/toggle_complete", response_model=TodoResponse)
async def toggle_todo_complete(todo_id: int):
    """Toggle the complete status of a todo"""
    service = TodoService()
    todo = await service.toggle_todo_complete(todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo