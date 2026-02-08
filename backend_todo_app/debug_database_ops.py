import sys
import os
sys.path.insert(0, './backend_todo_app')
os.chdir('./backend_todo_app')

from database import engine, Base
from models import User
from auth import create_access_token
from passlib.context import CryptContext
from sqlalchemy.orm import sessionmaker

# Create the database tables
Base.metadata.create_all(bind=engine)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    print("Testing signup functionality step by step...")

    # Test 1: Check if user already exists
    existing_user = db.query(User).filter((User.username == "testuser") | (User.email == "test@example.com")).first()
    print(f"Existing user check: {existing_user}")

    if not existing_user:
        # Test 2: Password hashing
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b")
        
        def hash_password(password: str) -> str:
            truncated_password = password[:72] if len(password) > 72 else password
            return pwd_context.hash(truncated_password)

        password_hash = hash_password("testpass")
        print(f"Password hashed successfully: {password_hash[:20]}...")

        # Test 3: Create new user
        user = User(username="testuser", email="test@example.com", password_hash=password_hash)
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"User created successfully with ID: {user.id}")

        # Test 4: Create access token
        access_token = create_access_token(data={"sub": str(user.id)})
        print(f"Access token created: {access_token[:20]}...")

        # Clean up
        db.delete(user)
        db.commit()
        print("Cleanup successful")
    else:
        print("User already exists, skipping creation")
        
finally:
    db.close()
    print("Database session closed")

print("All tests passed!")