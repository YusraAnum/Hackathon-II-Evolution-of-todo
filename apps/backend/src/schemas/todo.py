"""
Todo schemas for the Todo application
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TodoBase(BaseModel):
    title: str
    completed: bool = False


class TodoCreate(TodoBase):
    description: Optional[str] = None


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TodoResponse(TodoBase):
    id: int
    user_id: int
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True