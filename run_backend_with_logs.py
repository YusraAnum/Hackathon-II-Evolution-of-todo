import os
import sys
import threading
import time

# Add the backend to the Python path
sys.path.insert(0, './backend_todo_app')

# Set the environment variables
os.environ['DATABASE_URL'] = 'sqlite:///./todo_chatbot.db'
os.environ['OPENAI_API_KEY'] = 'sk-valid-test-key-for-testing'

def run_server():
    try:
        from backend_todo_app.src.main import app
        import uvicorn
        
        print("Starting the Todo AI Chatbot backend server...")
        print("Using database URL:", os.environ.get('DATABASE_URL'))
        print("Using OpenAI API key:", os.environ.get('OPENAI_API_KEY'))
        
        # Run the server in the main thread
        uvicorn.run(
            app, 
            host='127.0.0.1', 
            port=8000, 
            log_level='info'
        )
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_server()