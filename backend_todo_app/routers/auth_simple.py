from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import uuid
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import os

# Secret key for JWT - in production, use environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

class SignUpRequest(BaseModel):
    username: str
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/signup", response_model=TokenResponse)
def signup(request: SignUpRequest):
    try:
        # For now, just return a token without saving to database
        # This will help us determine if the issue is with database operations
        
        # Generate a user ID
        user_id = str(uuid.uuid4())
        
        # Create access token
        access_token = create_access_token(data={"sub": str(user_id)})
        
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        print(f"Signup error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during signup"
        )

@router.post("/login", response_model=TokenResponse)
def login(request: SignUpRequest):  # Using same model for testing
    try:
        # For now, just return a token without checking database
        user_id = str(uuid.uuid4())
        access_token = create_access_token(data={"sub": str(user_id)})
        
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        print(f"Login error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )