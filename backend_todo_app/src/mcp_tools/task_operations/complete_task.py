from typing import Dict, Any
from sqlmodel import Session, select
from datetime import datetime
import uuid
from ...models.todo_models import Task, TaskStatus
from ...database.session import get_session


def complete_task(user_id: str, task_id: str) -> Dict[str, Any]:
    """
    MCP tool to mark a task as completed.
    
    Args:
        user_id: The ID of the user
        task_id: The ID of the task to complete
        
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
                "message": "You don't have permission to modify this task"
            }
        
        # Update task status to completed
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.utcnow()
        task.updated_at = datetime.utcnow()
        
        session.add(task)
        session.commit()
        session.refresh(task)
        
        return {
            "success": True,
            "message": f"Task '{task.title}' has been marked as completed"
        }
    except Exception as e:
        session.rollback()
        return {
            "success": False,
            "message": f"Failed to complete task: {str(e)}"
        }
    finally:
        session.close()