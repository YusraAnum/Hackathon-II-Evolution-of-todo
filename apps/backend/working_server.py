#!/usr/bin/env python3
"""
Simple working server for Todo App - guaranteed to work
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sqlite3
import hashlib
import jwt
import datetime
import json
from contextlib import contextmanager

# Configuration
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"

app = FastAPI(
    title="Todo API - Working Version",
    description="A working version of the Todo API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_FILE = "working_todo.db"

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create todos table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN DEFAULT 0,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    """Hash password using SHA256 (for demo purposes, use bcrypt in production)"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return hash_password(plain_password) == hashed_password

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """Decode JWT access token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
        return int(user_id)
    except jwt.JWTError:
        return None

# Pydantic models
class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# Initialize database
init_db()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "working-todo-api"}

@app.post("/api/v1/auth/signup")
async def signup(user_data: UserCreate):
    """User signup endpoint"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    try:
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (user_data.email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return {"detail": "Email already registered"}

        # Hash password and create user
        password_hash = hash_password(user_data.password)
        cursor.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (user_data.email, password_hash)
        )
        user_id = cursor.lastrowid

        conn.commit()
        conn.close()

        # Create access token
        access_token = create_access_token(data={"sub": str(user_id)})

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except Exception as e:
        conn.close()
        return {"detail": f"Signup failed: {str(e)}"}

@app.post("/api/v1/auth/login")
async def login(user_data: UserLogin):
    """User login endpoint"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    try:
        # Find user
        cursor.execute(
            "SELECT id, password_hash FROM users WHERE email = ?",
            (user_data.email,)
        )
        row = cursor.fetchone()

        if not row:
            conn.close()
            return {"detail": "Incorrect email or password"}

        user_id, stored_hash = row

        # Verify password
        if not verify_password(user_data.password, stored_hash):
            conn.close()
            return {"detail": "Incorrect email or password"}

        conn.close()

        # Create access token
        access_token = create_access_token(data={"sub": str(user_id)})

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except Exception as e:
        conn.close()
        return {"detail": f"Login failed: {str(e)}"}

@app.get("/api/v1/auth/me")
async def get_current_user(authorization: str = None):
    """Get current user info"""
    if not authorization or not authorization.startswith("Bearer "):
        return {"detail": "Authorization header missing or invalid"}

    token = authorization.split(" ")[1]
    user_id = decode_access_token(token)

    if user_id is None:
        return {"detail": "Could not validate credentials"}

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id, email, created_at FROM users WHERE id = ?",
            (user_id,)
        )
        row = cursor.fetchone()

        if not row:
            conn.close()
            return {"detail": "User not found"}

        user_data = {
            "id": row[0],
            "email": row[1],
            "created_at": row[2]
        }

        conn.close()
        return user_data

    except Exception as e:
        conn.close()
        return {"detail": f"Error fetching user: {str(e)}"}

@app.get("/api/v1/todos/")
async def get_todos(authorization: str = None):
    """Get user's todos"""
    if not authorization or not authorization.startswith("Bearer "):
        return {"detail": "Authorization header missing or invalid"}

    token = authorization.split(" ")[1]
    user_id = decode_access_token(token)

    if user_id is None:
        return {"detail": "Could not validate credentials"}

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id, title, description, completed, created_at FROM todos WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
        rows = cursor.fetchall()

        todos = []
        for row in rows:
            todos.append({
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "completed": bool(row[3]),
                "created_at": row[4]
            })

        conn.close()
        return todos

    except Exception as e:
        conn.close()
        return {"detail": f"Error fetching todos: {str(e)}"}

@app.post("/api/v1/todos/")
async def create_todo(todo_data: TodoCreate, authorization: str = None):
    """Create a new todo"""
    if not authorization or not authorization.startswith("Bearer "):
        return {"detail": "Authorization header missing or invalid"}

    token = authorization.split(" ")[1]
    user_id = decode_access_token(token)

    if user_id is None:
        return {"detail": "Could not validate credentials"}

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO todos (title, description, completed, user_id) VALUES (?, ?, ?, ?)",
            (todo_data.title, todo_data.description, todo_data.completed, user_id)
        )
        todo_id = cursor.lastrowid

        conn.commit()
        conn.close()

        # Return the created todo
        return {
            "id": todo_id,
            "title": todo_data.title,
            "description": todo_data.description,
            "completed": todo_data.completed,
            "user_id": user_id,
            "created_at": datetime.datetime.utcnow().isoformat()
        }

    except Exception as e:
        conn.close()
        return {"detail": f"Error creating todo: {str(e)}"}

