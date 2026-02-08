import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test the auth module imports
from src.api.auth import signup, login
from src.database.session import get_db
from src.schemas.auth import UserCreate, UserLogin
from src.models.user import User
from sqlalchemy.orm import Session

def test_auth_functions():
    print("Testing auth functions directly...")

    # Test creating user data
    user_create = UserCreate(email="test@example.com", password="password123")
    print(f"UserCreate object: {user_create}")

    # Get db session
    db_gen = get_db()
    db = next(db_gen)
    print(f"DB session obtained: {type(db)}")

    try:
        # Try to create a user directly without the FastAPI wrapper
        from src.auth.security import hash_password

        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_create.email).first()
        if existing_user:
            db.delete(existing_user)
            db.commit()

        # Create new user
        hashed_pw = hash_password(user_create.password)
        print(f"Password hashed successfully: {type(hashed_pw)}")

        user = User(email=user_create.email, password_hash=hashed_pw)
        db.add(user)
        db.commit()
        db.refresh(user)

        print(f"User created successfully: {user.email}, ID: {user.id}")

        # Test login
        user_login = UserLogin(email=user_create.email, password=user_create.password)
        print(f"UserLogin object: {user_login}")

        # Query user for login
        db_user = db.query(User).filter(User.email == user_login.email).first()
        print(f"Found user for login: {db_user.email if db_user else 'None'}")

        from src.auth.security import verify_password
        is_valid = verify_password(user_login.password, db_user.password_hash)
        print(f"Password verification: {is_valid}")

    except Exception as e:
        print(f"Error in auth test: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_auth_functions()