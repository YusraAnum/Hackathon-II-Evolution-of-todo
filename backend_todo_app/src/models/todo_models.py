from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid
from enum import Enum


class TaskStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class UserRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    TOOL_CALL = "tool_call"
    TOOL_RESPONSE = "tool_response"


# Forward declarations
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(index=True)  # Using string for user ID from auth
    title: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")


class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversations.id", index=True)
    role: UserRole = Field(sa_column_kwargs={"default": UserRole.USER})
    content: str = Field()
    tool_calls: Optional[str] = Field(default=None)  # JSON string for tool calls
    tool_responses: Optional[str] = Field(default=None)  # JSON string for tool responses
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to conversation
    conversation: Conversation = Relationship(back_populates="messages")


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(index=True)  # Using string for user ID from auth
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None)
    status: TaskStatus = Field(sa_column_kwargs={"default": TaskStatus.ACTIVE})
    due_date: Optional[datetime] = Field(default=None)
    priority: TaskPriority = Field(sa_column_kwargs={"default": TaskPriority.MEDIUM})
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)

    def dict(self, **kwargs):
        # Override dict to handle datetime serialization
        d = super().dict(**kwargs)
        for key, value in d.items():
            if isinstance(value, datetime):
                d[key] = value.isoformat()
        return d