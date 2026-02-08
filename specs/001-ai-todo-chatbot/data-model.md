# Data Model: AI Todo Chatbot

## Overview
This document defines the data models for the AI Todo Chatbot feature, including entities, their fields, relationships, and validation rules.

## Entity: User
Represents a registered user with authentication credentials and profile information.

### Fields
- `id` (Integer, Primary Key, Auto-increment)
- `username` (String, Unique, Not Null, Length: 3-50 characters)
- `email` (String, Unique, Not Null, Valid Email Format)
- `password_hash` (String, Not Null, Encrypted using bcrypt)
- `created_at` (DateTime, Not Null, Auto-generated)
- `updated_at` (DateTime, Not Null, Auto-generated)
- `is_active` (Boolean, Default: True)

### Relationships
- One-to-Many: User → Tasks
- One-to-Many: User → Conversations

### Validation Rules
- Username must be 3-50 alphanumeric characters plus underscores/hyphens
- Email must follow standard email format
- Password must meet minimum strength requirements (8+ chars, mixed case, number, special char)
- Email and username must be unique across all users

## Entity: Task
Represents a todo item with properties like title, description, status (active/completed), due date, and priority.

### Fields
- `id` (Integer, Primary Key, Auto-increment)
- `user_id` (Integer, Foreign Key to User.id, Not Null)
- `title` (String, Not Null, Length: 1-200 characters)
- `description` (Text, Optional, Length: 0-1000 characters)
- `status` (String, Not Null, Values: "active", "completed", Default: "active")
- `due_date` (DateTime, Optional)
- `priority` (String, Default: "medium", Values: "low", "medium", "high")
- `created_at` (DateTime, Not Null, Auto-generated)
- `updated_at` (DateTime, Not Null, Auto-generated)
- `completed_at` (DateTime, Optional)

### Relationships
- Many-to-One: Task → User (owner)
- One-to-Many: Task → TaskUpdates (historical changes)

### Validation Rules
- Title must be 1-200 characters
- Status must be one of the allowed values
- Due date must be in the future if provided
- Priority must be one of the allowed values
- User_id must reference an existing user

### State Transitions
- `active` → `completed` (when task is marked as completed)
- `completed` → `active` (when task is reopened)

## Entity: Conversation
Represents a chat session with a unique identifier and associated messages.

### Fields
- `id` (Integer, Primary Key, Auto-increment)
- `user_id` (Integer, Foreign Key to User.id, Not Null)
- `title` (String, Optional, Auto-generated from first message if not provided)
- `created_at` (DateTime, Not Null, Auto-generated)
- `updated_at` (DateTime, Not Null, Auto-generated)
- `is_active` (Boolean, Default: True)

### Relationships
- Many-to-One: Conversation → User (owner)
- One-to-Many: Conversation → ChatMessages

### Validation Rules
- User_id must reference an existing user
- Title must be 0-100 characters if provided

## Entity: ChatMessage
Represents an individual message in a conversation with sender, content, and timestamp.

### Fields
- `id` (Integer, Primary Key, Auto-increment)
- `conversation_id` (Integer, Foreign Key to Conversation.id, Not Null)
- `sender_type` (String, Not Null, Values: "user", "ai")
- `content` (Text, Not Null, Length: 1-5000 characters)
- `timestamp` (DateTime, Not Null, Auto-generated)
- `tool_calls` (JSON, Optional, Contains function calls made by AI)

### Relationships
- Many-to-One: ChatMessage → Conversation
- Many-to-One: ChatMessage → User (for user messages)

### Validation Rules
- Conversation_id must reference an existing conversation
- Sender_type must be one of the allowed values
- Content must be 1-5000 characters
- Tool_calls must be valid JSON if provided

## Entity: TaskUpdate (Optional Historical Tracking)
Represents historical changes to tasks for audit purposes.

### Fields
- `id` (Integer, Primary Key, Auto-increment)
- `task_id` (Integer, Foreign Key to Task.id, Not Null)
- `field_changed` (String, Not Null, e.g., "title", "status", "due_date")
- `old_value` (Text, Optional)
- `new_value` (Text, Optional)
- `changed_at` (DateTime, Not Null, Auto-generated)
- `changed_by_user_id` (Integer, Foreign Key to User.id, Not Null)

### Relationships
- Many-to-One: TaskUpdate → Task
- Many-to-One: TaskUpdate → User (changer)

### Validation Rules
- Task_id must reference an existing task
- Field_changed must be a valid task field
- Changed_by_user_id must reference an existing user