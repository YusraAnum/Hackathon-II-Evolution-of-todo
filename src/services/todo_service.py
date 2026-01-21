from typing import List, Optional
from src.models.todo import Todo
from src.lib.storage import InMemoryStorage
from datetime import datetime


class TodoService:
    """
    Business logic for Todo operations.
    Implements the required functionality for creating, reading, updating, and deleting Todo items.
    """

    def __init__(self):
        self.storage = InMemoryStorage()

    def create_todo(self, description: str) -> int:
        """
        Create a new Todo item with a description and initial "incomplete" status.
        Assigns a unique identifier automatically.

        Args:
            description: The description of the todo item

        Returns:
            The unique identifier of the created todo item
        """
        todo_id = self.storage.generate_unique_id()
        todo = Todo(
            id=todo_id,
            description=description,
            status="incomplete",
            created_at=datetime.now()
        )
        self.storage.add_todo(todo)
        return todo_id

    def get_all_todos(self) -> List[Todo]:
        """
        Retrieve all Todo items in the collection.

        Returns:
            List of all Todo items
        """
        return self.storage.get_all_todos()

    def get_todo_by_id(self, todo_id: int) -> Optional[Todo]:
        """
        Retrieve a specific Todo item by its unique identifier.

        Args:
            todo_id: The unique identifier of the Todo item

        Returns:
            The Todo item if found, None otherwise
        """
        return self.storage.get_todo_by_id(todo_id)

    def update_todo(self, todo_id: int, description: Optional[str] = None, status: Optional[str] = None) -> bool:
        """
        Update a Todo item including description and completion status.

        Args:
            todo_id: The unique identifier of the Todo item to update
            description: New description (optional)
            status: New status (optional)

        Returns:
            True if successfully updated, False if ID does not exist
        """
        existing_todo = self.storage.get_todo_by_id(todo_id)
        if not existing_todo:
            return False

        # Validate status if provided
        if status is not None and status not in ["incomplete", "complete"]:
            raise ValueError(f"Status must be 'incomplete' or 'complete', got '{status}'")

        # Prepare updated values
        new_description = description if description is not None else existing_todo.description
        new_status = status if status is not None else existing_todo.status

        # Create updated todo
        updated_todo = Todo(
            id=existing_todo.id,
            description=new_description,
            status=new_status,
            created_at=existing_todo.created_at
        )

        # Attempt to update in storage
        return self.storage.update_todo(todo_id, updated_todo)

    def delete_todo(self, todo_id: int) -> bool:
        """
        Delete a Todo item by its unique identifier.

        Args:
            todo_id: The unique identifier of the Todo item to delete

        Returns:
            True if successfully deleted, False if ID does not exist
        """
        return self.storage.delete_todo(todo_id)