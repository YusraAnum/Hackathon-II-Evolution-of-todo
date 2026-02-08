# Phase III: Todo AI Chatbot (MCP + OpenAI Agents SDK)

## Overview
This project implements an AI-powered chatbot for managing todos using natural language. The system leverages OpenAI's Agents SDK and MCP (Model Context Protocol) to provide intelligent task management capabilities.

## Architecture
- **Frontend**: React/Next.js with OpenAI ChatKit
- **Backend**: FastAPI with SQLModel and Neon PostgreSQL
- **AI Framework**: OpenAI Agents SDK
- **MCP Server**: Official MCP SDK for tool integration
- **Authentication**: JWT-based authentication

## Features
- Natural language task management (add, list, update, complete, delete tasks)
- Persistent conversation history
- MCP-based tool integration
- JWT-based authentication
- Stateless backend architecture

## Tech Stack
- **Frontend**: Next.js, React, OpenAI ChatKit
- **Backend**: FastAPI, SQLModel, Neon PostgreSQL
- **AI Framework**: OpenAI Agents SDK
- **MCP Server**: Official MCP SDK
- **Authentication**: JWT
- **Deployment**: Docker-ready

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend_todo_app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Run the application:
   ```bash
   python -m src.main
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend_todo_app
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your configuration
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

## API Endpoints
- `POST /api/{user_id}/chat` - Chat endpoint for interacting with the AI assistant
- `GET /` - Health check endpoint

## MCP Tools
The system implements the following MCP tools:
- `add_task` - Add a new task to the user's todo list
- `list_tasks` - Retrieve all tasks for a specific user
- `complete_task` - Mark a task as completed
- `delete_task` - Remove a task from the user's list
- `update_task` - Modify an existing task

## Environment Variables
### Backend
- `DATABASE_URL` - PostgreSQL database URL
- `OPENAI_API_KEY` - OpenAI API key
- `JWT_SECRET_KEY` - Secret key for JWT signing
- `NEON_DATABASE_URL` - Neon PostgreSQL database URL

### Frontend
- `NEXT_PUBLIC_API_BASE_URL` - Backend API base URL

## Development
The project follows the SDD (Specification Driven Development) methodology with the following phases:
1. sp.constitution.md - Project constitution and principles
2. sp.specify.md - Detailed specifications
3. sp.plan.md - Implementation plan
4. sp.task.md - Task breakdown
5. sp.implement.md - Implementation instructions

## Testing
To run tests:
```bash
# Backend tests
cd backend_todo_app
pytest

# Frontend tests
cd frontend_todo_app
npm run test
```

## Deployment
The application is Docker-ready. Use the provided Dockerfile to containerize the application.

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License
This project is licensed under the MIT License.