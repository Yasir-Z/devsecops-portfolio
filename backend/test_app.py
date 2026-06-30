import pytest
from app import app, tasks

@pytest.fixture
def client():
    """Configures the Flask app for testing and provides a test client."""
    app.config['TESTING'] = True
    # Reset in-memory storage before each test for isolation
    tasks.clear()
    tasks.append({"id": 1, "title": "Learn DevSecOps", "completed": False})
    
    with app.test_client() as client:
        yield client

# 1. Test GET /health
def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

# 2. Test GET /tasks
def test_get_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['title'] == "Learn DevSecOps"

# 3. Test POST /tasks (Success Case)
def test_create_task_success(client):
    payload = {"title": "Build CI/CD Pipeline"}
    response = client.post('/tasks', json=payload)
    assert response.status_code == 201
    assert response.json['id'] == 2
    assert response.json['title'] == "Build CI/CD Pipeline"

# 4. Test POST /tasks (Validation Failure Case)
def test_create_task_invalid(client):
    payload = {"title": "   "} # Empty space validation check
    response = client.post('/tasks', json=payload)
    assert response.status_code == 400
    assert "error" in response.json

# 5. Test PUT /tasks/<id> (Success Case)
def test_update_task_success(client):
    payload = {"title": "Master DevSecOps", "completed": True}
    response = client.put('/tasks/1', json=payload)
    assert response.status_code == 200
    assert response.json['title'] == "Master DevSecOps"
    assert response.json['completed'] is True

# 6. Test PUT /tasks/<id> (Not Found Case)
def test_update_task_not_found(client):
    payload = {"title": "Ghost Task"}
    response = client.put('/tasks/999', json=payload)
    assert response.status_code == 404

# 7. Test DELETE /tasks/<id>
def test_delete_task(client):
    response = client.delete('/tasks/1')
    assert response.status_code == 200
    assert response.json == {"message": "Task deleted successfully"}
