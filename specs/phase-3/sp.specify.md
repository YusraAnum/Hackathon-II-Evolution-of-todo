# Phase III Specification: Todo AI Chatbot (MCP + OpenAI Agents SDK)

## Objective
Create an AI-powered chatbot that manages todos using natural language. The system will allow users to add, view, update, complete, and delete tasks through conversational interactions with an AI agent.

## Tech Stack (MANDATORY)
- **Frontend**: OpenAI ChatKit
- **Backend**: FastAPI
- **AI Framework**: OpenAI Agents SDK
- **MCP Server**: Official MCP SDK
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Auth**: Better Auth

## Core Concepts

### Stateless Architecture
- The `/api/{user_id}/chat` endpoint is stateless
- All conversation state is persisted in the database
- Server restarts do not affect conversation continuity

### Database-Persisted Conversation Memory
- Conversation history stored in database
- Message history accessible for context
- User-specific conversation threads

### AI Agent Decision Making
- Agent analyzes user input to determine intent
- Agent selects appropriate MCP tool based on intent
- Tools perform actual task CRUD operations
- Agent confirms actions with users conversationally

## Database Models

### Task Model
```sql
Table: tasks
- id (UUID, Primary Key)
- user_id (UUID, Foreign Key to users)
- title (VARCHAR, NOT NULL)
- description (TEXT, OPTIONAL)
- status (ENUM: 'active', 'completed', DEFAULT: 'active')
- due_date (TIMESTAMP, OPTIONAL)
- priority (ENUM: 'low', 'medium', 'high', DEFAULT: 'medium')
- created_at (TIMESTAMP, DEFAULT: NOW())
- updated_at (TIMESTAMP, DEFAULT: NOW())
```

### Conversation Model
```sql
Table: conversations
- id (UUID, Primary Key)
- user_id (UUID, Foreign Key to users)
- title (VARCHAR, OPTIONAL)
- created_at (TIMESTAMP, DEFAULT: NOW())
- updated_at (TIMESTAMP, DEFAULT: NOW())
- is_active (BOOLEAN, DEFAULT: TRUE)
```

### Message Model
```sql
Table: messages
- id (UUID, Primary Key)
- conversation_id (UUID, Foreign Key to conversations)
- role (ENUM: 'user', 'assistant', 'tool_call', 'tool_response', NOT NULL)
- content (TEXT, NOT NULL)
- tool_calls (JSONB, OPTIONAL)
- tool_responses (JSONB, OPTIONAL)
- created_at (TIMESTAMP, DEFAULT: NOW())
```

## MCP Tools (STRICT)

### 1. add_task
**Purpose**: Add a new task to the user's todo list

**Parameters**:
- `user_id` (string, required): The ID of the user
- `title` (string, required): The title of the task
- `description` (string, optional): Detailed description of the task
- `due_date` (string, optional): Due date in ISO format
- `priority` (string, optional): Priority level ('low', 'medium', 'high')

**Returns**:
- `task_id` (string): The ID of the created task
- `message` (string): Confirmation message

**Example Input**:
```json
{
  "user_id": "user-123",
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "due_date": "2024-12-31T23:59:59Z",
  "priority": "medium"
}
```

**Example Output**:
```json
{
  "task_id": "task-456",
  "message": "Task 'Buy groceries' has been added to your list"
}
```

### 2. list_tasks
**Purpose**: Retrieve all tasks for a specific user

**Parameters**:
- `user_id` (string, required): The ID of the user
- `status` (string, optional): Filter by status ('active', 'completed', 'all')

**Returns**:
- `tasks` (array): Array of task objects
- `count` (number): Total number of tasks returned

**Example Input**:
```json
{
  "user_id": "user-123",
  "status": "active"
}
```

**Example Output**:
```json
{
  "tasks": [
    {
      "id": "task-456",
      "title": "Buy groceries",
      "description": "Milk, bread, eggs",
      "status": "active",
      "due_date": "2024-12-31T23:59:59Z",
      "priority": "medium",
      "created_at": "2024-11-20T10:00:00Z"
    }
  ],
  "count": 1
}
```

### 3. complete_task
**Purpose**: Mark a task as completed

**Parameters**:
- `user_id` (string, required): The ID of the user
- `task_id` (string, required): The ID of the task to complete

**Returns**:
- `success` (boolean): Whether the operation was successful
- `message` (string): Confirmation message

**Example Input**:
```json
{
  "user_id": "user-123",
  "task_id": "task-456"
}
```

**Example Output**:
```json
{
  "success": true,
  "message": "Task 'Buy groceries' has been marked as completed"
}
```

### 4. delete_task
**Purpose**: Remove a task from the user's list

**Parameters**:
- `user_id` (string, required): The ID of the user
- `task_id` (string, required): The ID of the task to delete

**Returns**:
- `success` (boolean): Whether the operation was successful
- `message` (string): Confirmation message

**Example Input**:
```json
{
  "user_id": "user-123",
  "task_id": "task-456"
}
```

**Example Output**:
```json
{
  "success": true,
  "message": "Task 'Buy groceries' has been deleted"
}
```

### 5. update_task
**Purpose**: Modify an existing task

**Parameters**:
- `user_id` (string, required): The ID of the user
- `task_id` (string, required): The ID of the task to update
- `title` (string, optional): New title for the task
- `description` (string, optional): New description for the task
- `due_date` (string, optional): New due date in ISO format
- `priority` (string, optional): New priority level
- `status` (string, optional): New status

**Returns**:
- `success` (boolean): Whether the operation was successful
- `message` (string): Confirmation message

**Example Input**:
```json
{
  "user_id": "user-123",
  "task_id": "task-456",
  "title": "Buy groceries and household supplies",
  "priority": "high"
}
```

**Example Output**:
```json
{
  "success": true,
  "message": "Task 'Buy groceries and household supplies' has been updated with high priority"
}
```

## Agent Behavior Rules

### Intent Detection
- Recognize when users want to add a task (keywords: "add", "create", "new", "remind me to")
- Recognize when users want to view tasks (keywords: "show", "list", "view", "what do I have")
- Recognize when users want to complete a task (keywords: "complete", "done", "finished", "mark as done")
- Recognize when users want to delete a task (keywords: "delete", "remove", "cancel", "get rid of")
- Recognize when users want to update a task (keywords: "update", "change", "modify", "edit")

### Tool Invocation
- Match detected intent to appropriate MCP tool
- Extract relevant parameters from user input
- Call the appropriate tool with extracted parameters
- Handle tool execution results appropriately

### Confirmation Responses
- Confirm successful task creation: "I've added '{task_title}' to your list"
- Confirm successful task completion: "I've marked '{task_title}' as completed"
- Confirm successful task deletion: "I've removed '{task_title}' from your list"
- Confirm successful task updates: "I've updated '{task_title}' with your changes"
- Respond to task listings: "Here are your {status} tasks: {list_of_tasks}"

### Error Handling
- Handle cases where task ID is not found
- Handle cases where user doesn't have permission for a task
- Handle malformed user requests gracefully
- Ask for clarification when intent is ambiguous
- Provide helpful error messages to users

## User Interaction Flow
1. User sends a message to the chat endpoint
2. Message is stored in the database with role='user'
3. AI Agent processes the message and determines intent
4. Agent calls appropriate MCP tool with extracted parameters
5. Tool performs the requested operation
6. Agent generates a response based on tool result
7. Response is stored in the database with role='assistant'
8. Response is returned to the user

## Security & Privacy
- All user data is properly isolated by user_id
- Authentication is required for all operations
- MCP tools validate user permissions before executing operations
- No sensitive data is exposed in tool responses