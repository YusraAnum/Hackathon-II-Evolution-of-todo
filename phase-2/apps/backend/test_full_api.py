import sys
import os
import uuid
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_full_api_flow():
    print("Testing complete API flow...")

    # Generate unique emails for each test
    user1_email = f"user1_{uuid.uuid4()}@test.com"
    user2_email = f"user2_{uuid.uuid4()}@test.com"

    # Step 1: Signup user 1
    print(f"\n1. Signing up user1 ({user1_email[:10]}...)...")
    signup_response1 = client.post(
        "/api/v1/auth/signup",
        json={"email": user1_email, "password": "password123"}
    )
    assert signup_response1.status_code == 200
    user1_token = signup_response1.json()["access_token"]
    print(f"[SUCCESS] User1 signed up, got token: {user1_token[:10]}...")

    # Step 2: Signup user 2
    print(f"\n2. Signing up user2 ({user2_email[:10]}...)...")
    signup_response2 = client.post(
        "/api/v1/auth/signup",
        json={"email": user2_email, "password": "password123"}
    )
    assert signup_response2.status_code == 200
    user2_token = signup_response2.json()["access_token"]
    print(f"[SUCCESS] User2 signed up, got token: {user2_token[:10]}...")

    # Step 3: User1 creates a todo
    print("\n3. User1 creating a todo...")
    headers1 = {"Authorization": f"Bearer {user1_token}"}
    todo_response = client.post(
        "/api/v1/todos/",
        json={"title": "User 1 Todo", "description": "This belongs to user 1", "completed": False},
        headers=headers1
    )
    assert todo_response.status_code == 200
    user1_todo = todo_response.json()
    print(f"[SUCCESS] User1 created todo: {user1_todo['title']} (ID: {user1_todo['id']})")

    # Step 4: User1 gets their todos
    print("\n4. User1 getting their todos...")
    get_todos_response1 = client.get("/api/v1/todos/", headers=headers1)
    assert get_todos_response1.status_code == 200
    user1_todos = get_todos_response1.json()
    print(f"[SUCCESS] User1 has {len(user1_todos)} todos: {[t['title'] for t in user1_todos]}")

    # Step 5: User2 gets their todos (should be empty initially)
    print("\n5. User2 getting their todos...")
    headers2 = {"Authorization": f"Bearer {user2_token}"}
    get_todos_response2 = client.get("/api/v1/todos/", headers=headers2)
    assert get_todos_response2.status_code == 200
    user2_todos = get_todos_response2.json()
    print(f"[SUCCESS] User2 has {len(user2_todos)} todos: {[t['title'] for t in user2_todos]} (should be empty)")

    # Step 6: User2 creates a todo
    print("\n6. User2 creating a todo...")
    todo_response2 = client.post(
        "/api/v1/todos/",
        json={"title": "User 2 Todo", "description": "This belongs to user 2", "completed": False},
        headers=headers2
    )
    assert todo_response2.status_code == 200
    user2_todo = todo_response2.json()
    print(f"[SUCCESS] User2 created todo: {user2_todo['title']} (ID: {user2_todo['id']})")

    # Step 7: User1 should still only see their own todo
    print("\n7. User1 getting todos again (should still only see their own)...")
    get_todos_response1_after = client.get("/api/v1/todos/", headers=headers1)
    assert get_todos_response1_after.status_code == 200
    user1_todos_after = get_todos_response1_after.json()
    print(f"[SUCCESS] User1 still has {len(user1_todos_after)} todos: {[t['title'] for t in user1_todos_after]}")

    # Step 8: User2 should only see their own todo
    print("\n8. User2 getting todos again (should only see their own)...")
    get_todos_response2_after = client.get("/api/v1/todos/", headers=headers2)
    assert get_todos_response2_after.status_code == 200
    user2_todos_after = get_todos_response2_after.json()
    print(f"[SUCCESS] User2 has {len(user2_todos_after)} todos: {[t['title'] for t in user2_todos_after]}")

    # Final verification
    print("\n=== FINAL VERIFICATION ===")
    print(f"User1 has {len(user1_todos_after)} todo(s): {[t['title'] for t in user1_todos_after]}")
    print(f"User2 has {len(user2_todos_after)} todo(s): {[t['title'] for t in user2_todos_after]}")

    # Verify isolation
    assert len(user1_todos_after) == 1, f"User1 should have 1 todo, but has {len(user1_todos_after)}"
    assert len(user2_todos_after) == 1, f"User2 should have 1 todo, but has {len(user2_todos_after)}"
    assert user1_todos_after[0]['title'] == 'User 1 Todo', f"User1 should have 'User 1 Todo', but has '{user1_todos_after[0]['title']}'"
    assert user2_todos_after[0]['title'] == 'User 2 Todo', f"User2 should have 'User 2 Todo', but has '{user2_todos_after[0]['title']}'"

    print("[SUCCESS] All tests passed! User isolation is working correctly.")

if __name__ == "__main__":
    test_full_api_flow()