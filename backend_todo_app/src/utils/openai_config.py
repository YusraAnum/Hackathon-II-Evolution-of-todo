import os
from openai import OpenAI
from unittest.mock import Mock


def get_openai_client():
    """Return the configured OpenAI client"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.startswith("sk-dummy"):
        # For testing purposes, create a mock client that simulates API responses
        mock_client = Mock()
        
        # Mock the chat.completions.create method
        def mock_create(*args, **kwargs):
            mock_response = Mock()
            mock_choice = Mock()
            
            # Check if the message contains keywords that would trigger tool calls
            messages = kwargs.get('messages', [])
            last_message = messages[-1] if messages else {}
            content = last_message.get('content', '').lower() if isinstance(last_message, dict) else ''
            
            # Create a mock tool call if needed
            if 'add' in content and ('task' in content or 'todo' in content):
                # Simulate adding a task
                mock_tool_call = Mock()
                mock_tool_call.function.name = "add_task"
                mock_tool_call.function.arguments = '{"user_id": "test_user", "title": "Sample task", "description": "A sample task added via chat"}'
                
                mock_choice.message = Mock()
                mock_choice.message.tool_calls = [mock_tool_call]
                mock_choice.message.content = None
                
            elif 'list' in content and ('task' in content or 'todo' in content):
                # Simulate listing tasks
                mock_tool_call = Mock()
                mock_tool_call.function.name = "list_tasks"
                mock_tool_call.function.arguments = '{"user_id": "test_user", "status": "all"}'
                
                mock_choice.message = Mock()
                mock_choice.message.tool_calls = [mock_tool_call]
                mock_choice.message.content = None
                
            elif 'complete' in content or 'done' in content:
                # Simulate completing a task
                mock_tool_call = Mock()
                mock_tool_call.function.name = "complete_task"
                mock_tool_call.function.arguments = '{"user_id": "test_user", "task_id": "1"}'
                
                mock_choice.message = Mock()
                mock_choice.message.tool_calls = [mock_tool_call]
                mock_choice.message.content = None
                
            elif 'delete' in content in content:
                # Simulate deleting a task
                mock_tool_call = Mock()
                mock_tool_call.function.name = "delete_task"
                mock_tool_call.function.arguments = '{"user_id": "test_user", "task_id": "1"}'
                
                mock_choice.message = Mock()
                mock_choice.message.tool_calls = [mock_tool_call]
                mock_choice.message.content = None
                
            else:
                # Default response
                mock_choice.message = Mock()
                mock_choice.message.tool_calls = None
                mock_choice.message.content = "I understand. How else can I help you with your tasks?"
            
            mock_response.choices = [mock_choice]
            return mock_response
        
        mock_client.chat.completions.create = mock_create
        return mock_client
    
    client = OpenAI(api_key=api_key)
    return client


# System prompt for the agent
SYSTEM_PROMPT = """
You are a helpful AI assistant that helps users manage their tasks through natural language.
Your capabilities include:
- Adding tasks to the user's list
- Listing the user's tasks
- Marking tasks as completed
- Updating existing tasks
- Deleting tasks from the list

When a user wants to add a task, use the add_task tool.
When a user wants to see their tasks, use the list_tasks tool.
When a user wants to complete a task, use the complete_task tool.
When a user wants to update a task, use the update_task tool.
When a user wants to delete a task, use the delete_task tool.

Always confirm actions with users conversationally.
For example: "I've added 'buy groceries' to your list" or "I've marked 'buy groceries' as completed".
If you're unsure about something, ask the user for clarification.
"""

def get_system_prompt():
    """Return the system prompt for the agent"""
    return SYSTEM_PROMPT