import pytest
from fastapi.testclient import TestClient
from app.main import app, items_db, counter

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_db():
    """Reset in-memory DB before each test."""
    items_db.clear()
    counter["id"] = 1
    yield


# --- Health ---
def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"


# --- CRUD ---
def test_create_item():
    res = client.post("/items", json={"name": "Widget", "price": 9.99})
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "Widget"
    assert data["id"] == 1


def test_list_items():
    client.post("/items", json={"name": "A", "price": 1.0})
    client.post("/items", json={"name": "B", "price": 2.0})
    res = client.get("/items")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_get_item():
    client.post("/items", json={"name": "Thing", "price": 5.0})
    res = client.get("/items/1")
    assert res.status_code == 200
    assert res.json()["name"] == "Thing"


def test_get_item_not_found():
    res = client.get("/items/999")
    assert res.status_code == 404


def test_update_item():
    client.post("/items", json={"name": "Old", "price": 1.0})
    res = client.put("/items/1", json={"name": "New", "price": 99.0})
    assert res.status_code == 200
    assert res.json()["name"] == "New"
    assert res.json()["price"] == 99.0


def test_delete_item():
    client.post("/items", json={"name": "ToDelete", "price": 1.0})
    res = client.delete("/items/1")
    assert res.status_code == 200
    assert client.get("/items/1").status_code == 404