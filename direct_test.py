# Direct test of FastAPI application without running server
import sys
sys.path.insert(0, 'apps/backend')

from fastapi.testclient import TestClient
from apps.backend.src.main import app

print("Creating TestClient...")
client = TestClient(app)

print("Testing health endpoint...")
try:
    response = client.get("/health")
    print(f"Health response: {response.status_code}, {response.json()}")
except Exception as e:
    print(f"Health check failed: {e}")

print("Testing signup endpoint...")
try:
    response = client.post(
        "/api/v1/auth/signup",
        json={"email": "direct_test@example.com", "password": "password123"}
    )
    print(f"Signup response: {response.status_code}")
    if response.status_code == 200:
        print(f"Signup success: {response.json()}")
    else:
        print(f"Signup failed: {response.text}")
except Exception as e:
    print(f"Signup test failed: {e}")
    import traceback
    traceback.print_exc()

print("Testing login endpoint...")
try:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "direct_test@example.com", "password": "password123"}
    )
    print(f"Login response: {response.status_code}")
    if response.status_code == 200:
        print(f"Login success: {response.json()}")
    else:
        print(f"Login failed: {response.text}")
except Exception as e:
    print(f"Login test failed: {e}")
    import traceback
    traceback.print_exc()