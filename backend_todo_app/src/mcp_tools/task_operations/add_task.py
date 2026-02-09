from typing import Dict, Any, Optional
from sqlmodel import Session, select
from datetime import datetime
import uuid
from ...models.todo_models import Task, TaskStatus, TaskPriority
from ...database.session import get_session


def add_task(user_id: str, title: str, description: Optional[str] = None, 
             due_date: Optional[str] = None, priority: Optional[str] = "medium") -> Dict[str, Any]:
    """
    MCP tool to add a new task to the user's todo list.
    
    Args:
        user_id: The ID of the user
        title: The title of the task
        description: Detailed description of the task (optional)
        due_date: Due date in ISO format (optional)
        priority: Priority level ('low', 'medium', 'high') (optional)
        
    Returns:
        Dictionary with task_id and confirmation message
    """
    # Convert due_date string to datetime if provided
    due_date_obj = None
    if due_date:
        try:
            due_date_obj = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
        except ValueError:
            return {
                "success": False,
                "message": f"Invalid due date format: {due_date}. Please use ISO format."
            }
    
    # Validate priority
    try:
        priority_enum = TaskPriority(priority.lower())
    except ValueError:
        return {
            "success": False,
            "message": f"Invalid priority: {priority}. Must be 'low', 'medium', or 'high'."
        }
    
    # Create a new task instance
    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        due_date=due_date_obj,
        priority=priority_enum
    )
    
    # Get database session and add the task
    session_gen = get_session()
    session = next(session_gen)
    
    try:
        session.add(task)
        session.commit()
        session.refresh(task)
        
        return {
            "task_id": str(task.id),
            "message": f"Task '{task.title}' has been added to your list"
        }
    except Exception as e:
        session.rollback()
        return {
            "success": False,
            "message": f"Failed to add task: {str(e)}"
        }
    finally:
        session.close()