import uvicorn
import logging
import sys
from apps.backend.src.main import app

# Set up logging to see detailed errors
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    print("Starting server with debug logging...")
    try:
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            log_level="debug",
            access_log=True
        )
    except Exception as e:
        print(f"Server error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)