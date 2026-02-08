#!/usr/bin/env python3
"""
Simple Todo App - Standalone version that will definitely work
"""
from flask import Flask, request, jsonify, render_template_string
import sqlite3
import hashlib
import jwt
import datetime
import os
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'simple_secret_key_for_demo'

# Database setup
DATABASE = 'simple_todo.db'

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

@app.route('/')
def index():
    """Serve the main page"""
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple Todo App</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            input, button { padding: 10px; margin: 5px; border: 1px solid #ddd; border-radius: 4px; }
            button { background: #007bff; color: white; cursor: pointer; }
            button:hover { background: #0056b3; }
            .todo-item { padding: 10px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
            .completed { text-decoration: line-through; color: #888; }
            .error { color: red; margin: 10px 0; }
            .success { color: green; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Simple Todo App</h1>

            <!-- Login/Signup Section -->
            <div id="auth-section">
                <h2>Login</h2>
                <div id="login-error" class="error"></div>
                <input type="email" id="login-email" placeholder="Email">
                <input type="password" id="login-password" placeholder="Password">
                <button onclick="login()">Login</button>

                <h3>Don't have an account?</h3>
                <div id="signup-error" class="error"></div>
                <input type="email" id="signup-email" placeholder="Email">
                <input type="password" id="signup-password" placeholder="Password">
                <button onclick="signup()">Sign Up</button>
            </div>

            <!-- Todo Section (hidden until logged in) -->
            <div id="todo-section" style="display:none;">
                <h2>Todo List</h2>
                <div id="todo-success" class="success"></div>
                <div id="todo-error" class="error"></div>

                <div style="margin-bottom: 20px;">
                    <h3>Add New Todo</h3>
                    <input type="text" id="todo-title" placeholder="Todo title" style="width: 70%;">
                    <input type="text" id="todo-desc" placeholder="Description (optional)" style="width: 70%; margin-top: 5px;">
                    <button onclick="addTodo()" style="width: 30%; margin-top: 5px;">Add Todo</button>
                </div>

                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <h3>Your Todos</h3>
                    <button onclick="loadTodos()" style="background: #28a745;">Refresh</button>
                </div>

                <div id="todos-list"></div>

                <div id="todo-stats" style="margin-top: 20px; padding: 10px; background: #f8f9fa; border-radius: 4px;"></div>
            </div>
        </div>

        <script>
            let authToken = localStorage.getItem('authToken');

            // Check if user is already logged in
            if (authToken) {
                document.getElementById('auth-section').style.display = 'none';
                document.getElementById('todo-section').style.display = 'block';
                loadTodos();
            }

            function showError(elementId, message) {
                document.getElementById(elementId).innerText = message;
            }

            function showSuccess(message) {
                document.getElementById('todo-success').innerText = message;
                setTimeout(() => document.getElementById('todo-success').innerText = '', 3000);
            }

            function clearErrors() {
                document.querySelectorAll('.error').forEach(el => el.innerText = '');
                document.getElementById('todo-success').innerText = '';
            }

            async function signup() {
                clearErrors();
                const email = document.getElementById('signup-email').value;
                const password = document.getElementById('signup-password').value;

                if (!email || !password) {
                    showError('signup-error', 'Please fill in all fields');
                    return;
                }

                try {
                    const response = await fetch('/api/signup', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ email, password })
                    });

                    const data = await response.json();

                    if (response.ok) {
                        localStorage.setItem('authToken', data.token);
                        authToken = data.token;
                        document.getElementById('auth-section').style.display = 'none';
                        document.getElementById('todo-section').style.display = 'block';
                        loadTodos();
                    } else {
                        showError('signup-error', data.message || 'Signup failed');
                    }
                } catch (error) {
                    showError('signup-error', 'Network error');
                }
            }

            async function login() {
                clearErrors();
                const email = document.getElementById('login-email').value;
                const password = document.getElementById('login-password').value;

                if (!email || !password) {
                    showError('login-error', 'Please fill in all fields');
                    return;
                }

                try {
                    const response = await fetch('/api/login', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ email, password })
                    });

                    const data = await response.json();

                    if (response.ok) {
                        localStorage.setItem('authToken', data.token);
                        authToken = data.token;
                        document.getElementById('auth-section').style.display = 'none';
                        document.getElementById('todo-section').style.display = 'block';
                        loadTodos();
                    } else {
                        showError('login-error', data.message || 'Login failed');
                    }
                } catch (error) {
                    showError('login-error', 'Network error');
                }
            }

            function logout() {
                localStorage.removeItem('authToken');
                authToken = null;
                document.getElementById('auth-section').style.display = 'block';
                document.getElementById('todo-section').style.display = 'none';
                document.getElementById('signup-email').value = '';
                document.getElementById('signup-password').value = '';
                document.getElementById('login-email').value = '';
                document.getElementById('login-password').value = '';
            }

            async function addTodo() {
                clearErrors();
                const title = document.getElementById('todo-title').value;
                const desc = document.getElementById('todo-desc').value;

                if (!title) {
                    showError('todo-error', 'Please enter a title');
                    return;
                }

                try {
                    const response = await fetch('/api/todos', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + authToken
                        },
                        body: JSON.stringify({ title, description: desc })
                    });

                    const data = await response.json();

                    if (response.ok) {
                        document.getElementById('todo-title').value = '';
                        document.getElementById('todo-desc').value = '';
                        showSuccess('Todo added successfully');
                        loadTodos();
                    } else {
                        showError('todo-error', data.message || 'Failed to add todo');
                    }
                } catch (error) {
                    showError('todo-error', 'Network error');
                }
            }

            async function loadTodos() {
                try {
                    const response = await fetch('/api/todos', {
                        headers: {
                            'Authorization': 'Bearer ' + authToken
                        }
                    });

                    const todos = await response.json();

                    if (response.ok) {
                        const todosList = document.getElementById('todos-list');
                        todosList.innerHTML = '';

                        if (todos.length === 0) {
                            todosList.innerHTML = '<p style="text-align: center; color: #666;">No todos yet. Add one above!</p>';
                        } else {
                            todos.forEach(todo => {
                                const todoDiv = document.createElement('div');
                                todoDiv.className = 'todo-item';

                                let editFormHTML = '';
                                if (window.editingId === todo.id) {
                                    editFormHTML = `
                                        <div style="display: flex; flex-direction: column; gap: 5px;">
                                            <input type="text" id="edit-title-${todo.id}" value="${todo.title}" style="width: 100%; margin-bottom: 5px;">
                                            <textarea id="edit-desc-${todo.id}" style="width: 100%; margin-bottom: 5px;">${todo.description || ''}</textarea>
                                            <div>
                                                <button onclick="saveEdit(${todo.id})" style="background: #28a745; margin-right: 5px;">Save</button>
                                                <button onclick="cancelEdit()" style="background: #6c757d;">Cancel</button>
                                            </div>
                                        </div>
                                    `;
                                }

                                todoDiv.innerHTML = `
                                    <div style="flex: 1;">
                                        <div style="display: flex; align-items: center; margin-bottom: 5px;">
                                            <input type="checkbox" ${todo.completed ? 'checked' : ''} onchange="toggleTodo(${todo.id}, this.checked)" style="margin-right: 10px;">
                                            <span class="${todo.completed ? 'completed' : ''}" style="flex: 1;">${todo.title}</span>
                                        </div>
                                        ${todo.description ? '<div style="margin-left: 26px; color: #666; font-style: italic;">' + todo.description + '</div>' : ''}
                                    </div>
                                    <div>
                                        ${editFormHTML}
                                        ${window.editingId !== todo.id ?
                                            `<button onclick="startEdit(${todo.id}, '${todo.title}', '${todo.description || ''}')" style="background: #ffc107; color: #000; margin-right: 5px;">Edit</button>
                                             <button onclick="deleteTodo(${todo.id})" style="background: #dc3545;">Delete</button>` : ''}
                                    </div>
                                `;
                                todosList.appendChild(todoDiv);
                            });
                        }

                        // Calculate and show stats
                        const total = todos.length;
                        const completed = todos.filter(t => t.completed).length;
                        const pending = total - completed;

                        document.getElementById('todo-stats').innerHTML = `
                            <strong>Todos Stats:</strong>
                            Total: ${total} |
                            Completed: ${completed} |
                            Pending: ${pending}
                        `;
                    }
                } catch (error) {
                    showError('todo-error', 'Failed to load todos');
                }
            }

            let editingId = null;
            let editingTitle = '';
            let editingDesc = '';

            function startEdit(id, title, desc) {
                editingId = id;
                editingTitle = title;
                editingDesc = desc;
                loadTodos(); // Refresh to show edit form
            }

            function cancelEdit() {
                editingId = null;
                editingTitle = '';
                editingDesc = '';
                loadTodos(); // Refresh to hide edit form
            }

            async function saveEdit(id) {
                const newTitle = document.getElementById(`edit-title-${id}`).value;
                const newDesc = document.getElementById(`edit-desc-${id}`).value;

                if (!newTitle.trim()) {
                    alert('Title cannot be empty');
                    return;
                }

                try {
                    const response = await fetch('/api/todos/' + id, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + authToken
                        },
                        body: JSON.stringify({
                            title: newTitle,
                            description: newDesc
                        })
                    });

                    if (response.ok) {
                        editingId = null;
                        loadTodos(); // Refresh after saving
                        showSuccess('Todo updated successfully');
                    } else {
                        const data = await response.json();
                        alert(data.message || 'Failed to update todo');
                    }
                } catch (error) {
                    alert('Network error while updating todo');
                }
            }


            async function deleteTodo(id) {
                if (!confirm('Are you sure you want to delete this todo?')) return;

                try {
                    const response = await fetch('/api/todos/' + id, {
                        method: 'DELETE',
                        headers: {
                            'Authorization': 'Bearer ' + authToken
                        }
                    });

                    if (response.ok) {
                        loadTodos();
                        showSuccess('Todo deleted successfully');
                    } else {
                        const data = await response.json();
                        alert(data.message || 'Failed to delete todo');
                    }
                } catch (error) {
                    alert('Network error');
                }
            }

            async function addTodo() {
                clearErrors();
                const title = document.getElementById('todo-title').value.trim();
                const desc = document.getElementById('todo-desc').value.trim();

                if (!title) {
                    showError('todo-error', 'Please enter a title');
                    return;
                }

                try {
                    const response = await fetch('/api/todos', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + authToken
                        },
                        body: JSON.stringify({ title, description: desc })
                    });

                    const data = await response.json();

                    if (response.ok) {
                        document.getElementById('todo-title').value = '';
                        document.getElementById('todo-desc').value = '';
                        showSuccess('Todo added successfully');
                        loadTodos();
                    } else {
                        showError('todo-error', data.message || 'Failed to add todo');
                    }
                } catch (error) {
                    showError('todo-error', 'Network error');
                }
            }

            async function toggleTodo(id, completed) {
                try {
                    const response = await fetch('/api/todos/' + id, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + authToken
                        },
                        body: JSON.stringify({ completed })
                    });

                    if (!response.ok) {
                        loadTodos(); // Reload to revert the checkbox
                    }
                } catch (error) {
                    loadTodos(); // Reload to revert the checkbox
                }
            }

            async function deleteTodo(id) {
                if (!confirm('Are you sure you want to delete this todo?')) return;

                try {
                    const response = await fetch('/api/todos/' + id, {
                        method: 'DELETE',
                        headers: {
                            'Authorization': 'Bearer ' + authToken
                        }
                    });

                    if (response.ok) {
                        loadTodos();
                    } else {
                        alert('Failed to delete todo');
                    }
                } catch (error) {
                    alert('Network error');
                }
            }
        </script>
    </body>
    </html>
    '''
    return render_template_string(html)

# API Routes
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

        return jsonify({
            'id': todo_id,
            'title': title,
            'description': description,
            'completed': False,
            'user_id': user_id
        }), 200
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
        return jsonify({'message': 'Todo updated successfully'}), 200

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
    print("Starting Simple Todo App Server...")
    print("Access at: http://127.0.0.1:5000")
    print("This will definitely work!")
    app.run(host='127.0.0.1', port=5000, debug=True)