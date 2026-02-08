"""
Todos API routes for the Todo application
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..models.user import User
from ..models.todo import Todo
from ..schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from ..auth.dependencies import get_current_user
from ..database.session import get_db

router = APIRouter()


@router.get("/", response_model=list[TodoResponse])
def get_todos(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve all todos for the authenticated user.
    """
    todos = db.query(Todo).filter(Todo.user_id == current_user.id).all()
    return todos


@router.get("/{id}", response_model=TodoResponse)
def get_todo(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific todo by ID.
    """
    todo = db.query(Todo).filter(
        Todo.id == id,
        Todo.user_id == current_user.id
    ).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return todo


@router.post("/", response_model=TodoResponse)
def create_todo(
    todo_data: TodoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new todo for the authenticated user.
    """
    todo = Todo(
        title=todo_data.title,
        description=getattr(todo_data, 'description', None),  # Handle optional description
        completed=getattr(todo_data, 'completed', False),    # Handle optional completed field
        user_id=current_user.id
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.put("/{id}", response_model=TodoResponse)
def update_todo(
    id: int,
    todo_data: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing todo.
    """
    todo = db.query(Todo).filter(
        Todo.id == id,
        Todo.user_id == current_user.id
    ).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Update fields if provided
    if todo_data.title is not None:
        todo.title = todo_data.title
    if hasattr(todo_data, 'description') and todo_data.description is not None:
        todo.description = todo_data.description
    if todo_data.completed is not None:
        todo.completed = todo_data.completed

    db.commit()
    db.refresh(todo)
    return todo


@router.patch("/{id}/toggle", response_model=TodoResponse)
def toggle_todo_completion(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Toggle the completed status of a todo.
    """
    todo = db.query(Todo).filter(
        Todo.id == id,
        Todo.user_id == current_user.id
    ).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Toggle completion status
    todo.completed = not todo.completed
    db.commit()
    db.refresh(todo)
    return todo


@router.delete("/{id}")
def delete_todo(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a specific todo.
    """
    todo = db.query(Todo).filter(
        Todo.id == id,
        Todo.user_id == current_user.id
    ).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}