#!/usr/bin/env python3
"""
API Backend - Clean API-only version without UI
"""
from flask import Flask, request, jsonify
import sqlite3
import hashlib
import jwt
import datetime
import os
from functools import wraps
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SECRET_KEY'] = 'simple_secret_key_for_demo'

# Database setup
DATABASE = 'todo_api.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
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

def hash_password(password):
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hash_val):
    """Verify password against hash"""
    return hash_password(password) == hash_val

def create_token(user_id):
    """Create JWT token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except:
        return None

def token_required(f):
    """Decorator for routes requiring authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        if token.startswith('Bearer '):
            token = token[7:]

        user_id = verify_token(token)
        if not user_id:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(user_id, *args, **kwargs)
    return decorated

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password required'}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        # Check if user exists
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            return jsonify({'message': 'Email already registered'}), 400

        # Create user
        password_hash = hash_password(password)
        cursor.execute('INSERT INTO users (email, password_hash) VALUES (?, ?)', (email, password_hash))
        user_id = cursor.lastrowid
        conn.commit()

        # Generate token
        token = create_token(user_id)

        return jsonify({'message': 'User created successfully', 'token': token}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password required'}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        # Find user
        cursor.execute('SELECT id, password_hash FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()

        if not row or not verify_password(password, row[1]):
            return jsonify({'message': 'Invalid email or password'}), 401

        user_id = row[0]
        token = create_token(user_id)

        return jsonify({'message': 'Login successful', 'token': token}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/me', methods=['GET'])
@token_required
def get_user(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT id, email, created_at FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()

        if not row:
            return jsonify({'message': 'User not found'}), 404

        user_data = {
            'id': row[0],
            'email': row[1],
            'created_at': row[2]
        }

        return jsonify(user_data), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/todos', methods=['GET'])
@token_required
def get_todos(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT id, title, description, completed, created_at
            FROM todos
            WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (user_id,))

        rows = cursor.fetchall()
        todos = []
        for row in rows:
            todos.append({
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'completed': bool(row[3]),
                'created_at': row[4]
            })

        return jsonify(todos), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/todos', methods=['POST'])
@token_required
def create_todo(user_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')

    if not title:
        return jsonify({'message': 'Title is required'}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO todos (title, description, user_id)
            VALUES (?, ?, ?)
        ''', (title, description, user_id))

        todo_id = cursor.lastrowid
        conn.commit()

        # Return the created todo
        cursor.execute('SELECT id, title, description, completed, created_at FROM todos WHERE id = ?', (todo_id,))
        row = cursor.fetchone()

        created_todo = {
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'completed': bool(row[3]),
            'created_at': row[4]
        }

        return jsonify(created_todo), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
@token_required
def update_todo(user_id, todo_id):
    data = request.get_json()
    completed = data.get('completed')
    title = data.get('title')
    description = data.get('description')

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        # Check if todo exists and belongs to user
        cursor.execute('SELECT id FROM todos WHERE id = ? AND user_id = ?', (todo_id, user_id))
        if not cursor.fetchone():
            return jsonify({'message': 'Todo not found or not owned by user'}), 404

        # Build update query dynamically
        updates = []
        params = []

        if completed is not None:
            updates.append('completed = ?')
            params.append(completed)
        if title is not None:
            updates.append('title = ?')
            params.append(title)
        if description is not None:
            updates.append('description = ?')
            params.append(description)

        if not updates:
            return jsonify({'message': 'At least one field to update is required'}), 400

        query = f"UPDATE todos SET {', '.join(updates)} WHERE id = ? AND user_id = ?"
        params.extend([todo_id, user_id])

        cursor.execute(query, params)
        conn.commit()

        # Return updated todo
        cursor.execute('SELECT id, title, description, completed, created_at FROM todos WHERE id = ?', (todo_id,))
        row = cursor.fetchone()

        if row:
            updated_todo = {
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'completed': bool(row[3]),
                'created_at': row[4]
            }
            return jsonify(updated_todo), 200
        else:
            return jsonify({'message': 'Todo updated but could not retrieve updated record'}), 500

    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
@token_required
def delete_todo(user_id, todo_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            DELETE FROM todos
            WHERE id = ? AND user_id = ?
        ''', (todo_id, user_id))

        if cursor.rowcount == 0:
            return jsonify({'message': 'Todo not found or not owned by user'}), 404

        conn.commit()
        return jsonify({'message': 'Todo deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    print("Starting API Backend Server...")
    print("API available at: http://127.0.0.1:8080")
    print("This serves only API endpoints, no UI")
    app.run(host='127.0.0.1', port=8080, debug=True)