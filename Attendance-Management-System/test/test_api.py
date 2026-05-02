from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_signup():
    res = client.post("/auth/signup", json={
        "name":"a","email":"a@test.com","password":"123","role":"student"
    })
    assert res.status_code == 200

def test_login():
    res = client.post("/auth/login", json={
        "email":"a@test.com","password":"123"
    })
    assert res.status_code == 200

def test_create_session():
    client.post("/auth/signup", json={
        "name":"t","email":"t@test.com","password":"123","role":"trainer"
    })
    login = client.post("/auth/login", json={
        "email":"t@test.com","password":"123"
    })
    token = login.json()["token"]

    res = client.post("/sessions",
        headers={"Authorization": f"Bearer {token}"},
        json={"title":"s","batch_id":1,"trainer_id":1}
    )
    assert res.status_code == 200

def test_monitoring_405():
    res = client.post("/monitoring/attendance")
    assert res.status_code == 405

def test_no_token():
    res = client.post("/batches", json={"name":"b","institution_id":1})
    assert res.status_code == 401