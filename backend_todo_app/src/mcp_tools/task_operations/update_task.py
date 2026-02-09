from typing import Dict, Any, Optional
from sqlmodel import Session, select
from datetime import datetime
import uuid
from ...models.todo_models import Task, TaskStatus, TaskPriority
from ...database.session import get_session


def update_task(user_id: str, task_id: str, title: Optional[str] = None, 
                description: Optional[str] = None, due_date: Optional[str] = None, 
                priority: Optional[str] = None, status: Optional[str] = None) -> Dict[str, Any]:
    """
    MCP tool to modify an existing task.
    
    Args:
        user_id: The ID of the user
        task_id: The ID of the task to update
        title: New title for the task (optional)
        description: New description for the task (optional)
        due_date: New due date in ISO format (optional)
        priority: New priority level (optional)
        status: New status (optional)
        
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
        
        # Update task fields if provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if due_date is not None:
            try:
                task.due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            except ValueError:
                return {
                    "success": False,
                    "message": f"Invalid due date format: {due_date}. Please use ISO format."
                }
        if priority is not None:
            try:
                task.priority = TaskPriority(priority.lower())
            except ValueError:
                return {
                    "success": False,
                    "message": f"Invalid priority: {priority}. Must be 'low', 'medium', or 'high'."
                }
        if status is not None:
            try:
                task.status = TaskStatus(status.lower())
                # If status is being set to completed and completed_at is not set, set it now
                if task.status == TaskStatus.COMPLETED and task.completed_at is None:
                    task.completed_at = datetime.utcnow()
            except ValueError:
                return {
                    "success": False,
                    "message": f"Invalid status: {status}. Must be 'active' or 'completed'."
                }
        
        # Update the updated_at timestamp
        task.updated_at = datetime.utcnow()
        
        session.add(task)
        session.commit()
        session.refresh(task)
        
        # Create a descriptive message based on what was updated
        updates = []
        if title is not None:
            updates.append(f"title to '{task.title}'")
        if description is not None:
            updates.append("description")
        if due_date is not None:
            updates.append("due date")
        if priority is not None:
            updates.append(f"priority to '{task.priority.value}'")
        if status is not None:
            updates.append(f"status to '{task.status.value}'")
        
        update_str = ", ".join(updates)
        return {
            "success": True,
            "message": f"Task '{task.title}' has been updated ({update_str})"
        }
    except Exception as e:
        session.rollback()
        return {
            "success": False,
            "message": f"Failed to update task: {str(e)}"
        }
    finally:
        session.close()