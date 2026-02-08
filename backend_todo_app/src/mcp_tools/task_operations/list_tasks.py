from typing import Dict, Any, List
from sqlmodel import Session, select
from datetime import datetime
from ...models.todo_models import Task, TaskStatus
from ...database.session import get_session


def list_tasks(user_id: str, status: str = "all") -> Dict[str, Any]:
    """
    MCP tool to retrieve all tasks for a specific user.
    
    Args:
        user_id: The ID of the user
        status: Filter by status ('active', 'completed', 'all') (optional)
        
    Returns:
        Dictionary with tasks array and count
    """
    session_gen = get_session()
    session = next(session_gen)
    
    try:
        # Build query based on status filter
        query = select(Task).where(Task.user_id == user_id)
        
        if status != "all":
            try:
                status_enum = TaskStatus(status.lower())
                query = query.where(Task.status == status_enum)
            except ValueError:
                return {
                    "success": False,
                    "message": f"Invalid status: {status}. Must be 'active', 'completed', or 'all'."
                }
        
        # Execute query
        tasks = session.exec(query).all()
        
        # Format tasks for response
        formatted_tasks = []
        for task in tasks:
            task_dict = {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "status": task.status.value,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "priority": task.priority.value,
                "created_at": task.created_at.isoformat(),
                "completed_at": task.completed_at.isoformat() if task.completed_at else None
            }
            formatted_tasks.append(task_dict)
        
        return {
            "tasks": formatted_tasks,
            "count": len(formatted_tasks)
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to retrieve tasks: {str(e)}"
        }
    finally:
        session.close()