@app.get("/api/v1/todos/{todo_id}")
async def get_todo(todo_id: int, authorization: str = None):
    """Get a specific todo"""
    if not authorization or not authorization.startswith("Bearer "):
        return {"detail": "Authorization header missing or invalid"}

    token = authorization.split(" ")[1]
    user_id = decode_access_token(token)

    if user_id is None:
        return {"detail": "Could not validate credentials"}

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id, title, description, completed, created_at FROM todos WHERE id = ? AND user_id = ?",
            (todo_id, user_id)
        )
        row = cursor.fetchone()

        if not row:
            conn.close()
            return {"detail": "Todo not found"}

        todo = {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "completed": bool(row[3]),
            "created_at": row[4]
        }

        conn.close()
        return todo

    except Exception as e:
        conn.close()
        return {"detail": f"Error fetching todo: {str(e)}"}

@app.put("/api/v1/todos/{todo_id}")
async def update_todo(todo_id: int, todo_data: TodoUpdate, authorization: str = None):
    """Update a specific todo"""
    if not authorization or not authorization.startswith("Bearer "):
        return {"detail": "Authorization header missing or invalid"}

    token = authorization.split(" ")[1]
    user_id = decode_access_token(token)

    if user_id is None:
        return {"detail": "Could not validate credentials"}

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    try:
        # Check if todo exists and belongs to user
        cursor.execute(
            "SELECT id FROM todos WHERE id = ? AND user_id = ?",
            (todo_id, user_id)
        )
        if not cursor.fetchone():
            conn.close()
            return {"detail": "Todo not found"}

        # Build update query dynamically
        updates = []
        params = []

        if todo_data.title is not None:
            updates.append("title = ?")
            params.append(todo_data.title)
        if todo_data.description is not None:
            updates.append("description = ?")
            params.append(todo_data.description)
        if todo_data.completed is not None:
            updates.append("completed = ?")
            params.append(int(todo_data.completed))

        if updates:
            query = f"UPDATE todos SET {', '.join(updates)} WHERE id = ? AND user_id = ?"
            params.extend([todo_id, user_id])

            cursor.execute(query, params)
            conn.commit()

        # Return updated todo
        cursor.execute(
            "SELECT id, title, description, completed, created_at FROM todos WHERE id = ? AND user_id = ?",
            (todo_id, user_id)
        )
        row = cursor.fetchone()

        conn.close()

        if row:
            return {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "completed": bool(row[3]),
                "created_at": row[4]
            }
        else:
            return {"detail": "Todo not found after update"}

    except Exception as e:
        conn.close()
        return {"detail": f"Error updating todo: {str(e)}"}

@app.delete("/api/v1/todos/{todo_id}")
async def delete_todo(todo_id: int, authorization: str = None):
    """Delete a specific todo"""
    if not authorization or not authorization.startswith("Bearer "):
        return {"detail": "Authorization header missing or invalid"}

    token = authorization.split(" ")[1]
    user_id = decode_access_token(token)

    if user_id is None:
        return {"detail": "Could not validate credentials"}

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    try:
        # Check if todo exists and belongs to user
        cursor.execute(
            "SELECT id FROM todos WHERE id = ? AND user_id = ?",
            (todo_id, user_id)
        )
        if not cursor.fetchone():
            conn.close()
            return {"detail": "Todo not found"}

        # Delete the todo
        cursor.execute("DELETE FROM todos WHERE id = ? AND user_id = ?", (todo_id, user_id))
        conn.commit()
        conn.close()

        return {"message": "Todo deleted successfully"}

    except Exception as e:
        conn.close()
        return {"detail": f"Error deleting todo: {str(e)}"}

if __name__ == "__main__":
    print("Starting Working Todo API Server...")
    print("Listening on http://127.0.0.1:8000")
    print("Database: working_todo.db")
    print("CORS: Enabled for all origins")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")