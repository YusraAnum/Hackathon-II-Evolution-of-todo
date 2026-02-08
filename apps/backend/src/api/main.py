"""
Main API router for the Todo application
"""
from fastapi import APIRouter

from . import auth, todos

api_router = APIRouter()

# Include authentication routes
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Include todos routes
api_router.include_router(todos.router, prefix="/todos", tags=["todos"])