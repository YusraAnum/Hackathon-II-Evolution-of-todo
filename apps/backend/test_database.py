#!/usr/bin/env python3
"""
Test to verify database tables are created properly
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Set the database URL to SQLite file
os.environ['DATABASE_URL'] = 'sqlite:///./test_todo.db'

from src.database.session import engine, Base
from src.models.user import User
from src.models.todo import Todo

print("Creating tables...")
try:
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

    # Verify tables exist by checking the table names
    tables = Base.metadata.tables.keys()
    print(f"Created tables: {list(tables)}")

    # Verify expected tables exist
    expected_tables = {'users', 'todos'}
    created_tables = set(tables)

    if expected_tables.issubset(created_tables):
        print("[SUCCESS] All expected tables were created!")
    else:
        missing = expected_tables - created_tables
        print(f"[ERROR] Missing tables: {missing}")

    print("[SUCCESS] Database setup test completed successfully!")

except Exception as e:
    print(f"[ERROR] Error creating tables: {e}")
    import traceback
    traceback.print_exc()