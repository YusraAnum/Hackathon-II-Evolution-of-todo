"""
Configuration settings for the Todo application
"""
from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    # Project information
    PROJECT_NAME: str = "Todo API"
    VERSION: str = "0.1.0"

    # API settings
    API_V1_STR: str = "/api/v1"

    # Database settings - default to SQLite
    DATABASE_URL: str = "sqlite:///./todo.db"

    # Authentication settings
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = []

    class Config:
        env_file = ".env"


settings = Settings()