from src.services.todo_service import TodoService


def test_numeric_ids():
    """
    Test that the system now uses numeric IDs instead of UUIDs.
    """
    service = TodoService()

    # Create a few todos and verify they get numeric IDs starting from 1
    id1 = service.create_todo("First todo")
    id2 = service.create_todo("Second todo")
    id3 = service.create_todo("Third todo")

    print(f"Created todos with IDs: {id1}, {id2}, {id3}")

    # Verify IDs are integers and sequential
    assert isinstance(id1, int), f"ID should be int, got {type(id1)}"
    assert isinstance(id2, int), f"ID should be int, got {type(id2)}"
    assert isinstance(id3, int), f"ID should be int, got {type(id3)}"

    assert id1 == 1, f"First ID should be 1, got {id1}"
    assert id2 == 2, f"Second ID should be 2, got {id2}"
    assert id3 == 3, f"Third ID should be 3, got {id3}"

    # Verify we can retrieve todos by their numeric IDs
    todo1 = service.get_todo_by_id(id1)
    assert todo1 is not None, "Todo 1 should exist"
    assert todo1.id == id1, f"Todo ID mismatch: expected {id1}, got {todo1.id}"
    assert todo1.description == "First todo", f"Description mismatch: expected 'First todo', got '{todo1.description}'"

    # Test update with numeric ID
    update_result = service.update_todo(id1, description="Updated first todo")
    assert update_result, "Update should succeed"

    updated_todo1 = service.get_todo_by_id(id1)
    assert updated_todo1.description == "Updated first todo", f"Updated description mismatch: expected 'Updated first todo', got '{updated_todo1.description}'"

    # Test delete with numeric ID
    delete_result = service.delete_todo(id2)
    assert delete_result, "Delete should succeed"

    deleted_todo = service.get_todo_by_id(id2)
    assert deleted_todo is None, "Todo 2 should be deleted"

    # Verify remaining todos
    all_todos = service.get_all_todos()
    remaining_ids = [todo.id for todo in all_todos]
    assert id1 in remaining_ids, "Todo 1 should still exist"
    assert id2 not in remaining_ids, "Todo 2 should be deleted"
    assert id3 in remaining_ids, "Todo 3 should still exist"

    print("All numeric ID tests passed!")


if __name__ == "__main__":
    test_numeric_ids()