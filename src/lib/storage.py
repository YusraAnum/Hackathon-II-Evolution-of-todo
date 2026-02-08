from typing import Dict, List, Optional
from src.models.todo import Todo


class InMemoryStorage:
    """
    In-memory storage mechanism for Todo items.
    Implements unique identifier generation and storage operations.
    """

    def __init__(self):
        self._todos: Dict[int, Todo] = {}
        self._next_id = 1

    def generate_unique_id(self) -> int:
        """
        Generate a unique numeric identifier for Todo items.
        """
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def add_todo(self, todo: Todo) -> bool:
        """
        Add a Todo item to storage.

        Args:
            todo: The Todo item to add

        Returns:
            True if successfully added, False if ID already exists
        """
        if todo.id in self._todos:
            return False

        self._todos[todo.id] = todo
        return True

    def get_todo_by_id(self, todo_id: int) -> Optional[Todo]:
        """
        Retrieve a specific Todo item by its unique identifier.

        Args:
            todo_id: The unique identifier of the Todo item

        Returns:
            The Todo item if found, None otherwise
        """
        return self._todos.get(todo_id)

    def get_all_todos(self) -> List[Todo]:
        """
        Retrieve all Todo items from storage.

        Returns:
            List of all Todo items
        """
        return list(self._todos.values())

    def update_todo(self, todo_id: int, updated_todo: Todo) -> bool:
        """
        Update an existing Todo item.

        Args:
            todo_id: The unique identifier of the Todo item to update
            updated_todo: The updated Todo item

        Returns:
            True if successfully updated, False if ID does not exist
        """
        if todo_id not in self._todos:
            return False

        self._todos[todo_id] = updated_todo
        return True

    def delete_todo(self, todo_id: int) -> bool:
        """
        Delete a Todo item by its unique identifier.

        Args:
            todo_id: The unique identifier of the Todo item to delete

        Returns:
            True if successfully deleted, False if ID does not exist
        """
        if todo_id not in self._todos:
            return False

        del self._todos[todo_id]
        return True