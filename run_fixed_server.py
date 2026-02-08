import os
import sys
sys.path.insert(0, '.')

# Change to the backend directory
os.chdir('backend_todo_app')

from main import app
import uvicorn

if __name__ == "__main__":
    print("Starting server on http://127.0.0.1:8000")
    try:
        uvicorn.run(app, host='127.0.0.1', port=8000, log_level="debug")
    except Exception as e:
        print(f"Server error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to continue...")