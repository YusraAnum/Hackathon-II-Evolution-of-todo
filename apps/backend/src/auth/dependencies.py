"""
Authentication dependencies for the Todo application
"""
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .security import decode_access_token
from ..database.session import get_db
from ..models.user import User
from sqlalchemy.orm import Session

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user.

    Args:
        credentials: HTTP Bearer token credentials
        db: Database session

    Returns:
        User: The authenticated user object

    Raises:
        HTTPException: If the token is invalid or user doesn't exist
    """
    token = credentials.credentials

    user_id = decode_access_token(token)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user