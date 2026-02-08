# Phase III Implementation Prompt: Todo AI Chatbot (MCP + OpenAI Agents SDK)

## Implementation Instructions

You are tasked with implementing the AI-powered Todo Chatbot as specified in the previous documents. Follow these instructions carefully to ensure compliance with all requirements.

## Execution Sequence

Execute the following tasks sequentially, validating each step before proceeding to the next:

1. P3-T01: Setup Neon PostgreSQL Database
2. P3-T02: Define SQLModel Schemas
3. P3-T03: Implement MCP add_task Tool
4. P3-T04: Implement MCP list_tasks Tool
5. P3-T05: Implement MCP complete_task Tool
6. P3-T06: Implement MCP delete_task Tool
7. P3-T07: Implement MCP update_task Tool
8. P3-T08: Configure OpenAI Agent
9. P3-T09: Create Stateless Chat Endpoint
10. P3-T10: Implement Conversation Persistence
11. P3-T11: Set Up Better Auth Integration
12. P3-T12: Integrate ChatKit Frontend
13. P3-T13: Test End-to-End Chatbot Flow
14. P3-T14: Implement Error Handling
15. P3-T15: Optimize Performance
16. P3-T16: Add Monitoring and Logging
17. P3-T17: Security Review
18. P3-T18: Final Integration Testing

## OpenAI Agents SDK Implementation

### Agent Configuration
- Initialize the OpenAI client with the API key from environment variables
- Create an agent with a system prompt that explains the todo management capabilities
- Register all five MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) with the agent
- Configure the agent to use function calling to execute the appropriate tools based on user input

### System Prompt
The agent should have a system prompt that includes:
- The agent's role as a todo management assistant
- Available capabilities (adding, listing, completing, deleting, updating tasks)
- Instructions to confirm actions with users
- Guidelines for handling ambiguous requests

## MCP Server Implementation

### Tool Implementation Requirements
- Each MCP tool must wrap the corresponding Phase-2 logic
- Tools must validate inputs before executing operations
- Tools must return responses in the exact format specified in the specification
- Tools must handle errors gracefully and return appropriate error messages

### Tool Functions
1. **add_task**: Creates a new task in the database
2. **list_tasks**: Retrieves tasks for a specific user with optional filtering
3. **complete_task**: Updates a task's status to completed
4. **delete_task**: Removes a task from the database
5. **update_task**: Modifies an existing task with provided fields

## Stateless Backend Architecture

### API Endpoint Requirements
- The `/api/{user_id}/chat` endpoint must be completely stateless
- All conversation state must be loaded from and saved to the database
- The endpoint must accept a user ID and message
- The endpoint must return the agent's response

### Database Operations
- Store incoming user messages in the messages table with role='user'
- Store agent responses in the messages table with role='assistant'
- Maintain conversation context by retrieving recent messages when processing new requests
- Ensure all database operations use proper transaction handling

## ChatKit Frontend Integration

### Frontend Setup
- Integrate OpenAI ChatKit as the primary user interface
- Implement authentication flow to obtain user tokens
- Connect the chat interface to the backend `/api/{user_id}/chat` endpoint
- Display conversation history from the database

### User Experience
- Show loading indicators during agent processing
- Display clear error messages when requests fail
- Maintain conversation history across page refreshes
- Provide clear feedback when tasks are created/updated/completed

## Validation Requirements

### Natural Language Scenarios
Test the chatbot against these scenarios:
1. Adding a task: "Add 'buy groceries' to my list"
2. Listing tasks: "Show me my tasks" or "What do I need to do?"
3. Completing a task: "Mark 'buy groceries' as done"
4. Updating a task: "Change 'buy groceries' to 'buy groceries and household supplies'"
5. Deleting a task: "Remove 'buy groceries' from my list"

### Persistence Validation
- Restart the server and verify conversation history remains intact
- Verify that all messages are properly stored in the database
- Confirm that conversation context is maintained across multiple interactions

### Error Handling Validation
- Test with invalid user inputs
- Verify that the agent handles ambiguous requests gracefully
- Confirm that errors are logged appropriately
- Ensure that the user receives helpful error messages

## Compliance Checks

Before completing implementation, verify:
- OpenAI Agents SDK is used correctly for AI processing
- MCP tools are properly exposed and functional
- All state is persisted to the database
- Backend remains stateless
- ChatKit frontend is properly integrated
- No traditional UI CRUD operations exist
- All Phase-2 logic is reused through MCP tools
- Natural language processing works as specified

## Success Criteria

The implementation is complete when:
- Users can manage tasks through natural language chat
- The agent correctly selects and executes appropriate tools
- Conversation context is maintained across server restarts
- All specified MCP tools function correctly
- The ChatKit frontend provides a seamless user experience
- Error handling is comprehensive and user-friendly
- Performance meets the specified metrics (>85% accuracy, <3s response time)