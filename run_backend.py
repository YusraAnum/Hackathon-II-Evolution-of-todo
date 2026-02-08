import os
import sys
import subprocess

def run_server():
    try:
        # Run the server from the backend directory using subprocess
        backend_dir = os.path.join(os.getcwd(), 'backend_todo_app')
        
        # Set the environment variable for the database
        env = os.environ.copy()
        env['DATABASE_URL'] = 'sqlite:///./todo_app.db'
        
        print("Starting the Todo App backend server...")
        print("Database tables will be created if they don't exist...")
        print("Using database URL:", env['DATABASE_URL'])
        
        # Run the server from the backend directory
        result = subprocess.run([
            sys.executable, '-c', 
            'from main import app; import uvicorn; uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")'
        ], cwd=backend_dir, env=env, capture_output=False)
        
        if result.returncode != 0:
            print(f"Server exited with code: {result.returncode}")
        
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Run the server in the main thread
    run_server()