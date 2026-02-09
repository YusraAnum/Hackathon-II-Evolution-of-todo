from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.api import api_router

# 🔥 DB IMPORTS (IMPORTANT) - Import models to register them with Base
from src.database.session import Base, engine
from src.models import User, Todo  # Explicitly import models to register them with Base

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Todo API - Part of the Hackathon II Evolution of Todo App"
)

# Create tables immediately
Base.metadata.create_all(bind=engine)

# CORS - Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "todo-api"}


@app.get("/")
async def root():
    return {"message": "Welcome to the Todo API v1"}