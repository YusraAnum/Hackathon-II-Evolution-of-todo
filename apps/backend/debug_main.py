from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.api import api_router

# Import models to register them
from src.database.session import Base, engine
from src.models import User, Todo

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Todo API - Part of the Hackathon II Evolution of Todo App"
)

# Create tables immediately (instead of on startup)
Base.metadata.create_all(bind=engine)

# CORS - Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000", "http://127.0.0.1:3001", "http://localhost:3001"],
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")