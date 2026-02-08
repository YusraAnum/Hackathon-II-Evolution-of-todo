from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from passlib.context import CryptContext

# Import Base from the database module to ensure consistency
from database import Base

# Password hashing context - using a more compatible bcrypt configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def verify_password(self, plain_password):
        # Truncate password to 72 bytes to comply with bcrypt limitations
        truncated_password = plain_password[:72] if len(plain_password) > 72 else plain_password
        try:
            return pwd_context.verify(truncated_password, self.password_hash)
        except Exception as e:
            print(f"Error verifying password: {e}")
            return False

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())