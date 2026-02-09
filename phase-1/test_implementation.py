from src.services.todo_service import TodoService


def test_basic_todo_operations():
    """
    Test basic Todo operations to verify implementation.
    This serves as a basic validation that the implementation meets the specification.
    """
    service = TodoService()

    # Test 1: Create a new todo item
    todo_id = service.create_todo("Buy groceries")
    print(f"Created todo with ID: {todo_id}")

    # Test 2: Retrieve the created todo
    todo = service.get_todo_by_id(todo_id)
    assert todo is not None
    assert todo.description == "Buy groceries"
    assert todo.status == "incomplete"
    print(f"Retrieved todo: {todo}")

    # Test 3: List all todos
    all_todos = service.get_all_todos()
    assert len(all_todos) == 1
    print(f"All todos: {all_todos}")

    # Test 4: Update the todo status to complete
    update_success = service.update_todo(todo_id, status="complete")
    assert update_success
    updated_todo = service.get_todo_by_id(todo_id)
    assert updated_todo.status == "complete"
    print(f"Updated todo status: {updated_todo}")

    # Test 5: Update the todo description
    update_success = service.update_todo(todo_id, description="Buy groceries and cook dinner")
    assert update_success
    updated_todo = service.get_todo_by_id(todo_id)
    assert updated_todo.description == "Buy groceries and cook dinner"
    print(f"Updated todo description: {updated_todo}")

    # Test 6: Delete the todo
    delete_success = service.delete_todo(todo_id)
    assert delete_success
    deleted_todo = service.get_todo_by_id(todo_id)
    assert deleted_todo is None
    print("Todo successfully deleted")

    # Test 7: Verify todo list is empty after deletion
    all_todos_after_delete = service.get_all_todos()
    assert len(all_todos_after_delete) == 0
    print(f"All todos after deletion: {all_todos_after_delete}")

    print("\nAll basic operations passed!")


if __name__ == "__main__":
    test_basic_todo_operations()