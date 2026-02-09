import os
import sys
import subprocess

# Change to the backend directory
backend_dir = os.path.join(os.path.dirname(__file__), "backend_todo_app")
os.chdir(backend_dir)

print(f"Changed to directory: {os.getcwd()}")

# Install required packages if not already installed
try:
    import fastapi
    import uvicorn
    import sqlalchemy
    import passlib
    import python_jose
    print("Required packages are available.")
except ImportError as e:
    print(f"Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Packages installed.")

# Now run the server
from main import app
import uvicorn

print("Starting server on http://127.0.0.1:8000")
uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")