#!/usr/bin/env python3
"""
Server startup script with error handling for Todo App
"""
import uvicorn
import sys
import os
import logging

# Add the backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_server():
    logger.info("Starting Todo App backend server...")
    logger.info("Host: 127.0.0.1")
    logger.info("Port: 8000")
    logger.info("Reloading: enabled")

    try:
        # Import the app to catch any import errors early
        from src.main import app
        logger.info("✅ Successfully imported FastAPI app")

        # Check if database is accessible
        from src.database.session import engine
        logger.info("✅ Successfully connected to database")

        # Check if models are working
        from src.models.user import User
        from src.models.todo import Todo
        logger.info("✅ Successfully imported models")

        # Start the server
        logger.info("🚀 Starting Uvicorn server...")
        uvicorn.run(
            "src.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )

    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        logger.error("This usually means there's an issue with the code imports")
        logger.error("Check your models, dependencies, and file paths")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Server startup error: {e}")
        logger.error("Check the error above and fix the issue")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    start_server()