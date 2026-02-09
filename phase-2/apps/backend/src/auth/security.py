"""
Security utilities for the Todo application
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
import bcrypt

from ..core.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    # Ensure both passwords are bytes
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')

    try:
        return bcrypt.checkpw(plain_password, hashed_password)
    except ValueError:
        # Handle the case where password is too long for bcrypt
        if len(plain_password) > 72:
            plain_password = plain_password[:72]
            return bcrypt.checkpw(plain_password, hashed_password)
        else:
            raise


def hash_password(password: str) -> str:
    """Hash a plain password."""
    # Truncate password to 72 bytes to comply with bcrypt limitations
    if isinstance(password, str):
        password = password.encode('utf-8')

    # Truncate to 72 bytes maximum for bcrypt
    if len(password) > 72:
        password = password[:72]

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)  # Default expiration

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    """Decode a JWT access token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        return int(user_id)  # Convert back to int
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )