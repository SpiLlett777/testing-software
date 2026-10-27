# Лабораторная работа 5. REST API

Объект: https://jsonplaceholder.typicode.com. Собственное API для этой работы не требуется. Контракт фиктивного
сохранения: https://jsonplaceholder.typicode.com/guide/.

| Метод/путь   | Назначение            | Ожидаемые проверки                                              |
|--------------|-----------------------|-----------------------------------------------------------------|
| GET /users/1 | Получить пользователя | 200; id=1; непустое имя; email содержит @; address — объект     |
| POST /users  | Создать пользователя  | 201; целочисленный id; name, username, email равны отправленным |
| PUT /users/1 | Обновить пользователя | 200; id=1; новое имя; остальные отправленные поля совпадают     |

Postman-коллекция содержит JS-assertions статуса, структуры и значений. Тесты Python повторяют логику через requests и
pytest, timeout=30 секунд. Запросы независимы: POST не создает постоянного ресурса, поэтому GET после POST не
используется как проверка сохранения.

## Ручная часть

1. Импортировать collection и environment из postman.
2. Выбрать окружение «ЛР 5 — JSONPlaceholder».
3. Поочередно выполнить запросы, изучить JSON и Test Results.
4. Выполнить Run collection (1 итерация, все три запроса).
5. Сохранить экспорт результата и скриншот с количеством успешных/неуспешных проверок.
6. Сравнить результаты с pytest и пояснить расхождения, если есть.

Фактические статусы запусков — в STATUS. Запуск Newman, если выполнен, подтверждает коллекцию, но не выдается за запуск
интерфейса Postman. При сетевой ошибке фиксировать ее как ошибку окружения, а не успешный результат API.

## Общий статус выполнения на момент сборки

# Статус на 18.09.2026

После просьбы пользователя оставить прогоны ему новые тесты не запускались. Ниже зафиксированы только уже полученные
результаты.

## Готово

- Собственный веб-стенд без БД: калькулятор, Todo (исправный и намеренно дефектный), логин/Logout, контактная форма,
  health API.
- Тест-план, чек-листы, 10 тест-кейсов калькулятора, 3 баг-репорта, анализ селекторов, матрица решений.
- Unit/серверные, Selenium Page Object и requests-тесты; Postman-коллекция с окружением; k6-скрипт; GitHub Actions YAML.
- Инструкции запуска и сборщик Markdown-отчетов с полными листингами.

## Фактические запуски

| Набор                          | Результат                                                                                                                                              | Доказательство                                                |
|--------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------|
| Calculator: чистые unit-тесты  | 31 passed                                                                                                                                              | artifacts/lab06/unit.xml                                      |
| Серверные проверки             | 44 passed                                                                                                                                              | artifacts/lab06/unit.xml                                      |
| Selenium Chrome                | 14 passed; включает 3 проверки воспроизводимости намеренных дефектов и 2 проверки адаптивной компоновки                                                | artifacts/ui/results.xml, скриншоты artifacts/ui              |
| Публичное API, Python          | 3 passed                                                                                                                                               | artifacts/lab05/python-api.xml                                |
| Postman-коллекция через Newman | Первый прогон: 3 запроса с ожидаемыми статусами, 3 ошибки JS из-за имени data; переменная переименована в responseBody, повторный запуск не выполнялся | artifacts/lab05/newman.json содержит результат ДО исправления |
| k6, 10 VUs × 30s               | 2960 запросов, 98.47 req/s, среднее 1.06 мс, p95 2.14 мс, 0% HTTP-ошибок, 5920/5920 успешных проверок                                                  | artifacts/lab08/10vu.json                                     |
| k6, 50 VUs × 10s               | Не запускался                                                                                                                                          | Скрипт и команда готовы                                       |

UI запуск выполнен на Chrome 153.0.8010.48 / ChromeDriver 153.0.8010.52. Окружение: Windows 10, Python 3.14.0;
подробности в artifacts/environment.json. Визуально просмотрен снимок главной страницы на ширине 1440; автоматическая
проверка переполнения выполнена на 390 и 1440 для пяти страниц. Это не полноценный аудит доступности и не мобильная ЛР

7.

Первоначальные попытки скачивания драйвера блокировались сетевыми ограничениями; после загрузки из официального
источника весь UI-набор прошел. В API-прогоне был warning записи pytest cache, который не повлиял на проверки.
Нагрузочный прогон выполнялся одновременно с частью служебных операций на той же машине; это нужно учитывать при
интерпретации малых задержек.

## Остается выполнить для сдачи

- Ручной прогон чек-листов и исследовательская сессия ЛР 2; заполнение фактических результатов. Автотесты не выданы за
  ручную работу.
- Проверка исправленной коллекции, запуск через Postman Collection Runner и сохранение результатов.
- Второй профиль k6 и сравнение двух результатов (`python -m scripts.summarize_load`).
- Публикация публичного GitHub-репозитория и подтверждение успешного GitHub Actions run.
- Титульные листы и оформление отчетов по требованиям преподавателя.
- ЛР 7 — мобильное приложение — вне текущего веб-этапа.

Дополнительная утилита Newman использует зависимости, для которых npm сообщил 19 уязвимостей даже в установленной 6.2.2.
Она не подключена к веб-приложению и нужна только для необязательного CLI-прогона коллекции. Основной путь ЛР 5 — импорт
коллекции в Postman. Автоматические несовместимые обновления зависимостей не применялись.

## Приложение. Листинги исходного кода

### tests/api/test_public_api.py

SHA-256: `c013000f7b1807c4b6731cc5b48f4dce2d12c2fd91cedd905d4a45dd67af3a80`

```python
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

```

### postman/lab05.collection.json

