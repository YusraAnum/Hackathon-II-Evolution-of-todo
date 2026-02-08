import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "todo-api"}


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_create_and_get_todo():
    """Test creating and retrieving a todo"""
    # Create a todo
    todo_data = {
        "title": "Test Todo",
        "description": "Test Description"
    }
    response = client.post("/api/v1/todos/", json=todo_data)
    assert response.status_code == 200

    # Get the created todo
    created_todo = response.json()
    todo_id = created_todo["id"]

    response = client.get(f"/api/v1/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["id"] == todo_id
    assert response.json()["title"] == "Test Todo"