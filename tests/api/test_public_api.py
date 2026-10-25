import requests
import pytest

pytestmark = pytest.mark.api
BASE_URL = "https://jsonplaceholder.typicode.com"
USER = {"name": "Test Student", "username": "student", "email": "student@example.com"}


def test_get_user():
    response = requests.get(f"{BASE_URL}/users/1", timeout=30)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert isinstance(data["name"], str) and data["name"]
    assert isinstance(data["email"], str) and "@" in data["email"]
    assert isinstance(data["address"], dict)


def test_create_user():
    response = requests.post(f"{BASE_URL}/users", json=USER, timeout=30)
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data["id"], int)
    for key, value in USER.items():
        assert data[key] == value


def test_update_user():
    response = requests.put(f"{BASE_URL}/users/1", json={**USER, "name": "Updated Student"}, timeout=30)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Updated Student"
    assert data["username"] == USER["username"]
    assert data["email"] == USER["email"]
