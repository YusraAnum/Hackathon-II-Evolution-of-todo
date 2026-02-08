import sys
sys.path.insert(0, '.')
from database import engine, Base
from models import User, Todo
print('Engine created with URL:', engine.url)
print('Creating all tables...')
result = Base.metadata.create_all(bind=engine)
print('Tables created successfully')
# Check if tables exist
from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()
print('Tables in database:', tables)

# Also try to create a user directly
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    # Check if user already exists
    existing_user = db.query(User).filter((User.username == "testuser") | (User.email == "test@example.com")).first()
    print(f"Existing user check: {existing_user}")
except Exception as e:
    print(f"Error querying user: {e}")
finally:
    db.close()