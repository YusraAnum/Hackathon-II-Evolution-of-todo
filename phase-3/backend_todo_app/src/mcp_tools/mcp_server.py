from mcp.shared.exceptions import McpError
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.shared import mcp_util
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import uvicorn
from ..mcp_tools.task_operations.add_task import add_task
from ..mcp_tools.task_operations.list_tasks import list_tasks
from ..mcp_tools.task_operations.complete_task import complete_task
from ..mcp_tools.task_operations.delete_task import delete_task
from ..mcp_tools.task_operations.update_task import update_task


# Define the server
server = Server("todo-mcp-server")


# Define the tool schemas
class AddTaskArguments(BaseModel):
    user_id: str
    title: str
    description: Optional[str] = None
    due_date: Optional[str] = None
    priority: Optional[str] = "medium"


class ListTasksArguments(BaseModel):
    user_id: str
    status: Optional[str] = "all"


class CompleteTaskArguments(BaseModel):
    user_id: str
    task_id: str


class DeleteTaskArguments(BaseModel):
    user_id: str
    task_id: str


class UpdateTaskArguments(BaseModel):
    user_id: str
    task_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None


# Register the tools with the server
@server.tool("add_task", "Add a new task to the user's todo list")
async def handle_add_task(args: AddTaskArguments):
    result = add_task(
        user_id=args.user_id,
        title=args.title,
        description=args.description,
        due_date=args.due_date,
        priority=args.priority
    )
    return result


@server.tool("list_tasks", "Retrieve all tasks for a specific user")
async def handle_list_tasks(args: ListTasksArguments):
    result = list_tasks(
        user_id=args.user_id,
        status=args.status
    )
    return result


@server.tool("complete_task", "Mark a task as completed")
async def handle_complete_task(args: CompleteTaskArguments):
    result = complete_task(
        user_id=args.user_id,
        task_id=args.task_id
    )
    return result


@server.tool("delete_task", "Remove a task from the user's list")
async def handle_delete_task(args: DeleteTaskArguments):
    result = delete_task(
        user_id=args.user_id,
        task_id=args.task_id
    )
    return result


@server.tool("update_task", "Modify an existing task")
async def handle_update_task(args: UpdateTaskArguments):
    result = update_task(
        user_id=args.user_id,
        task_id=args.task_id,
        title=args.title,
        description=args.description,
        due_date=args.due_date,
        priority=args.priority,
        status=args.status
    )
    return result


async def start_mcp_server():
    """Start the MCP server"""
    options = InitializationOptions(
        server_name="Todo MCP Server",
        server_version="1.0.0"
    )
    
    async with server.clipboard(options):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(start_mcp_server())