# Backend Specification - Todo API

## Overview
This specification defines the backend API for the Todo application using FastAPI with PostgreSQL database, SQLAlchemy ORM, Alembic for migrations, and Better Auth for authentication.

## Tech Stack
- FastAPI: Modern, fast web framework for building APIs with Python 3.7+
- PostgreSQL: Robust, open-source relational database
- SQLAlchemy: Object Relational Mapping library for database operations
- Alembic: Database migration tool for version control of schema changes
- Better Auth: Authentication library for secure user management

## Database Schema

### users table
- id (BIGINT, PRIMARY KEY, BIGSERIAL): Unique identifier for each user
- email (VARCHAR(255), UNIQUE, NOT NULL): User's email address for login
- password_hash (VARCHAR, NOT NULL): Hashed password for security
- created_at (TIMESTAMP, NOT NULL): Timestamp when the user account was created

### todos table
- id (BIGINT, PRIMARY KEY, BIGSERIAL): Unique identifier for each todo
- user_id (BIGINT, NOT NULL, REFERENCES users(id) ON DELETE CASCADE): Reference to the user who owns the todo
- title (VARCHAR, NOT NULL): Title/description of the todo item
- completed (BOOLEAN, DEFAULT FALSE): Flag indicating if the todo is completed
- created_at (TIMESTAMP, NOT NULL): Timestamp when the todo was created
- updated_at (TIMESTAMP, NULL): Timestamp when the todo was last updated

### Database Indexing
- CREATE INDEX idx_todos_user_id ON todos(user_id);

## API Endpoints

### Authentication Endpoints
- POST /auth/signup - Create a new user account
- POST /auth/login - Authenticate user and return token
- POST /auth/logout - Invalidate user session
- GET /auth/me - Get current user information

### Todo Management Endpoints
- GET /api/v1/todos - Retrieve all todos for the authenticated user
- GET /api/v1/todos/{id} - Retrieve a specific todo by ID
- POST /api/v1/todos - Create a new todo for the authenticated user
- PUT /api/v1/todos/{id} - Update an existing todo
- PATCH /api/v1/todos/{id}/toggle - Toggle the completed status of a todo
- DELETE /api/v1/todos/{id} - Delete a specific todo

## Authentication Flow
1. Signup: User registers with email and password
2. Login: User provides credentials to authenticate
3. Token Generation: System generates secure JWT Bearer token
4. Protected Routes: All todo-related endpoints require valid JWT Bearer token in Authorization header
5. Logout: User session is invalidated

## Security Requirements
- All endpoints except authentication require valid JWT Bearer token sent in Authorization header
- Passwords must be securely hashed using industry-standard algorithms
- User data isolation: Users can only access their own todos
- Rate limiting on authentication endpoints to prevent brute force attacks

## Error Handling
- Consistent error response format across all endpoints
- Proper HTTP status codes (200, 201, 400, 401, 403, 404, 500)
- Meaningful error messages for client applications

## Performance Requirements
- API response time under 500ms for standard operations
- Support for concurrent users accessing the system
- Efficient database queries with proper indexing