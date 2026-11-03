from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "healthy"}

def test_get_existing_user():
    res = client.get("/users/alice")
    assert res.status_code == 200
    assert res.json()["email"] == "alice@example.com"

def test_get_missing_user():
    res = client.get("/users/unknown")
    assert res.status_code == 404