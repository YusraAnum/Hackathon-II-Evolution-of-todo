import React, { useState, useEffect, useContext } from 'react';
import { ApiContext } from '../App';

function Dashboard() {
  const { user, logout } = useContext(ApiContext);
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState({ title: '', description: '' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [editingText, setEditingText] = useState('');

  // Fetch todos on component mount
  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://127.0.0.1:8000/api/v1/todos/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json',
        }
      });

      if (response.ok) {
        const data = await response.json();
        setTodos(data);
      } else {
        setError('Failed to fetch todos');
      }
    } catch (err) {
      setError('An error occurred while fetching todos');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTodo = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/todos/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          title: newTodo.title,
          description: newTodo.description,
          completed: false
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setTodos([...todos, data]);
        setNewTodo({ title: '', description: '' });
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to add todo');
      }
    } catch (err) {
      setError('An error occurred while adding todo');
    }
  };

  const toggleTodoCompletion = async (id) => {
    const todo = todos.find(t => t.id === id);

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/v1/todos/${id}/toggle`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
      });

      if (response.ok) {
        const updatedTodo = await response.json();
        setTodos(todos.map(t => t.id === id ? updatedTodo : t));
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to update todo');
      }
    } catch (err) {
      setError('An error occurred while updating todo');
    }
  };

  const deleteTodo = async (id) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/v1/todos/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        setTodos(todos.filter(t => t.id !== id));
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to delete todo');
      }
    } catch (err) {
      setError('An error occurred while deleting todo');
    }
  };

  const startEditing = (todo) => {
    setEditingId(todo.id);
    setEditingText(todo.title);
  };

  const saveEdit = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/v1/todos/${editingId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          title: editingText,
          completed: todos.find(t => t.id === editingId)?.completed
        }),
      });

      if (response.ok) {
        const updatedTodo = await response.json();
        setTodos(todos.map(t => t.id === editingId ? updatedTodo : t));
        setEditingId(null);
        setEditingText('');
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to update todo');
      }
    } catch (err) {
      setError('An error occurred while updating todo');
    }
  };

  const cancelEdit = () => {
    setEditingId(null);
    setEditingText('');
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Todo Dashboard</h1>
        <div className="user-info">
          <span>Welcome, {user?.email}</span>
          <button onClick={logout} className="logout-btn">Logout</button>
        </div>
      </header>

      <main className="dashboard-main">
        {error && <div className="error-message">{error}</div>}

        {/* Add Todo Form */}
        <form onSubmit={handleAddTodo} className="add-todo-form">
          <h2>Add New Todo</h2>
          <div className="form-group">
            <input
              type="text"
              placeholder="Todo title..."
              value={newTodo.title}
              onChange={(e) => setNewTodo({...newTodo, title: e.target.value})}
              required
            />
          </div>
          <div className="form-group">
            <textarea
              placeholder="Description (optional)..."
              value={newTodo.description}
              onChange={(e) => setNewTodo({...newTodo, description: e.target.value})}
            />
          </div>
          <button type="submit">Add Todo</button>
        </form>

        {/* Loading indicator */}
        {loading && <div className="loading">Loading todos...</div>}

        {/* Todos List */}
        {!loading && (
          <div className="todos-list">
            <h2>Your Todos ({todos.length})</h2>
            {todos.length === 0 ? (
              <p>No todos yet. Add one above!</p>
            ) : (
              <ul className="todo-items">
                {todos.map(todo => (
                  <li key={todo.id} className={`todo-item ${todo.completed ? 'completed' : ''}`}>
                    {editingId === todo.id ? (
                      <div className="edit-form">
                        <input
                          type="text"
                          value={editingText}
                          onChange={(e) => setEditingText(e.target.value)}
                          autoFocus
                        />
                        <button onClick={saveEdit}>Save</button>
                        <button onClick={cancelEdit} className="cancel-btn">Cancel</button>
                      </div>
                    ) : (
                      <>
                        <div className="todo-content">
                          <input
                            type="checkbox"
                            checked={todo.completed}
                            onChange={() => toggleTodoCompletion(todo.id)}
                          />
                          <span className="todo-text">{todo.title}</span>
                          {todo.description && (
                            <small className="todo-description">{todo.description}</small>
                          )}
                        </div>
                        <div className="todo-actions">
                          <button onClick={() => startEditing(todo)}>Edit</button>
                          <button onClick={() => deleteTodo(todo.id)} className="delete-btn">
                            Delete
                          </button>
                        </div>
                      </>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default Dashboard;