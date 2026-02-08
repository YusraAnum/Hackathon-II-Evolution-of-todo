import os
import sys

# Add the backend to the Python path
sys.path.insert(0, './backend_todo_app')

# Set the environment variables
os.environ['DATABASE_URL'] = 'sqlite:///../todo_chatbot.db'
os.environ['OPENAI_API_KEY'] = 'sk-valid-test-key-for-testing'

print('Attempting to start server...')

try:
    from backend_todo_app.src.main import app
    import uvicorn
    
    print("Starting the Todo AI Chatbot backend server with auth endpoints...")
    print("Using database URL:", os.environ.get('DATABASE_URL'))
    print("Using OpenAI API key:", os.environ.get('OPENAI_API_KEY'))
    
    # Run the server in the main thread
    uvicorn.run(
        app, 
        host='0.0.0.0', 
        port=8000, 
        log_level='info'
    )
except ImportError as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"Server startup failed: {e}")
    import traceback
    traceback.print_exc()