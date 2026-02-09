from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import User
from database import get_db
from auth import create_access_token
from passlib.context import CryptContext
import traceback
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
    logger.debug(f"Hashing password of length: {len(truncated_password)}")
    try:
        hashed = pwd_context.hash(truncated_password)
        logger.debug("Password hashed successfully")
        return hashed
    except Exception as e:
        logger.error(f"Error hashing password: {e}")
        raise

@router.post("/signup", response_model=TokenResponse)
def signup(request: SignUpRequest, db: Session = Depends(get_db)):
    logger.info(f"Signup request received for user: {request.username}")
    try:
        # Check if user already exists
        logger.debug("Checking if user already exists")
        existing_user = db.query(User).filter((User.username == request.username) | (User.email == request.email)).first()
        logger.debug(f"Existing user check result: {existing_user is not None}")
        
        if existing_user:
            logger.warning("User already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already registered"
            )

        # Create new user
        logger.debug("Creating new user")
        password_hash = hash_password(request.password)
        user = User(username=request.username, email=request.email, password_hash=password_hash)
        logger.debug("Adding user to database session")
        db.add(user)
        logger.debug("Committing transaction")
        db.commit()
        logger.debug("Refreshing user object")
        db.refresh(user)
        logger.info(f"User created successfully with ID: {user.id}")

        # Create access token
        logger.debug("Creating access token")
        access_token = create_access_token(data={"sub": str(user.id)})
        logger.info("Access token created successfully")

        logger.info("Signup completed successfully")
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        logger.error("HTTP Exception occurred")
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"General exception in signup: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error during signup: {str(e)}"
        )

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    logger.info(f"Login request received for user: {request.username}")
    try:
        # Find user by username
        logger.debug("Querying user from database")
        user = db.query(User).filter(User.username == request.username).first()
        logger.debug(f"User found: {user is not None}")

        if not user or not user.verify_password(request.password):
            logger.warning("Invalid credentials")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )

        # Create access token
        logger.debug("Creating access token for login")
        access_token = create_access_token(data={"sub": str(user.id)})
        logger.info("Login completed successfully")

        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        logger.error("HTTP Exception occurred in login")
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"General exception in login: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error during login: {str(e)}"
        )