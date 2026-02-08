from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, todos

app = FastAPI(title="Todo App API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(todos.router)

@app.get("/")
async def root():
    return {"message": "Todo App API is running!"}

# Create database tables after app is defined to avoid circular imports
import asyncio
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Create tables on startup
@app.on_event("startup")
def startup_event():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")