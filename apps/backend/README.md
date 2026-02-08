# Todo Application Backend

This is the backend for the Todo application built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- User authentication with JWT tokens (signup, login, logout, get current user)
- Todo management (CRUD operations with user ownership)
- Database persistence with PostgreSQL
- Alembic for database migrations
- Pydantic for data validation
- SQLAlchemy ORM for database operations

## Tech Stack

- FastAPI: Modern, fast web framework for building APIs with Python
- PostgreSQL: Robust, open-source relational database
- SQLAlchemy: Object Relational Mapping library for database operations
- Alembic: Database migration tool for version control of schema changes
- JWT: Secure authentication with JSON Web Tokens
- Passlib: Password hashing and verification

## Project Structure

```
apps/backend/
├── src/
│   ├── models/           # Database models (User, Todo)
│   ├── api/              # API routes (auth, todos)
│   ├── auth/             # Authentication utilities
│   ├── database/         # Database session management
│   ├── core/             # Configuration settings
│   ├── schemas/          # Pydantic schemas for data validation
│   └── main.py           # Main FastAPI application
├── alembic/              # Database migration scripts
├── alembic.ini          # Alembic configuration
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Poetry configuration
├── main.py              # Application entry point
└── README.md            # This file
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables (or update config):
   - DATABASE_URL
   - SECRET_KEY

3. Run the application:
   ```bash
   python main.py
   ```

The application will start on http://localhost:8000

## API Endpoints

### Authentication Endpoints
- `POST /auth/signup` - Create a new user account
- `POST /auth/login` - Authenticate user and return token
- `POST /auth/logout` - Invalidate user session
- `GET /auth/me` - Get current user information

### Todo Management Endpoints
- `GET /api/v1/todos` - Retrieve all todos for the authenticated user
- `GET /api/v1/todos/{id}` - Retrieve a specific todo by ID
- `POST /api/v1/todos` - Create a new todo for the authenticated user
- `PUT /api/v1/todos/{id}` - Update an existing todo
- `PATCH /api/v1/todos/{id}/toggle` - Toggle the completed status of a todo
- `DELETE /api/v1/todos/{id}` - Delete a specific todo