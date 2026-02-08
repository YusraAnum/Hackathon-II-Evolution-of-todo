from fastapi import HTTPException, Request, Depends
from typing import Optional
import os
import jwt
from datetime import datetime, timedelta
from ..utils.openai_config import get_openai_client


# Secret key for JWT (should come from environment)
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback_secret_key_for_development")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    """Verify a JWT token and return the payload."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


async def get_current_user(request: Request):
    """Dependency to get the current user from the Authorization header."""
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.split(" ")[1]  # Extract token after "Bearer "
    payload = verify_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    return {"user_id": user_id}


def get_user_id_from_token(token: str) -> Optional[str]:
    """Extract user ID from a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None