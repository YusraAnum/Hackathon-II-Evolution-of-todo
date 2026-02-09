from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sqlite3
import hashlib
import os

app = FastAPI(title="Debug Todo App API", version="1.0.0")

# Simple model for signup
class SignUpRequest(BaseModel):
    username: str
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

@app.post("/api/v1/auth/signup", response_model=TokenResponse)
def signup(request: SignUpRequest):
    # Simple response without database operations
    # Just return a dummy token to test if the endpoint works
    return {"access_token": "dummy_token", "token_type": "bearer"}

@app.get("/")
def root():
    return {"message": "Debug server is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)