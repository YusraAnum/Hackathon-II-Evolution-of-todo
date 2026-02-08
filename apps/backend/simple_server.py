import uvicorn
from src.main import app

if __name__ == "__main__":
    print("Starting server on http://127.0.0.1:8000")
    print("If you see this message, server is starting...")
    try:
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            log_level="warning"  # Reduced logging to avoid console issues
        )
    except Exception as e:
        print(f"Server error: {e}")
        import traceback
        traceback.print_exc()