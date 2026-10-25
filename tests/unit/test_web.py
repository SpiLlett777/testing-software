import itertools
import pytest


@pytest.mark.parametrize("route", ["/", "/calculator", "/todo", "/todo?mode=buggy", "/login", "/contact"])
def test_pages_render(client, route):
    response = client.get(route)
    assert response.status_code == 200
    assert '<html lang="ru">' in response.text


def test_calculation_uses_backend(client):
    response = client.post("/api/calculate", json={"a": "1,5", "b": "2", "operation": "multiply"})
    assert response.status_code == 200
    assert response.json == {"result": 3.0, "display": "3"}


@pytest.mark.parametrize("a,b,operation", [("", 2, "add"), ("abc", 2, "add"), (True, 2, "add"), ("NaN", 2, "add"), ("Infinity", 2, "add"), (1e13, 2, "add"), (1, 0, "divide"), (1, 2, "pow"), (1, 2, []), (None, 2, "add"), (1, "1e-320", "divide")])
def test_invalid_calculations(client, a, b, operation):
    response = client.post("/api/calculate", json={"a": a, "b": b, "operation": operation})
    assert response.status_code == 400
    assert response.json["error"]


@pytest.mark.parametrize("body", [[], "invalid", None])
def test_calculator_requires_object(client, body):
    assert client.post("/api/calculate", json=body).status_code == 400


def test_login_session_and_logout(client):
    assert client.get("/account").status_code == 302
    bad = client.post("/login", data={"username": "student", "password": "bad"})
    assert bad.status_code == 401
    assert client.get("/account").status_code == 302
    good = client.post("/login", data={"username": "student", "password": "Test123!"}, follow_redirects=True)
    assert 'id="logout"' in good.text
    client.post("/logout")
    assert client.get("/account").status_code == 302


@pytest.mark.parametrize("validity", list(itertools.product([True, False], repeat=3)))
def test_contact_decision_matrix(client, validity):
    data = dict(zip(("name", "email", "message"), ("Иван", "ivan@example.com", "Тестовое сообщение")))
    for key, valid in zip(data, validity):
        if not valid:
            data[key] = ""
    response = client.post("/contact", data=data)
    assert response.status_code == (200 if all(validity) else 422)
    assert ('id="contact-success"' in response.text) == all(validity)


@pytest.mark.parametrize("field,value,valid", [("name", "А", False), ("name", "Аб", True), ("name", "А" * 60, True), ("name", "А" * 61, False), ("email", "a@b", False), ("email", "a b@c.ru", False), ("email", "a" * 115 + "@b.ru", True), ("email", "a" * 116 + "@b.ru", False), ("message", "x" * 9, False), ("message", "x" * 10, True), ("message", "x" * 1000, True), ("message", "x" * 1001, False)])
def test_contact_boundaries(client, field, value, valid):
    data = {"name": "Иван", "email": "ivan@example.com", "message": "Тестовое сообщение"}
    data[field] = value
    assert client.post("/contact", data=data).status_code == (200 if valid else 422)


def test_contact_escapes_html(client):
    response = client.post("/contact", data={"name": '<script>alert(1)</script>', "email": "", "message": ""})
    assert "<script>alert(1)</script>" not in response.text
    assert "&lt;script&gt;" in response.text


def test_health(client):
    assert client.get("/api/health").json == {"status": "ok", "service": "testing-lab", "storage": "none"}
