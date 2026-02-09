# Phase III Constitution: Todo AI Chatbot (MCP + OpenAI Agents SDK)

## Phase Goal
Create a conversational AI Todo Assistant that allows users to manage their tasks using natural language through a chat interface. The system will leverage OpenAI's Agents SDK and MCP (Model Context Protocol) to provide intelligent task management capabilities.

## Core Principles

### 1. Technology Stack Mandate
- **Frontend**: OpenAI ChatKit for the chat interface
- **Backend**: FastAPI for the API layer
- **AI Framework**: OpenAI Agents SDK for intelligent processing
- **MCP Server**: Official MCP SDK for tool integration
- **ORM**: SQLModel for database operations
- **Database**: Neon Serverless PostgreSQL for persistence
- **Authentication**: Better Auth for user management

### 2. Architecture Requirements
- **Stateless Backend**: The backend API must be stateless, with all conversation state persisted to the database
- **Database-Backed Conversation Memory**: All conversation history and context must be stored in the database
- **Strict "NO UI CRUD — ONLY CHAT"**: No traditional UI-based task management; everything must be done through the chat interface
- **MCP Tool Integration**: All task operations must be performed through MCP tools

### 3. Reusability Constraint
- **Reuse Phase-2 Logic**: Leverage existing Phase-2 todo management logic by wrapping it in MCP tools
- **Maintain Existing Functionality**: Do not modify Phase-1 or Phase-2 implementations

### 4. Compliance Requirements
- **No Deviation After Approval**: Once specifications are approved, no deviations are allowed without formal change request
- **Follow SDD Process**: Adhere to the sp.constitution → sp.specify → sp.plan → sp.task → sp.implement sequence
- **Judging Criteria Alignment**: Meet Hackathon-II judging criteria for innovation, technical implementation, and user experience

## Non-Negotiable Requirements

### Technical Constraints
- Must use OpenAI Agents SDK for AI processing
- Must implement official MCP SDK for tool communication
- Must use ChatKit frontend for consistent user experience
- Must maintain statelessness of backend services
- Must persist all conversation data to database
- Must reuse Phase-2 todo logic as MCP tools

### Functional Constraints
- No traditional UI CRUD operations allowed
- All task management must happen through natural language
- Agent must intelligently select appropriate MCP tools
- Agent must confirm actions with users conversationally
- System must maintain conversation context across sessions

## Success Criteria

### Technical Success
- Successful integration of OpenAI Agents SDK
- Proper MCP tool implementation and exposure
- Stateless backend with database-backed persistence
- Seamless ChatKit frontend integration

### Functional Success
- Natural language task management works reliably
- Agent correctly selects and executes appropriate tools
- Conversation context maintained across restarts
- User experience is intuitive and efficient

## Governance
This constitution supersedes all other practices for Phase III implementation. All development activities must comply with these requirements. Any proposed changes to these requirements must go through formal approval process.