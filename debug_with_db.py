from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import os

# Add the backend directory to the path
import sys
sys.path.insert(0, './backend_todo_app')

from database import engine, Base
from models import User

app = FastAPI(title="Debug Todo App API with DB", version="1.0.0")

# Simple model for signup
class SignUpRequest(BaseModel):
    username: str
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

@app.post("/api/v1/auth/signup", response_model=TokenResponse)
def signup(request: SignUpRequest, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter((User.username == request.username) | (User.email == request.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already registered"
        )

    # Return a dummy response for now to test if DB operations work
    return {"access_token": "dummy_token_with_db", "token_type": "bearer"}

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)