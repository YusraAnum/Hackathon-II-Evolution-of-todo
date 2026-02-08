import jwt
import os
import uuid
import requests
from datetime import datetime, timedelta

# Set up the secret key (same as in the app)
SECRET_KEY = "supersecretkeyfordevelopment"
ALGORITHM = "HS256"

# Generate a user ID
user_id = str(uuid.uuid4())
print(f"Generated user ID: {user_id}")

# Create a JWT token with the user ID as the subject
token_data = {
    "sub": user_id,  # The user ID should be in the 'sub' claim
    "exp": datetime.utcnow() + timedelta(hours=1)
}
token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

print(f"Generated token: {token}")

# Test the chat endpoint
url = f"http://localhost:8000/api/{user_id}/chat"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
data = {
    "message": "Add a task to buy groceries"
}

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
except Exception as e:
    print(f"Error making request: {e}")