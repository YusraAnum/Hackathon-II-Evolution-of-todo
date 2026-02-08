import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_signup():
    print("Testing signup via TestClient...")

    response = client.post(
        "/api/v1/auth/signup",
        json={"email": "test2@example.com", "password": "password123"}
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    if response.status_code != 200:
        print("Headers:", response.headers)
        try:
            print("JSON Response:", response.json())
        except:
            print("Could not parse JSON response")

        # Try to get more detailed error by enabling debug mode
        import traceback
        if hasattr(response, 'exception'):
            print("Exception:", response.exception)

def test_full_flow():
    print("\nTesting full flow...")

    # Test signup
    signup_response = client.post(
        "/api/v1/auth/signup",
        json={"email": "fullflow@example.com", "password": "password123"}
    )
    print(f"Signup Status: {signup_response.status_code}")
    if signup_response.status_code == 200:
        print(f"Signup Success: {signup_response.json()}")
        token_data = signup_response.json()

        # Test login with the same credentials
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "fullflow@example.com", "password": "password123"}
        )
        print(f"Login Status: {login_response.status_code}")
        if login_response.status_code == 200:
            print(f"Login Success: {login_response.json()}")

            # Test protected route
            token = token_data.get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            me_response = client.get("/api/v1/auth/me", headers=headers)
            print(f"Me endpoint Status: {me_response.status_code}")
            if me_response.status_code == 200:
                print(f"Me endpoint Success: {me_response.json()}")

if __name__ == "__main__":
    test_signup()
    test_full_flow()