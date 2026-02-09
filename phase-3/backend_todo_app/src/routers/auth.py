from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import timedelta
from ..utils.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["authentication"])

# Pydantic models for request/response
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# In the Phase 3 implementation, we're using a simplified approach
# where users are identified by UUIDs without storing user details in a separate table
# This is consistent with the architecture that focuses on task management and conversations

@router.post("/signup", response_model=Token)
def signup(user_data: UserCreate):
    """
    Create a new user account.
    In this implementation, we generate a user ID without storing user details,
    which is consistent with the Phase 3 architecture focusing on task management.
    """
    # Generate a new user ID
    user_id = str(uuid.uuid4())
    
    # Create access token
    token_data = {"sub": user_id, "username": user_data.username, "email": user_data.email}
    access_token = create_access_token(data=token_data, expires_delta=timedelta(hours=24))
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(login_data: UserLogin):
    """
    Authenticate a user and return an access token.
    For this demo implementation, we're not validating credentials against a database
    since the Phase 3 architecture doesn't include a persistent user store.
    """
    # In a real implementation, you would validate credentials against a database
    # For this demo, we'll just generate a token for any login attempt
    
    # Generate a user ID (in a real app, you'd look up the user by credentials)
    user_id = str(uuid.uuid4())
    
    # Create access token
    token_data = {"sub": user_id, "username": login_data.username}
    access_token = create_access_token(data=token_data, expires_delta=timedelta(hours=24))
    
    return {"access_token": access_token, "token_type": "bearer"}