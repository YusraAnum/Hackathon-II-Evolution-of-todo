from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
import uuid
from ..models.todo_models import Conversation, Message, UserRole
from ..database.session import get_session


def create_conversation(user_id: str, title: Optional[str] = None) -> Conversation:
    """Create a new conversation for a user."""
    session_gen = get_session()
    session = next(session_gen)
    
    try:
        conversation = Conversation(
            user_id=user_id,
            title=title,
            is_active=True
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation
    finally:
        session.close()


def get_conversation_by_id(conversation_id: str) -> Optional[Conversation]:
    """Retrieve a conversation by its ID."""
    session_gen = get_session()
    session = next(session_gen)
    
    try:
        conversation_uuid = uuid.UUID(conversation_id)
        conversation = session.get(Conversation, conversation_uuid)
        return conversation
    except ValueError:
        return None
    finally:
        session.close()


def get_conversations_for_user(user_id: str) -> List[Conversation]:
    """Retrieve all conversations for a specific user."""
    session_gen = get_session()
    session = next(session_gen)
    
    try:
        conversations = session.exec(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.created_at.desc())
        ).all()
        return conversations
    finally:
        session.close()


def add_message_to_conversation(
    conversation_id: str, 
    role: UserRole, 
    content: str, 
    tool_calls: Optional[str] = None, 
    tool_responses: Optional[str] = None
) -> Message:
    """Add a message to a conversation."""
    session_gen = get_session()
    session = next(session_gen)
    
    try:
        conversation_uuid = uuid.UUID(conversation_id)
        
        message = Message(
            conversation_id=conversation_uuid,
            role=role,
            content=content,
            tool_calls=tool_calls,
            tool_responses=tool_responses
        )
        
        session.add(message)
        session.commit()
        session.refresh(message)
        return message
    finally:
        session.close()


def get_messages_for_conversation(conversation_id: str, limit: int = 50) -> List[Message]:
    """Retrieve messages for a specific conversation."""
    session_gen = get_session()
    session = next(session_gen)
    
    try:
        conversation_uuid = uuid.UUID(conversation_id)
        messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation_uuid)
            .order_by(Message.created_at.asc())
            .limit(limit)
        ).all()
        return messages
    except ValueError:
        return []
    finally:
        session.close()


def update_conversation_title(conversation_id: str, title: str) -> bool:
    """Update the title of a conversation."""
    session_gen = get_session()
    session = next(session_gen)
    
    try:
        conversation_uuid = uuid.UUID(conversation_id)
        conversation = session.get(Conversation, conversation_uuid)
        
        if conversation:
            conversation.title = title
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()
            return True
        return False
    finally:
        session.close()


def close_conversation(conversation_id: str) -> bool:
    """Close a conversation by setting is_active to False."""
    session_gen = get_session()
    session = next(session_gen)
    
    try:
        conversation_uuid = uuid.UUID(conversation_id)
        conversation = session.get(Conversation, conversation_uuid)
        
        if conversation:
            conversation.is_active = False
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()
            return True
        return False
    finally:
        session.close()