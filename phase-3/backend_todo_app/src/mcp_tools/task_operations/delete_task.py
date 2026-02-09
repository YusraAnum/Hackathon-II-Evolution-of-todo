from typing import Dict, Any
from sqlmodel import Session, select
from datetime import datetime
import uuid
from ...models.todo_models import Task
from ...database.session import get_session


def delete_task(user_id: str, task_id: str) -> Dict[str, Any]:
    """
    MCP tool to remove a task from the user's list.
    
    Args:
        user_id: The ID of the user
        task_id: The ID of the task to delete
        
    Returns:
        Dictionary with success status and confirmation message
    """
    session_gen = get_session()
    session = next(session_gen)
    
    try:
        # Validate UUID
        try:
            task_uuid = uuid.UUID(task_id)
        except ValueError:
            return {
                "success": False,
                "message": f"Invalid task ID format: {task_id}"
            }
        
        # Find the task
        task = session.get(Task, task_uuid)
        
        if not task:
            return {
                "success": False,
                "message": f"Task with ID {task_id} not found"
            }
        
        # Verify the task belongs to the user
        if task.user_id != user_id:
            return {
                "success": False,
                "message": "You don't have permission to delete this task"
            }
        
        # Delete the task
        session.delete(task)
        session.commit()
        
        return {
            "success": True,
            "message": f"Task '{task.title}' has been deleted"
        }
    except Exception as e:
        session.rollback()
        return {
            "success": False,
            "message": f"Failed to delete task: {str(e)}"
        }
    finally:
        session.close()