# Quick Start Guide: In-Memory Todo System (Phase 1)

## Overview

The In-Memory Todo System is a simple, backend-only system that allows you to manage todo items in memory during runtime. All data is lost when the program terminates.

## Getting Started

### Prerequisites

- Python 3.7 or higher

### Installation

No installation required - this is a pure in-memory system with no external dependencies.

### Usage Example

```python
from src.services.todo_service import TodoService

# Create a new todo service instance
service = TodoService()

# Create a new todo item
todo_id = service.create_todo("Complete project documentation")
print(f"Created todo with ID: {todo_id}")

# Retrieve a specific todo by ID
todo = service.get_todo_by_id(todo_id)
print(f"Todo: {todo}")

# List all todos
all_todos = service.get_all_todos()
print(f"All todos: {all_todos}")

# Update a todo's status
service.update_todo(todo_id, status="complete")

# Update a todo's description
service.update_todo(todo_id, description="Review and finalize project documentation")

# Delete a todo
service.delete_todo(todo_id)
```

## Available Operations

- **Create**: `create_todo(description)` - Creates a new todo with a unique ID and "incomplete" status
- **Read**: `get_todo_by_id(todo_id)` - Retrieves a specific todo by its ID
- **List**: `get_all_todos()` - Retrieves all todos in the system
- **Update**: `update_todo(todo_id, description=None, status=None)` - Updates description or status of a todo
- **Delete**: `delete_todo(todo_id)` - Removes a todo from the system

## Important Notes

- All data is stored in memory only and will be lost when the program ends
- Each todo receives a unique identifier automatically upon creation
- Status can only be "incomplete" or "complete"
- No persistence, authentication, or external interfaces are available