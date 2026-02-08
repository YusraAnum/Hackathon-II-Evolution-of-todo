# Todo Application - Complete Solution

This is a complete full-stack todo application with a React/Vite frontend and FastAPI backend, featuring user authentication and full CRUD operations for todos.

## Features

- **User Authentication**: Secure signup and login with JWT tokens
- **Todo Management**: Create, read, update, delete, and mark todos as complete
- **Modern UI**: Clean, responsive React interface
- **Statistics Dashboard**: Shows total, completed, and pending todos
- **Responsive Design**: Works on desktop and mobile devices

## Architecture

- **Frontend**: React 18 with Vite and React Router
- **Backend**: FastAPI with SQLite database and SQLAlchemy ORM
- **Authentication**: JWT-based authentication with bcrypt password hashing
- **Styling**: CSS with responsive design

## How to Run

### Prerequisites

- Node.js (v14 or higher)
- Python 3.x
- pip (Python package manager)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd apps/backend
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the backend server:
   ```bash
   python -m uvicorn src.main:app --reload --port 8000
   ```
4. The backend will be available at `http://127.0.0.1:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd apps/frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. The frontend will be available at `http://localhost:5173` (or next available port)

### Usage

1. Access the application at the frontend URL (e.g., `http://localhost:5173`)
2. Sign up for a new account or log in if you already have one
3. Use the dashboard to manage your todos:
   - Add new todos with title and description
   - Mark todos as complete/incomplete
   - Edit existing todos
   - Delete todos
   - View statistics of your todo progress

## API Endpoints

The backend provides the following API endpoints:

- `POST /api/v1/auth/signup` - Create a new user account
- `POST /api/v1/auth/login` - Authenticate user and return JWT token
- `GET /api/v1/auth/me` - Get current user information
- `GET /api/v1/todos/` - Get all todos for the authenticated user
- `POST /api/v1/todos/` - Create a new todo
- `PUT /api/v1/todos/{id}` - Update a todo (title, description, or completion status)
- `PATCH /api/v1/todos/{id}/toggle` - Toggle completion status of a todo
- `DELETE /api/v1/todos/{id}` - Delete a todo

## Security

- Passwords are securely hashed using bcrypt
- Authentication is handled via JWT tokens stored in localStorage
- All API requests require authentication for protected endpoints
- CORS is configured to allow communication between frontend and backend
- User isolation - each user only sees their own todos

## Database Schema

The application uses SQLite with SQLAlchemy ORM and the following models:

- `User`: Stores user information (id, email, hashed_password)
- `Todo`: Stores todo items (id, title, description, completed, owner_id, created_at)

## File Structure

```
todo-app/
├── apps/
│   ├── backend/
│   │   ├── src/
│   │   │   ├── main.py
│   │   │   ├── core/config.py
│   │   │   ├── database/session.py
│   │   │   ├── models/(user.py, todo.py)
│   │   │   ├── auth/(security.py, dependencies.py)
│   │   │   ├── api/(auth.py, todos.py, main.py)
│   │   │   └── schemas/(auth.py, todo.py)
│   │   ├── requirements.txt
│   │   └── todo.db (generated)
│   └── frontend/
│       ├── package.json
│       ├── src/
│       │   ├── main.jsx
│       │   ├── App.jsx
│       │   ├── components/(Login.jsx, Signup.jsx, Dashboard.jsx)
│       │   ├── index.css
│       │   └── App.css
│       ├── index.html
│       └── vite.config.js
├── api_backend.py             # Legacy Flask API-only backend server
├── simple_todo_app.py         # Original Flask backend with UI (for reference)
└── README.md                  # This file
```

## Troubleshooting

If you encounter issues:

1. Make sure both servers are running simultaneously
2. Ensure the backend server is accessible at `http://127.0.0.1:8000`
3. Check browser console for any JavaScript errors
4. Verify that the database file is writable if using SQLite
5. If frontend doesn't start on port 5173, check the terminal output for the actual port number

## Technologies Used

- **Frontend**: React 18, Vite, React Router, Axios
- **Backend**: FastAPI, SQLite, SQLAlchemy, Pydantic, JWT, bcrypt
- **Development**: Node.js, npm, Python, uvicorn