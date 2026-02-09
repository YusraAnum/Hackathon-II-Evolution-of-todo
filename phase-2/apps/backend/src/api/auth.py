"""
Authentication API routes for the Todo application
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas.auth import UserCreate, UserLogin, Token
from ..auth.security import verify_password, hash_password, create_access_token
from ..auth.dependencies import get_current_user
from ..database.session import get_db
from ..core.config import settings

router = APIRouter()


@router.post("/signup", response_model=Token)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account.
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = hash_password(user_data.password)

    # Create new user
    user = User(email=user_data.email, password_hash=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return token.
    """
    # Find user by email
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout():
    """
    Invalidate user session.
    """
    # In a stateless JWT system, the logout is typically handled on the client side
    # by removing the token. On the server side, we might implement token blacklisting
    # if needed, but for now we'll just return a success message.
    return {"message": "Successfully logged out"}


@router.get("/me")
def get_current_user_route(current_user: User = Depends(get_current_user)):
    """
    Get current user information.
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at
    }