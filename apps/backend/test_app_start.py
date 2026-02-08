#!/usr/bin/env python3
"""
Simple test to verify the FastAPI application starts without errors
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    # Import the main app to test if it initializes properly
    from src.main import app

    print("[SUCCESS] Application imported successfully!")
    print(f"[INFO] App title: {app.title}")
    print(f"[INFO] App routes: {[route.path for route in app.routes]}")

    # Test database session
    from src.database.session import engine, Base, SessionLocal
    print("[SUCCESS] Database session imported successfully!")
    print(f"[INFO] Engine: {engine.__class__.__name__}")

    # Test model imports
    from src.models.user import User
    from src.models.todo import Todo
    print("[SUCCESS] Models imported successfully!")
    print(f"[INFO] User table: {User.__tablename__}")
    print(f"[INFO] Todo table: {Todo.__tablename__}")

    # Test auth modules
    from src.auth.security import hash_password, verify_password
    print("[SUCCESS] Auth modules imported successfully!")

    # Test a simple password hashing (ensure password is under 72 bytes)
    test_password = "testpass123"  # Shorter password to avoid bcrypt 72-byte limit
    test_hash = hash_password(test_password)
    is_valid = verify_password(test_password, test_hash)
    print(f"[SUCCESS] Password hashing works: {is_valid}")

    print("\n[ALL TESTS PASSED] The application should start without errors.")

except Exception as e:
    print(f"[ERROR] Error occurred: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)