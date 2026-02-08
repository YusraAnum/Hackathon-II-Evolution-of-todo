import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Import the login function directly to test
from src.api.auth import login
from src.database.session import SessionLocal
from src.schemas.auth import UserLogin

def test_login():
    print("Testing login function directly...")

    # Create test user data
    user_data = UserLogin(email="test@example.com", password="testpass123")

    # Get database session
    db = SessionLocal()

    try:
        result = login(user_data, db)
        print(f"Login result: {result}")
    except Exception as e:
        print(f"Login error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_login()