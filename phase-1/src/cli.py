from src.services.todo_service import TodoService
from typing import Optional


class TodoCLI:
    """
    Command Line Interface for the In-Memory Todo System.
    Provides a simple text menu for managing todos.
    """

    def __init__(self):
        self.service = TodoService()

    def display_menu(self):
        """Display the main menu options."""
        print("\n--- Todo CLI Menu ---")
        print("1. Add todo")
        print("2. List todos")
        print("3. View todo by ID")
        print("4. Update todo description")
        print("5. Delete todo")
        print("6. Mark complete/incomplete")
        print("7. Exit")
        print("--------------------")

    def add_todo(self):
        """Add a new todo item."""
        description = input("Enter todo description: ").strip()
        if description:
            todo_id = self.service.create_todo(description)
            print(f"Todo created with ID: {todo_id}")
        else:
            print("Description cannot be empty.")

    def list_todos(self):
        """List all todo items."""
        todos = self.service.get_all_todos()
        if not todos:
            print("No todos found.")
            return

        print(f"\nFound {len(todos)} todo(s):")
        for todo in todos:
            status_icon = "✓" if todo.status == "complete" else "○"
            print(f"ID: {todo.id} | {status_icon} {todo.description} [{todo.status}]")

    def view_todo(self):
        """View a specific todo by ID."""
        todo_id_str = input("Enter todo ID: ").strip()
        if not todo_id_str:
            print("ID cannot be empty.")
            return

        try:
            todo_id = int(todo_id_str)
        except ValueError:
            print(f"Invalid ID format: {todo_id_str}. Please enter a numeric ID.")
            return

        todo = self.service.get_todo_by_id(todo_id)
        if todo:
            status_icon = "✓" if todo.status == "complete" else "○"
            print(f"\nID: {todo.id}")
            print(f"Description: {todo.description}")
            print(f"Status: {todo.status} {status_icon}")
            print(f"Created: {todo.created_at}")
        else:
            print(f"No todo found with ID: {todo_id}")

    def update_todo(self):
        """Update a todo's description."""
        todo_id_str = input("Enter todo ID: ").strip()
        if not todo_id_str:
            print("ID cannot be empty.")
            return

        try:
            todo_id = int(todo_id_str)
        except ValueError:
            print(f"Invalid ID format: {todo_id_str}. Please enter a numeric ID.")
            return

        # Check if todo exists
        existing_todo = self.service.get_todo_by_id(todo_id)
        if not existing_todo:
            print(f"No todo found with ID: {todo_id}")
            return

        new_description = input(f"Enter new description (current: {existing_todo.description}): ").strip()
        if new_description:
            success = self.service.update_todo(todo_id, description=new_description)
            if success:
                print("Todo updated successfully.")
            else:
                print("Failed to update todo.")
        else:
            print("Description cannot be empty.")

    def delete_todo(self):
        """Delete a todo by ID."""
        todo_id_str = input("Enter todo ID to delete: ").strip()
        if not todo_id_str:
            print("ID cannot be empty.")
            return

        try:
            todo_id = int(todo_id_str)
        except ValueError:
            print(f"Invalid ID format: {todo_id_str}. Please enter a numeric ID.")
            return

        success = self.service.delete_todo(todo_id)
        if success:
            print("Todo deleted successfully.")
        else:
            print(f"No todo found with ID: {todo_id}")

    def mark_complete_incomplete(self):
        """Toggle a todo's completion status."""
        todo_id_str = input("Enter todo ID: ").strip()
        if not todo_id_str:
            print("ID cannot be empty.")
            return

        try:
            todo_id = int(todo_id_str)
        except ValueError:
            print(f"Invalid ID format: {todo_id_str}. Please enter a numeric ID.")
            return

        # Check if todo exists
        existing_todo = self.service.get_todo_by_id(todo_id)
        if not existing_todo:
            print(f"No todo found with ID: {todo_id}")
            return

        # Toggle status
        new_status = "incomplete" if existing_todo.status == "complete" else "complete"
        success = self.service.update_todo(todo_id, status=new_status)
        if success:
            print(f"Todo marked as {new_status}.")
        else:
            print("Failed to update todo status.")

    def run(self):
        """Run the CLI application."""
        print("Welcome to the In-Memory Todo CLI!")
        print("Note: All data is stored in memory only and will be lost when the program exits.")

        while True:
            self.display_menu()
            choice = input("Select an option (1-7): ").strip()

            if choice == "1":
                self.add_todo()
            elif choice == "2":
                self.list_todos()
            elif choice == "3":
                self.view_todo()
            elif choice == "4":
                self.update_todo()
            elif choice == "5":
                self.delete_todo()
            elif choice == "6":
                self.mark_complete_incomplete()
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please select 1-7.")