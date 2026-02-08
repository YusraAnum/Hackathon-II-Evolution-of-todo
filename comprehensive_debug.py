#!/usr/bin/env python3
import sys
import os
import traceback
from pathlib import Path

print("="*60)
print("COMPREHENSIVE DEBUGGING OF TODO APP")
print("="*60)

# Add backend to path
backend_path = Path("apps/backend")
sys.path.insert(0, str(backend_path))

def check_imports():
    print("\n1. CHECKING IMPORTS...")
    try:
        from src.auth.security import hash_password, verify_password
        print("   [OK] Security imports: OK")
    except Exception as e:
        print(f"   [ERROR] Security imports failed: {e}")
        traceback.print_exc()
        return False

    try:
        from src.models.user import User
        from src.models.todo import Todo
        print("   [OK] Model imports: OK")
    except Exception as e:
        print(f"   [ERROR] Model imports failed: {e}")
        traceback.print_exc()
        return False

    try:
        from src.database.session import engine, Base, get_db
        print("   [OK] Database imports: OK")
    except Exception as e:
        print(f"   [ERROR] Database imports failed: {e}")
        traceback.print_exc()
        return False

    try:
        from src.main import app
        print("   [OK] Main app import: OK")
    except Exception as e:
        print(f"   [ERROR] Main app import failed: {e}")
        traceback.print_exc()
        return False

    return True

def check_password_functionality():
    print("\n2. CHECKING PASSWORD FUNCTIONALITY...")
    try:
        from src.auth.security import hash_password, verify_password

        test_password = "password123"
        hashed = hash_password(test_password)
        print(f"   [OK] Password hashing: OK (length: {len(hashed)})")

        is_valid = verify_password(test_password, hashed)
        print(f"   [OK] Password verification: {is_valid}")

        return is_valid
    except Exception as e:
        print(f"   [ERROR] Password functionality failed: {e}")
        traceback.print_exc()
        return False

def check_database():
    print("\n3. CHECKING DATABASE...")
    try:
        from src.database.session import engine, Base
        from src.models.user import User
        from src.models.todo import Todo

        # Create tables
        Base.metadata.create_all(bind=engine)
        print("   [OK] Database tables created: OK")

        # Check if tables exist
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"   [OK] Tables found: {tables}")

        return "users" in tables and "todos" in tables
    except Exception as e:
        print(f"   [ERROR] Database check failed: {e}")
        traceback.print_exc()
        return False

def check_auth_endpoints():
    print("\n4. CHECKING AUTH ENDPOINTS...")
    try:
        from fastapi.testclient import TestClient
        from src.main import app

        client = TestClient(app)

        # Test health endpoint
        health_response = client.get("/health")
        print(f"   [OK] Health endpoint: {health_response.status_code}")

        # Test signup
        signup_response = client.post(
            "/api/v1/auth/signup",
            json={"email": "debug_test@example.com", "password": "password123"}
        )
        print(f"   [OK] Signup endpoint: {signup_response.status_code}")

        if signup_response.status_code == 200:
            print(f"   [OK] Signup response: {list(signup_response.json().keys())}")

        # Test login
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "debug_test@example.com", "password": "password123"}
        )
        print(f"   [OK] Login endpoint: {login_response.status_code}")

        return signup_response.status_code == 200 and login_response.status_code == 200
    except Exception as e:
        print(f"   [ERROR] Auth endpoints failed: {e}")
        traceback.print_exc()
        return False

def check_frontend_files():
    print("\n5. CHECKING FRONTEND FILES...")
    frontend_path = Path("apps/frontend")

    required_files = [
        "package.json",
        "src/main.jsx",
        "src/App.jsx",
        "src/components/Login.jsx",
        "src/components/Signup.jsx",
        "src/components/Dashboard.jsx"
    ]

    all_good = True
    for file in required_files:
        file_path = frontend_path / file
        if file_path.exists():
            print(f"   [OK] {file}: EXISTS")
        else:
            print(f"   [ERROR] {file}: MISSING")
            all_good = False

    return all_good

def main():
    print("Starting comprehensive debugging...")

    results = {}

    results['imports'] = check_imports()
    results['password'] = check_password_functionality()
    results['database'] = check_database()
    results['auth'] = check_auth_endpoints()
    results['frontend'] = check_frontend_files()

    print(f"\n{'='*60}")
    print("DEBUG RESULTS SUMMARY:")
    print(f"{'='*60}")

    for check, result in results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"{check.upper()}: {status}")

    total_passed = sum(results.values())
    total_tests = len(results)

    print(f"\nOVERALL: {total_passed}/{total_tests} tests passed")

    if total_passed == total_tests:
        print("[SUCCESS] ALL SYSTEMS WORKING - READY FOR DEPLOYMENT!")
        return True
    else:
        print("[ERROR] SOME ISSUES DETECTED - NEEDS FIXING")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)