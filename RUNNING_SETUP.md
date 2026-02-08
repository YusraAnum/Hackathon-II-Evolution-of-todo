# Running Setup Instructions

## Servers

- **Backend API Server**: http://127.0.0.1:8080
  - Clean Flask API-only server (no UI)
  - Handles all authentication and todo operations
  - SQLite database backend

- **Frontend Server**: http://localhost:3001 (or next available port)
  - Next.js application with beautiful UI
  - Responsive design with Tailwind CSS
  - Full todo management features

## How to Run

### Terminal 1: Start Backend
```bash
cd "C:\Users\YUSRA\OneDrive\Desktop\Hackathon-II Evolution of todo app"
python api_backend.py
```

### Terminal 2: Start Frontend
```bash
cd "C:\Users\YUSRA\OneDrive\Desktop\Hackathon-II Evolution of todo app\todo-nextjs"
npm run dev
```

## API Endpoints Available

- `POST /api/signup` - Create a new user account
- `POST /api/login` - Authenticate user and return JWT token
- `GET /api/me` - Get current user information
- `GET /api/todos` - Get all todos for the authenticated user
- `POST /api/todos` - Create a new todo
- `PUT /api/todos/<id>` - Update a todo
- `DELETE /api/todos/<id>` - Delete a todo

## Frontend Features

- Beautiful login/signup forms
- Dashboard with todo management
- Add/edit/delete todos
- Mark todos as complete/incomplete
- Statistics showing total/completed/pending todos
- Responsive design for all screen sizes
- Error handling and user feedback
- Session management with JWT tokens
- Proper API communication using Next.js rewrites to avoid CORS issues

## Architecture

The application uses Next.js rewrites to forward API requests from the frontend to the backend, maintaining separation of concerns while enabling seamless communication.