import os
import sys
import subprocess
import time

# Set environment variables
os.environ['DATABASE_URL'] = 'sqlite:///./todo_chatbot.db'
os.environ['OPENAI_API_KEY'] = 'sk-valid-test-key-for-testing'

# Change to the backend directory
os.chdir('./backend_todo_app')

# Start the server using subprocess
process = subprocess.Popen([
    sys.executable, '-c', 
    '''
import os
from src.main import app
import uvicorn

print("Starting the Todo AI Chatbot backend server...")
print("Using database URL:", os.environ.get('DATABASE_URL'))

uvicorn.run(
    app, 
    host='127.0.0.1', 
    port=8000, 
    log_level='info'
)
'''
])

print(f"Server started with PID: {process.pid}")

# Keep the script alive
try:
    process.wait()
except KeyboardInterrupt:
    print("Terminating server...")
    process.terminate()
    process.wait()