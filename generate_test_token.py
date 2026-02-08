import jwt
import os
from datetime import datetime, timedelta
import uuid

# Use the same secret as the backend
SECRET_KEY = "supersecretkeyfordevelopment"
ALGORITHM = "HS256"

# Generate a user ID
user_id = str(uuid.uuid4())
print(f"Generated user ID: {user_id}")

# Create a JWT token with user information
token_data = {
    "sub": user_id,  # User ID
    "name": "Test User",
    "email": "test@example.com",
    "exp": datetime.utcnow() + timedelta(days=30)  # Valid for 30 days
}

token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
print(f"Generated JWT token: {token}")
print("\nTo use this token:")
print("1. Copy the token above")
print("2. Open your browser's developer tools (F12)")
print("3. Go to the Console tab")
print("4. Run: localStorage.setItem('auth_token', 'YOUR_TOKEN_HERE')")
print("5. Refresh the page - you should now be logged in as a test user")
print("\nAlternatively, you can set this token in your browser's localStorage directly")