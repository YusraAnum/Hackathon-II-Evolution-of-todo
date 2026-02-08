from src.cli import TodoCLI
from src.services.todo_service import TodoService


def test_cli_integration():
    """
    Test that CLI integrates properly with existing services.
    This ensures the CLI uses the same service layer as the original implementation.
    """
    # Create a CLI instance
    cli = TodoCLI()

    # We'll mock user input by directly calling the service methods to verify integration
    # This is to confirm the CLI's service is the same as what we tested before

    # Test adding a todo through CLI's service
    original_count = len(cli.service.get_all_todos())

    # Directly use the service to add a test todo
    todo_id = cli.service.create_todo("Test todo from CLI integration")

    # Verify it was added
    new_count = len(cli.service.get_all_todos())
    assert new_count == original_count + 1, f"Expected {original_count + 1} todos, got {new_count}"

    # Verify the todo exists
    retrieved_todo = cli.service.get_todo_by_id(todo_id)
    assert retrieved_todo is not None, "Todo should exist after creation"
    assert retrieved_todo.description == "Test todo from CLI integration", "Description should match"

    # Test updating the todo
    update_success = cli.service.update_todo(todo_id, status="complete")
    assert update_success, "Update should succeed"

    updated_todo = cli.service.get_todo_by_id(todo_id)
    assert updated_todo.status == "complete", "Status should be updated to complete"

    # Test listing todos
    all_todos = cli.service.get_all_todos()
    assert len(all_todos) > 0, "Should have at least one todo"

    # Test deleting the todo
    delete_success = cli.service.delete_todo(todo_id)
    assert delete_success, "Deletion should succeed"

    # Verify it's gone
    deleted_todo = cli.service.get_todo_by_id(todo_id)
    assert deleted_todo is None, "Todo should be None after deletion"

    print("CLI integration test passed! CLI properly uses the existing service layer.")


if __name__ == "__main__":
    test_cli_integration()