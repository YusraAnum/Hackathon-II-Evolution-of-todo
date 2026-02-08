from src.services.todo_service import TodoService
from src.models.todo import Todo


def test_comprehensive_functionality():
    """
    Comprehensive test to verify all functionality meets specification requirements.
    """
    service = TodoService()

    print("=== Testing User Story 1: Basic Todo Management ===")

    # Test 1: Given an empty todo list, When a new todo item is created,
    # Then the item should appear in the list with a unique identifier and status "incomplete"
    todo_id_1 = service.create_todo("First todo item")
    all_todos = service.get_all_todos()
    assert len(all_todos) == 1
    assert all_todos[0].id == todo_id_1
    assert all_todos[0].status == "incomplete"
    print("PASS: Test 1 passed: Created todo has unique ID and 'incomplete' status")

    # Test 2: Given a list with todo items, When the list operation is called,
    # Then all items should be returned with their identifiers, descriptions, and statuses
    todo_id_2 = service.create_todo("Second todo item")
    all_todos = service.get_all_todos()
    assert len(all_todos) == 2
    ids = [todo.id for todo in all_todos]
    assert todo_id_1 in ids
    assert todo_id_2 in ids
    print("PASS: Test 2 passed: List operation returns all items with identifiers, descriptions, and statuses")

    # Test 3: Given a list with todo items, When an item is updated,
    # Then the changes should be reflected when the list is retrieved again
    service.update_todo(todo_id_1, description="Updated first todo")
    updated_todo = service.get_todo_by_id(todo_id_1)
    assert updated_todo.description == "Updated first todo"
    print("PASS: Test 3 passed: Update operation reflects changes")

    # Test 4: Given a list with todo items, When an item is deleted,
    # Then it should no longer appear in the list
    service.delete_todo(todo_id_1)
    all_todos_after_delete = service.get_all_todos()
    assert len(all_todos_after_delete) == 1
    remaining_ids = [todo.id for todo in all_todos_after_delete]
    assert todo_id_1 not in remaining_ids
    assert todo_id_2 in remaining_ids
    print("PASS: Test 4 passed: Delete operation removes item from list")

    print("\n=== Testing User Story 2: Todo Item Lifecycle ===")

    # Test 5: Given a todo item with status "incomplete", When the update operation sets status to "complete",
    # Then the item should reflect the "complete" status
    todo_id_3 = service.create_todo("Todo for lifecycle test")
    service.update_todo(todo_id_3, status="complete")
    updated_todo = service.get_todo_by_id(todo_id_3)
    assert updated_todo.status == "complete"
    print("PASS: Test 5 passed: Status can be changed from 'incomplete' to 'complete'")

    # Test 6: Given a todo item with status "complete", When the update operation sets status to "incomplete",
    # Then the item should reflect the "incomplete" status
    service.update_todo(todo_id_3, status="incomplete")
    updated_todo = service.get_todo_by_id(todo_id_3)
    assert updated_todo.status == "incomplete"
    print("PASS: Test 6 passed: Status can be changed from 'complete' to 'incomplete'")

    print("\n=== Testing User Story 3: Todo Item Details Management ===")

    # Test 7: Given a todo item with a specific description, When the update operation modifies the description,
    # Then the new description should be returned when retrieving the item
    original_description = "Original description"
    new_description = "Modified description"
    todo_id_4 = service.create_todo(original_description)
    service.update_todo(todo_id_4, description=new_description)
    updated_todo = service.get_todo_by_id(todo_id_4)
    assert updated_todo.description == new_description
    print("PASS: Test 7 passed: Description can be modified")

    # Test 8: Given a todo item, When an attempt is made to update a non-existent item,
    # Then the system should return an appropriate error response (in our case, False)
    result = service.update_todo("non-existent-id", description="This should fail")
    assert result is False
    print("PASS: Test 8 passed: Update operation returns False for non-existent items")

    print("\n=== Testing Error Handling & Validation ===")

    # Test 9: Attempting to create a Todo with invalid status should raise an error
    try:
        invalid_todo = Todo(id="test", description="test", status="invalid", created_at=None)
        assert False, "Should have raised ValueError for invalid status"
    except ValueError as e:
        assert "Status must be 'incomplete' or 'complete'" in str(e)
        print("PASS: Test 9 passed: Invalid status raises ValueError")

    # Test 10: Attempting to update with invalid status should raise an error
    todo_id_5 = service.create_todo("Test invalid status update")
    try:
        service.update_todo(todo_id_5, status="invalid_status")
        assert False, "Should have raised ValueError for invalid status update"
    except ValueError as e:
        assert "Status must be 'incomplete' or 'complete'" in str(e)
        print("PASS: Test 10 passed: Invalid status update raises ValueError")

    print("\n=== All Acceptance Scenarios Passed! ===")


if __name__ == "__main__":
    test_comprehensive_functionality()