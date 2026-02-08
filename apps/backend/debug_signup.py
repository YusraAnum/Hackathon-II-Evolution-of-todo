import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Import the signup function directly to test
from src.api.auth import signup
from src.database.session import get_db, SessionLocal
from src.schemas.auth import UserCreate
from sqlalchemy.orm import Session

def test_signup():
    print("Testing signup function directly...")

    # Create test user data
    user_data = UserCreate(email="test@example.com", password="testpass123")

    # Get database session
    db: Session = next(get_db())

    try:
        result = signup(user_data, db)
        print(f"Signup result: {result}")
    except Exception as e:
        print(f"Signup error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_signup()