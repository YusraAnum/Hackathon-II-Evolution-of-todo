# Todo Application - Complete Solution

This is a complete todo application with a Next.js frontend and Flask backend, featuring user authentication and full CRUD operations for todos.

## Features

- **User Authentication**: Secure signup and login with JWT tokens
- **Todo Management**: Create, read, update, delete, and mark todos as complete
- **Beautiful UI**: Modern, responsive design with Tailwind CSS
- **Statistics Dashboard**: Shows total, completed, and pending todos
- **Responsive Design**: Works on desktop and mobile devices

## Architecture

- **Frontend**: Next.js 14 with React and Tailwind CSS
- **Backend**: Flask with SQLite database
- **Authentication**: JWT-based authentication
- **Styling**: Tailwind CSS for beautiful UI components

## How to Run

### Prerequisites

- Node.js (v14 or higher)
- Python 3.x
- pip (Python package manager)

### Backend Setup

1. Navigate to the project directory
2. Install Python dependencies:
   ```bash
   pip install flask flask-cors werkzeug
   ```
3. Start the backend server:
   ```bash
   python api_backend.py
   ```
4. The backend will be available at `http://127.0.0.1:8080`

### Frontend Setup

1. Navigate to the todo-nextjs directory:
   ```bash
   cd todo-nextjs
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. The frontend will be available at `http://localhost:3000` (or next available port like 3001 if 3000 is busy)

### Usage

1. Access the application at the frontend URL (e.g., `http://localhost:3001`)
2. Sign up for a new account or log in if you already have one
3. Use the dashboard to manage your todos:
   - Add new todos with title and description
   - Mark todos as complete/incomplete
   - Edit existing todos
   - Delete todos
   - View statistics of your todo progress

## API Endpoints

The backend provides the following API endpoints:

- `POST /api/signup` - Create a new user account
- `POST /api/login` - Authenticate user and return JWT token
- `GET /api/me` - Get current user information
- `GET /api/todos` - Get all todos for the authenticated user
- `POST /api/todos` - Create a new todo
- `PUT /api/todos/<id>` - Update a todo (title, description, or completion status)
- `DELETE /api/todos/<id>` - Delete a todo

## Security

- Passwords are securely hashed using SHA-256
- Authentication is handled via JWT tokens stored in localStorage
- All API requests require authentication for protected endpoints
- CORS is configured to allow communication between frontend and backend

## Database Schema

The application uses SQLite with the following tables:

- `users`: Stores user information (id, email, password_hash)
- `todos`: Stores todo items (id, title, description, completed, user_id, created_at)

## File Structure

```
todo-app/
├── api_backend.py             # Clean API-only Flask backend server
├── simple_todo_app.py         # Original Flask backend with UI (for reference)
├── todo-nextjs/               # Next.js frontend
│   ├── package.json           # Dependencies
│   ├── src/app/page.js        # Main page with login/signup/dashboard
│   ├── src/app/layout.js      # Root layout
│   ├── next.config.js         # Next.js configuration with API rewrites
│   └── tailwind.config.js     # Tailwind CSS configuration
└── README.md                  # This file
```

## Troubleshooting

If you encounter issues:

1. Make sure both servers are running simultaneously
2. Ensure the backend server is accessible at `http://127.0.0.1:8080`
3. Check browser console for any JavaScript errors
4. Verify that the database file is writable if using SQLite
5. If frontend doesn't start on port 3000, check the terminal output for the actual port number

## Technologies Used

- **Frontend**: Next.js, React, Tailwind CSS, Axios
- **Backend**: Flask, SQLite, JWT, Werkzeug, flask-cors
- **Development**: Node.js, npm, Python