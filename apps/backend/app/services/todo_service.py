import asyncio
from typing import List, Optional
from datetime import datetime

from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse


class TodoService:
    def __init__(self):
        # Initialize with some sample data for demonstration
        self.todos = []
        self.next_id = 1

    async def get_all_todos(self) -> List[TodoResponse]:
        """Get all todos"""
        return [TodoResponse.from_orm(todo) for todo in self.todos]

    async def get_todo_by_id(self, todo_id: int) -> Optional[TodoResponse]:
        """Get a specific todo by ID"""
        for todo in self.todos:
            if todo.id == todo_id:
                return TodoResponse.from_orm(todo)
        return None

    async def create_todo(self, todo_create: TodoCreate) -> TodoResponse:
        """Create a new todo"""
        new_todo = Todo(
            id=self.next_id,
            title=todo_create.title,
            description=todo_create.description,
            completed=False,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.todos.append(new_todo)
        self.next_id += 1
        return TodoResponse.from_orm(new_todo)

    async def update_todo(self, todo_id: int, todo_update: TodoUpdate) -> Optional[TodoResponse]:
        """Update an existing todo"""
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                updated_data = todo_update.dict(exclude_unset=True)
                for field, value in updated_data.items():
                    setattr(self.todos[i], field, value)
                self.todos[i].updated_at = datetime.now()
                return TodoResponse.from_orm(self.todos[i])
        return None

    async def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo"""
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                del self.todos[i]
                return True
        return False

    async def toggle_todo_complete(self, todo_id: int) -> Optional[TodoResponse]:
        """Toggle the complete status of a todo"""
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                self.todos[i].completed = not self.todos[i].completed
                self.todos[i].updated_at = datetime.now()
                return TodoResponse.from_orm(self.todos[i])
        return None