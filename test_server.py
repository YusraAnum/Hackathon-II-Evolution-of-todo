import sys
import os
sys.path.append('./')

# Change to the backend directory
os.chdir('./backend_todo_app')

try:
    from main import app
    print("Successfully imported app")
    
    import uvicorn
    print("Successfully imported uvicorn")
    
    print("Attempting to run server...")
    uvicorn.run(app, host='127.0.0.1', port=8000, log_level="info")
    
except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to continue...")