from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from models import Todo, User
from database import get_db
from auth import get_current_user

router = APIRouter(prefix="/api/v1/todos", tags=["todos"])

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

@router.post("/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Create new todo linked to current user
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        user_id=current_user.id
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    return db_todo

@router.get("/", response_model=List[TodoResponse])
def get_todos(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get only todos belonging to current user
    todos = db.query(Todo).filter(Todo.user_id == current_user.id).order_by(Todo.created_at.desc()).all()
    return todos

@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get specific todo belonging to current user
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo_update: TodoUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Update specific todo belonging to current user
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Update fields if provided
    if todo_update.title is not None:
        todo.title = todo_update.title
    if todo_update.description is not None:
        todo.description = todo_update.description
    if todo_update.completed is not None:
        todo.completed = todo_update.completed

    db.commit()
    db.refresh(todo)
    return todo

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Delete specific todo belonging to current user
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}