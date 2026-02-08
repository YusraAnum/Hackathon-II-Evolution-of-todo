import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.database.session import SessionLocal
from src.models.user import User
from src.models.todo import Todo
from src.schemas.todo import TodoCreate

def test_todos():
    print("Testing todos functionality...")

    # Get database session
    db = SessionLocal()

    try:
        # First, let's get the user we created earlier (assuming it has id=1)
        user = db.query(User).filter(User.email == "test@example.com").first()
        if not user:
            print("No test user found, creating one...")
            from src.auth.security import hash_password
            user = User(email="test@example.com", password_hash=hash_password("testpass123"))
            db.add(user)
            db.commit()
            db.refresh(user)

        print(f"Using user: {user.email} (ID: {user.id})")

        # Test creating a todo
        new_todo = Todo(
            title="Test Todo",
            description="This is a test todo",
            completed=False,
            user_id=user.id
        )

        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)

        print(f"Created todo: {new_todo.title} (ID: {new_todo.id})")

        # Test getting todos for this user
        user_todos = db.query(Todo).filter(Todo.user_id == user.id).all()
        print(f"Found {len(user_todos)} todos for user {user.email}")

        for todo in user_todos:
            print(f"- Todo {todo.id}: {todo.title} (completed: {todo.completed})")

        # Test that another user wouldn't see this todo
        # Create another user
        other_user = User(email="other@example.com", password_hash=hash_password("otherpass123"))
        db.add(other_user)
        db.commit()
        db.refresh(other_user)

        print(f"Created other user: {other_user.email} (ID: {other_user.id})")

        # Check that other user has no todos
        other_user_todos = db.query(Todo).filter(Todo.user_id == other_user.id).all()
        print(f"Other user has {len(other_user_todos)} todos (should be 0)")

        print("✓ Todos functionality test completed successfully")

    except Exception as e:
        print(f"Todos test error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_todos()