import os
import sys

# Add the backend to the Python path
sys.path.insert(0, './backend_todo_app')

# Set the environment variable for the database
os.environ['DATABASE_URL'] = 'sqlite:///./todo_app.db'

def run_server():
    try:
        from backend_todo_app.main import app
        import uvicorn

        print("Starting the Todo App backend server with debug mode...")
        print("Using database URL:", os.environ.get('DATABASE_URL'))

        uvicorn.run(
            app,
            host='0.0.0.0',
            port=8000,
            log_level='debug',  # More verbose logging
            reload=False
        )
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_server()