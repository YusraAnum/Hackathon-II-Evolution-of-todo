import uvicorn
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app

if __name__ == "__main__":
    try:
        print("Starting server...")
        uvicorn.run(
            "src.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="debug"
        )
    except Exception as e:
        print(f"Server error: {e}")
        import traceback
        traceback.print_exc()