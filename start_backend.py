import uvicorn
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "apps", "backend"))

from apps.backend.src.main import app

if __name__ == "__main__":
    print("Starting backend server with error logging...")
    try:
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            reload=False,
            log_level="debug"
        )
    except Exception as e:
        print(f"Server startup error: {e}")
        import traceback
        traceback.print_exc()