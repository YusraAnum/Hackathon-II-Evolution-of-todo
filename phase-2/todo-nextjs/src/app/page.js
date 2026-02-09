'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'

export default function Home() {
  const [currentPage, setCurrentPage] = useState('login') // 'login', 'signup', 'dashboard'
  const [user, setUser] = useState(null)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  // Todo state
  const [todos, setTodos] = useState([])
  const [newTodo, setNewTodo] = useState({ title: '', description: '' })
  const [loading, setLoading] = useState(false)
  const [editingTodo, setEditingTodo] = useState(null)

  // Set API base URL - using relative path to leverage Next.js rewrites
  const API_BASE = ''

  // Check if user is already logged in
  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      // Verify token and get user info
      axios.get(`${API_BASE}/api/me`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(response => {
        setUser(response.data)
        setCurrentPage('dashboard')
        loadTodos()
      })
      .catch(() => {
        localStorage.removeItem('token')
      })
    }
  }, [])

  const handleSignup = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await axios.post(`${API_BASE}/api/signup`, {
        email,
        password
      })

      const { token } = response.data
      localStorage.setItem('token', token)

      // Get user info
      const userResponse = await axios.get(`${API_BASE}/api/me`, {
        headers: { Authorization: `Bearer ${token}` }
      })

      setUser(userResponse.data)
      setCurrentPage('dashboard')
      setSuccess('Account created successfully!')
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError(err.response?.data?.message || 'Signup failed')
    } finally {
      setLoading(false)
    }
  }

  const handleLogin = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await axios.post(`${API_BASE}/api/login`, {
        email,
        password
      })

      const { token } = response.data
      localStorage.setItem('token', token)

      // Get user info
      const userResponse = await axios.get(`${API_BASE}/api/me`, {
        headers: { Authorization: `Bearer ${token}` }
      })

      setUser(userResponse.data)
      setCurrentPage('dashboard')
      setSuccess('Login successful!')
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError(err.response?.data?.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  const loadTodos = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${API_BASE}/api/todos`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setTodos(response.data)
    } catch (err) {
      setError('Failed to load todos')
    }
  }

  const addTodo = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const token = localStorage.getItem('token')
      const response = await axios.post(`${API_BASE}/api/todos`, newTodo, {
        headers: { Authorization: `Bearer ${token}` }
      })

      setTodos([response.data, ...todos])
      setNewTodo({ title: '', description: '' })
      setSuccess('Todo added successfully!')
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to add todo')
    } finally {
      setLoading(false)
    }
  }

  const updateTodo = async (id, updates) => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.put(`${API_BASE}/api/todos/${id}`, updates, {
        headers: { Authorization: `Bearer ${token}` }
      })

      setTodos(todos.map(todo =>
        todo.id === id ? { ...todo, ...updates } : todo
      ))
      setEditingTodo(null)
      setSuccess('Todo updated successfully!')
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to update todo')
    }
  }

  const toggleTodoCompletion = async (id, completed) => {
    try {
      const token = localStorage.getItem('token')
      await axios.put(`${API_BASE}/api/todos/${id}`, { completed }, {
        headers: { Authorization: `Bearer ${token}` }
      })

      setTodos(todos.map(todo =>
        todo.id === id ? { ...todo, completed } : todo
      ))
    } catch (err) {
      setError('Failed to update todo')
    }
  }

  const deleteTodo = async (id) => {
    if (!window.confirm('Are you sure you want to delete this todo?')) return

    try {
      const token = localStorage.getItem('token')
      await axios.delete(`${API_BASE}/api/todos/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      })

      setTodos(todos.filter(todo => todo.id !== id))
      setSuccess('Todo deleted successfully!')
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to delete todo')
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    setUser(null)
    setCurrentPage('login')
    setTodos([])
  }

  const startEditing = (todo) => {
    setEditingTodo(todo)
  }

  const cancelEditing = () => {
    setEditingTodo(null)
  }

  const calculateStats = () => {
    const total = todos.length
    const completed = todos.filter(todo => todo.completed).length
    const pending = total - completed
    return { total, completed, pending }
  }

  const { total, completed, pending } = calculateStats()

  if (currentPage === 'login') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-md">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800">Todo App</h1>
            <p className="text-gray-600 mt-2">Sign in to your account</p>
          </div>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}

          {success && (
            <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
              {success}
            </div>
          )}

          <form onSubmit={handleLogin}>
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-medium mb-2" htmlFor="email">
                Email
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="your@email.com"
                required
              />
            </div>

            <div className="mb-6">
              <label className="block text-gray-700 text-sm font-medium mb-2" htmlFor="password">
                Password
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="••••••••"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-lg transition duration-200 disabled:opacity-50"
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-gray-600">
              Don't have an account?{' '}
              <button
                onClick={() => setCurrentPage('signup')}
                className="text-blue-600 hover:text-blue-800 font-medium"
              >
                Sign up
              </button>
            </p>
          </div>
        </div>
      </div>
    )
  }

  if (currentPage === 'signup') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-md">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800">Todo App</h1>
            <p className="text-gray-600 mt-2">Create your account</p>
          </div>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}

          {success && (
            <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
              {success}
            </div>
          )}

          <form onSubmit={handleSignup}>
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-medium mb-2" htmlFor="signup-email">
                Email
              </label>
              <input
                id="signup-email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="your@email.com"
                required
              />
            </div>

            <div className="mb-6">
              <label className="block text-gray-700 text-sm font-medium mb-2" htmlFor="signup-password">
                Password
              </label>
              <input
                id="signup-password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="••••••••"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-4 rounded-lg transition duration-200 disabled:opacity-50"
            >
              {loading ? 'Creating account...' : 'Sign Up'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-gray-600">
              Already have an account?{' '}
              <button
                onClick={() => setCurrentPage('login')}
                className="text-blue-600 hover:text-blue-800 font-medium"
              >
                Sign in
              </button>
            </p>
          </div>
        </div>
      </div>
    )
  }

  // Dashboard
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">Todo App</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">
                Welcome, {user?.email}
              </span>
              <button
                onClick={logout}
                className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition duration-200"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {success && (
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-6">
            {success}
          </div>
        )}

        {/* Stats Card */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-3xl font-bold text-blue-600">{total}</div>
            <div className="text-gray-600">Total Todos</div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-3xl font-bold text-green-600">{completed}</div>
            <div className="text-gray-600">Completed</div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-3xl font-bold text-yellow-600">{pending}</div>
            <div className="text-gray-600">Pending</div>
          </div>
        </div>

        {/* Add Todo Form */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Add New Todo</h2>
          <form onSubmit={addTodo} className="space-y-4">
            <div>
              <input
                type="text"
                value={newTodo.title}
                onChange={(e) => setNewTodo({ ...newTodo, title: e.target.value })}
                placeholder="Todo title..."
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>
            <div>
              <textarea
                value={newTodo.description}
                onChange={(e) => setNewTodo({ ...newTodo, description: e.target.value })}
                placeholder="Description (optional)..."
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows="3"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-6 rounded-lg transition duration-200 disabled:opacity-50"
            >
              {loading ? 'Adding...' : 'Add Todo'}
            </button>
          </form>
        </div>

        {/* Todos List */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-800">Your Todos ({todos.length})</h2>
          </div>

          {todos.length === 0 ? (
            <div className="p-12 text-center">
              <p className="text-gray-500 text-lg">No todos yet. Add one above!</p>
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {todos.map(todo => (
                <div key={todo.id} className="p-6 hover:bg-gray-50 transition duration-150">
                  {editingTodo?.id === todo.id ? (
                    // Edit form
                    <div className="space-y-4">
                      <input
                        type="text"
                        defaultValue={todo.title}
                        id={`edit-title-${todo.id}`}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg mb-2"
                        required
                      />
                      <textarea
                        defaultValue={todo.description || ''}
                        id={`edit-desc-${todo.id}`}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg mb-2"
                        rows="2"
                      />
                      <div className="flex space-x-2">
                        <button
                          onClick={() => updateTodo(todo.id, {
                            title: document.getElementById(`edit-title-${todo.id}`).value,
                            description: document.getElementById(`edit-desc-${todo.id}`).value
                          })}
                          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded text-sm"
                        >
                          Save
                        </button>
                        <button
                          onClick={cancelEditing}
                          className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded text-sm"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  ) : (
                    // Todo display
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4">
                        <input
                          type="checkbox"
                          checked={todo.completed}
                          onChange={(e) => toggleTodoCompletion(todo.id, e.target.checked)}
                          className="h-5 w-5 text-blue-600 rounded focus:ring-blue-500"
                        />
                        <div>
                          <h3 className={`font-medium ${todo.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                            {todo.title}
                          </h3>
                          {todo.description && (
                            <p className={`text-sm ${todo.completed ? 'line-through text-gray-400' : 'text-gray-600'}`}>
                              {todo.description}
                            </p>
                          )}
                          <p className="text-xs text-gray-500 mt-1">
                            Created: {new Date(todo.created_at).toLocaleDateString()}
                          </p>
                        </div>
                      </div>

                      <div className="flex space-x-2">
                        <button
                          onClick={() => startEditing(todo)}
                          className="bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-1 rounded text-sm"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => deleteTodo(todo.id)}
                          className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm"
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}