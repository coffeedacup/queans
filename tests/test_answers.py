import pytest
from app.models import Question

def test_create_answer(client, db_session):
    question = Question(text="Test question?")
    db_session.add(question)
    db_session.commit()
    db_session.refresh(question)
    
    response = client.post(
        f"/api/v1/questions/{question.id}/answers/",
        json={"text": "Test answer", "user_id": "user123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "Test answer"
    assert data["user_id"] == "user123"
    assert data["question_id"] == question.id

def test_create_answer_nonexistent_question(client):
    response = client.post(
        "/api/v1/questions/999/answers/",
        json={"text": "Test answer", "user_id": "user123"}
    )
    assert response.status_code == 404

def test_get_answer(client, db_session):
    question = Question(text="Test question?")
    db_session.add(question)
    db_session.commit()
    db_session.refresh(question)
    
    answer_data = {"text": "Test answer", "user_id": "user123"}
    create_response = client.post(
        f"/api/v1/questions/{question.id}/answers/",
        json=answer_data
    )
    answer_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/questions/{question.id}/answers/{answer_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Test answer"
    assert data["user_id"] == "user123"

def test_delete_answer(client, db_session):
    question = Question(text="Test question?")
    db_session.add(question)
    db_session.commit()
    db_session.refresh(question)
    
    answer_data = {"text": "Test answer", "user_id": "user123"}
    create_response = client.post(
        f"/api/v1/questions/{question.id}/answers/",
        json=answer_data
    )
    answer_id = create_response.json()["id"]
    
    response = client.delete(f"/api/v1/questions/{question.id}/answers/{answer_id}")
    assert response.status_code == 200
    
    get_response = client.get(f"/api/v1/questions/{question.id}/answers/{answer_id}")
    assert get_response.status_code == 404