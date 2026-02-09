import os
import sys
sys.path.insert(0, '.')

from database import engine, Base
from models import User
from auth import create_access_token
from passlib.context import CryptContext

# Create the database tables
Base.metadata.create_all(bind=engine)

# Test the signup functionality step by step
print("Testing signup functionality...")

# Test password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

password_hash = hash_password("testpassword")
print(f"Password hashed successfully: {password_hash[:20]}...")

# Test token creation
access_token = create_access_token(data={"sub": "1"})
print(f"Token created successfully: {access_token[:20]}...")

# Test database connection
from sqlalchemy.orm import Session

db = Session(bind=engine)

# Check if user already exists
existing_user = db.query(User).filter((User.username == "testuser") | (User.email == "test@example.com")).first()
if existing_user:
    print("User already exists, deleting for test...")
    db.delete(existing_user)
    db.commit()

# Create new user
user = User(username="testuser", email="test@example.com", password_hash=password_hash)
db.add(user)
db.commit()
db.refresh(user)

print(f"User created successfully with ID: {user.id}")

# Clean up
db.delete(user)
db.commit()
db.close()

print("All signup functionality tests passed!")