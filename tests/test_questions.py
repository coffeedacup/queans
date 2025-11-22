import pytest
from app.models import Question

def test_create_question(client):
    response = client.post(
        "/api/v1/questions/",
        json={"text": "Test question?"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "Test question?"
    assert "id" in data
    assert "created_at" in data

def test_get_questions(client):
    client.post("/api/v1/questions/", json={"text": "Test question?"})
    
    response = client.get("/api/v1/questions/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["text"] == "Test question?"

def test_get_question_not_found(client):
    response = client.get("/api/v1/questions/999")
    assert response.status_code == 404

def test_delete_question(client):
    create_response = client.post("/api/v1/questions/", json={"text": "Test question?"})
    question_id = create_response.json()["id"]
    
    response = client.delete(f"/api/v1/questions/{question_id}")
    assert response.status_code == 200
    
    get_response = client.get(f"/api/v1/questions/{question_id}")
    assert get_response.status_code == 404