SHA-256: `48a03181772989e672d7f8e485f8f22da8763643dfed2a99bb3c2979c850ccbc`

```json
{
  "info": {
    "name": "ЛР 5 — REST API",
    "description": "GET, POST, PUT и проверки ответов. Запись в JSONPlaceholder имитируется.",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "GET — получить пользователя",
      "request": {
        "method": "GET",
        "header": [],
        "url": "{{base_url}}/users/1"
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "pm.test('Status 200', () => pm.response.to.have.status(200));",
              "const responseBody = pm.response.json();",
              "pm.test('User structure', () => { pm.expect(responseBody).to.be.an('object'); pm.expect(responseBody.name).to.be.a('string').and.not.empty; pm.expect(responseBody.email).to.be.a('string').and.include('@'); pm.expect(responseBody.address).to.be.an('object'); });",
              "pm.test('Requested user id', () => pm.expect(responseBody.id).to.eql(1));"
            ]
          }
        }
      ]
    },
    {
      "name": "POST — создать пользователя",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "url": "{{base_url}}/users",
        "body": {
          "mode": "raw",
          "raw": "{\n  \"name\": \"Test Student\",\n  \"username\": \"student\",\n  \"email\": \"student@example.com\"\n}",
          "options": {
            "raw": {
              "language": "json"
            }
          }
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "pm.test('Status 201', () => pm.response.to.have.status(201));",
              "const responseBody = pm.response.json();",
              "pm.test('Created user structure', () => { pm.expect(responseBody).to.be.an('object'); pm.expect(Number.isInteger(responseBody.id)).to.eql(true); });",
              "pm.test('Created user values', () => { pm.expect(responseBody.name).to.eql('Test Student'); pm.expect(responseBody.username).to.eql('student'); pm.expect(responseBody.email).to.eql('student@example.com'); });"
            ]
          }
        }
      ]
    },
    {
      "name": "PUT — обновить пользователя",
      "request": {
        "method": "PUT",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "url": "{{base_url}}/users/1",
        "body": {
          "mode": "raw",
          "raw": "{\n  \"name\": \"Updated Student\",\n  \"username\": \"student\",\n  \"email\": \"student@example.com\"\n}",
          "options": {
            "raw": {
              "language": "json"
            }
          }
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "pm.test('Status 200', () => pm.response.to.have.status(200));",
              "const responseBody = pm.response.json();",
              "pm.test('Updated user structure', () => { pm.expect(responseBody).to.be.an('object'); pm.expect(responseBody.id).to.be.a('number'); pm.expect(responseBody.name).to.be.a('string'); pm.expect(responseBody.username).to.be.a('string'); pm.expect(responseBody.email).to.be.a('string'); });",
              "pm.test('Updated user values', () => { pm.expect(responseBody.id).to.eql(1); pm.expect(responseBody.name).to.eql('Updated Student'); pm.expect(responseBody.username).to.eql('student'); pm.expect(responseBody.email).to.eql('student@example.com'); });"
            ]
          }
        }
      ]
    }
  ]
}

```

### postman/lab05.environment.json

SHA-256: `ba30abb52eb952c0d333639ec5fd72c01c766d561cac418481f58f60256f9c95`

```json
{
  "name": "ЛР 5 — JSONPlaceholder",
  "values": [
    {
      "key": "base_url",
      "value": "https://jsonplaceholder.typicode.com",
      "enabled": true
    }
  ],
  "_postman_variable_scope": "environment"
}

```

### requirements-dev.txt

SHA-256: `c91ce27370688b171fe6d98243a3351c7e10ae687ff951be1ee0f6df37eb5e9a`

```text
-r requirements.txt
pytest==9.1.1
selenium==4.49.0
webdriver-manager==4.1.2
requests==2.34.2

```

### requirements.txt

SHA-256: `05b055cad237ae3212058d5a2f632537c5bc4a0a6b4d67927778fd11382dd4f8`

```text
Flask==3.1.3
waitress==3.0.2

```

### tests/conftest.py

SHA-256: `1b325add053e8a89f94e9d4d9da66f5126d4b4baed73835093e350de26eaa715`

```python
from pathlib import Path
import hashlib
import re
import threading

import pytest
from werkzeug.serving import make_server

from app import create_app


def pytest_addoption(parser):
    parser.addoption("--run-ui", action="store_true", help="Run Selenium Chrome tests")
    parser.addoption("--run-api", action="store_true", help="Run tests against public JSONPlaceholder")
    parser.addoption("--headed", action="store_true", help="Show Chrome window")


def pytest_collection_modifyitems(config, items):
    for item in items:
        for marker, option in (("ui", "--run-ui"), ("api", "--run-api")):
            if marker in item.keywords and not config.getoption(option):
                item.add_marker(pytest.mark.skip(reason=f"Enable with {option}"))


@pytest.fixture
def app():
    return create_app({"TESTING": True, "SECRET_KEY": "test-only-key"})


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def base_url():
    server = make_server("127.0.0.1", 0, create_app({"TESTING": True, "SECRET_KEY": "ui-test-key"}), threaded=True)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()
    thread.join(timeout=5)
    server.server_close()


@pytest.fixture
def browser(request):
    from scripts.browser import create_browser
    driver = create_browser(headless=not request.config.getoption("--headed"))
    folder = Path("artifacts/ui")
    folder.mkdir(parents=True, exist_ok=True)
    yield driver
    try:
        name = re.sub(r"[^a-zA-Z0-9_-]", "_", request.node.originalname or request.node.name)
        suffix = hashlib.sha256(request.node.nodeid.encode()).hexdigest()[:8]
        driver.save_screenshot(str(folder / f"{name}-{suffix}.png"))
    finally:
        driver.quit()

```
