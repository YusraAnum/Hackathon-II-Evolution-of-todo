import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# Simple test to see what's happening
print("Testing single signup...")

response = client.post(
    "/api/v1/auth/signup",
    json={"email": "simple@test.com", "password": "password123"}
)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
try:
    print(f"JSON Response: {response.json()}")
except:
    print("Could not parse as JSON")

# Let's also test the health endpoint
health_response = client.get("/health")
print(f"Health Status: {health_response.status_code}")
print(f"Health Response: {health_response.text}")