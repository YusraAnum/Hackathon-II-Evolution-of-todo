import os
import sys
sys.path.insert(0, 'backend_todo_app')

# Set the environment variable before importing any modules
os.environ['DATABASE_URL'] = 'sqlite:///./todo_chatbot.db'

from backend_todo_app.src.database.session import engine
from backend_todo_app.src.models.todo_models import Conversation, Message, Task
from sqlmodel import SQLModel

# Create all tables
SQLModel.metadata.create_all(engine)
print('Database tables created successfully in todo_chatbot.db')