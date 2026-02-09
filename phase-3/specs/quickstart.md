# Quickstart Guide: AI Todo Chatbot

## Overview
This guide provides instructions to quickly set up and run the AI Todo Chatbot application.

## Prerequisites
- Python 3.11+
- Node.js 18+ (for frontend development)
- pip (Python package manager)
- npm or yarn (JavaScript package manager)

## Backend Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Set up Python virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install backend dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the backend directory:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./todo_app.db
OPENAI_API_KEY=your-openai-api-key  # if using OpenAI for NLP
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 5. Run database migrations
```bash
python -m src.main migrate
```

### 6. Start the backend server
```bash
python -m src.main run
```
The backend will start on `http://localhost:8000`

## Frontend Setup

### 1. Navigate to frontend directory
```bash
cd frontend
```

### 2. Install dependencies
```bash
npm install
# or
yarn install
```

### 3. Set up environment variables
Create a `.env` file in the frontend directory:
```env
REACT_APP_API_BASE_URL=http://localhost:8000/api
```

### 4. Start the frontend development server
```bash
npm start
# or
yarn start
```
The frontend will start on `http://localhost:3000`

## API Usage Examples

### 1. User Registration
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePassword123!"
  }'
```

### 2. User Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username_or_email": "johndoe",
    "password": "SecurePassword123!"
  }'
```

### 3. Add a Task via Chat
```bash
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {access_token}" \
  -d '{
    "message": "Add buy groceries to my list"
  }'
```

### 4. View All Tasks
```bash
curl -X GET http://localhost:8000/api/{user_id}/tasks \
  -H "Authorization: Bearer {access_token}"
```

## Environment Configuration

### Backend Configuration
- Port: Configurable via `PORT` environment variable (default: 8000)
- Database: SQLite by default, configurable via `DATABASE_URL`
- Logging: Configurable via `LOG_LEVEL` (default: INFO)

### Frontend Configuration
- Port: Configurable via `.env` file (default: 3000)
- API Base URL: Configurable via `REACT_APP_API_BASE_URL`

## Troubleshooting

### Common Issues
1. **Port already in use**: Change the port in environment variables
2. **Database connection errors**: Verify `DATABASE_URL` in .env file
3. **Authentication errors**: Ensure JWT tokens are properly included in requests
4. **NLP service errors**: Verify API keys for AI services are correctly set

### Resetting the Database
To reset the database (development only):
```bash
rm ./todo_app.db  # Remove the database file
python -m src.main migrate  # Recreate the database
```

## Development Commands

### Backend
- Run tests: `pytest`
- Format code: `black .`
- Lint code: `flake8 .`

### Frontend
- Run tests: `npm test` or `yarn test`
- Build for production: `npm run build` or `yarn build`
- Format code: `npm run format` or `yarn format`