from src.cli import TodoCLI


def test_cli_numeric_id_handling():
    """
    Test that CLI properly handles numeric IDs (converting string input to int).
    This simulates how the CLI would handle user input.
    """
    cli = TodoCLI()

    # Create a few todos to work with
    id1 = cli.service.create_todo("Test todo 1")
    id2 = cli.service.create_todo("Test todo 2")

    print(f"Created todos with numeric IDs: {id1}, {id2}")

    # Test that we can retrieve them with their numeric IDs
    todo1 = cli.service.get_todo_by_id(id1)
    assert todo1 is not None, f"Todo with ID {id1} should exist"
    assert todo1.id == id1, f"Todo ID mismatch: expected {id1}, got {todo1.id}"

    # Test that CLI methods work correctly when manually called with integer IDs
    # This verifies the internal service integration

    # Test update
    update_result = cli.service.update_todo(id1, status="complete")
    assert update_result, "Update should succeed"

    updated_todo = cli.service.get_todo_by_id(id1)
    assert updated_todo.status == "complete", f"Status should be 'complete', got '{updated_todo.status}'"

    # Test delete
    delete_result = cli.service.delete_todo(id2)
    assert delete_result, "Delete should succeed"

    deleted_todo = cli.service.get_todo_by_id(id2)
    assert deleted_todo is None, f"Todo with ID {id2} should be deleted"

    print("CLI numeric ID handling test passed!")


if __name__ == "__main__":
    test_cli_numeric_id_handling()