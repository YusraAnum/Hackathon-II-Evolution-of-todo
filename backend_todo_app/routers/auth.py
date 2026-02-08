from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import User
from database import get_db
from auth import create_access_token
from passlib.context import CryptContext

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

# Password hashing context - using a more compatible bcrypt configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SignUpRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

def hash_password(password: str) -> str:
    # Truncate password to 72 bytes to comply with bcrypt limitations
    truncated_password = password[:72] if len(password) > 72 else password
    return pwd_context.hash(truncated_password)

@router.post("/signup", response_model=TokenResponse)
def signup(request: SignUpRequest, db: Session = Depends(get_db)):
    try:
        # Check if user already exists
        existing_user = db.query(User).filter((User.username == request.username) | (User.email == request.email)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already registered"
            )

        # Create new user
        password_hash = hash_password(request.password)
        user = User(username=request.username, email=request.email, password_hash=password_hash)
        db.add(user)
        db.commit()
        db.refresh(user)

        # Create access token
        access_token = create_access_token(data={"sub": str(user.id)})

        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error and raise an internal server error
        print(f"Signup error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during signup"
        )

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    try:
        # Find user by username
        user = db.query(User).filter(User.username == request.username).first()

        if not user or not user.verify_password(request.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )

        # Create access token
        access_token = create_access_token(data={"sub": str(user.id)})

        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error and raise an internal server error
        print(f"Login error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )