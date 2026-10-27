# Лабораторная работа 9. GitHub Actions

Подготовлен `.github/workflows/run-tests.yml`: push, pull_request и workflow_dispatch; runner Ubuntu; Python 3.13;
установка зависимостей; pytest unit+UI; выгрузка artifacts при любом исходе. Временный сервер для UI запускает pytest
fixture. ChromeDriver подбирается webdriver-manager. Публичные API-тесты запускаются отдельным job при
workflow_dispatch, чтобы зависимость от чужого сервиса не делала каждый push нестабильным.

## Действия для выполнения работы

1. Создать **публичный** пустой репозиторий в своем GitHub-аккаунте.
2. Проверить `.gitignore`: не включать .venv, tools/bin, учетные данные и реальные секреты.
3. Из корня проекта выполнить команды, заменив OWNER/REPOSITORY реальными значениями:

```powershell
git init
git add .
git commit -m "Add testing lab application and automated tests"
git branch -M main
git remote add origin https://github.com/OWNER/REPOSITORY.git
git push -u origin main
```

4. Открыть Actions, дождаться выполнения workflow. При ошибке изучить лог, исправить причину, сделать новый commit/push.
5. Сохранить ссылку на успешный run, commit SHA, скриншот зеленого статуса и скачать test-results.

Эта инструкция рассчитана на каталог без существующего Git-репозитория. Если репозиторий/remote уже есть, использовать
его, не переинициализировать и не переписывать историю.

## Фактический статус

YAML подготовлен. Публикация и запуск на GitHub не выполнялись; ссылка на реальный успешный run отсутствует. Локальные
результаты не являются доказательством завершения ЛР 9.

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

### .github/workflows/run-tests.yml

SHA-256: `780055965fec6c4fee9bb2ed9abdf7f3f80b8c57b55fbb467959554b8e974886`

```yaml
name: Python and Selenium tests
on:
  push:
  pull_request:
  workflow_dispatch:
permissions:
  contents: read
jobs:
  local-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
          cache: pip
      - run: python -m pip install -r requirements-dev.txt
      - name: Unit and UI tests (fixture starts local server)
        run: python -m pytest tests/unit tests/ui --run-ui --junitxml=artifacts/ci/results.xml
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results
          path: artifacts/
  public-api:
    if: github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - run: python -m pip install -r requirements-dev.txt
      - run: python -m pytest tests/api --run-api --junitxml=artifacts/ci/api.xml
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: public-api-results
          path: artifacts/

```

### requirements.txt

SHA-256: `05b055cad237ae3212058d5a2f632537c5bc4a0a6b4d67927778fd11382dd4f8`

```text
Flask==3.1.3
waitress==3.0.2

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

### pytest.ini

SHA-256: `56b6f95f29f5f66776e4700342b0f4c8e4d2e3d5e577bd7d0177f96c2f72fadb`

```text
[pytest]
testpaths = tests
pythonpath = .
addopts = -ra
markers =
    ui: Browser tests (requires --run-ui)
    api: Public API tests (requires --run-api)

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

### scripts/browser.py

SHA-256: `c2d6702a0011a5af26185cbd3782261f0bafa57ec96fa1c5011e89e21408012b`

```python
"""One WebDriver factory used by lab 3's script and pytest fixtures."""
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager


def create_browser(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--lang=ru")
    driver_path = os.environ.get("CHROMEDRIVER")
    if not driver_path and Path("tools/bin/chromedriver.exe").exists():
        driver_path = str(Path("tools/bin/chromedriver.exe").resolve())
    if not driver_path:
        driver_path = ChromeDriverManager(cache_manager=DriverCacheManager(root_dir="tools/bin")).install()
    driver = webdriver.Chrome(service=Service(driver_path), options=options)
    driver.set_page_load_timeout(30)
    return driver

```

### tests/unit/test_calculator.py

SHA-256: `3a50e6c2a952e4a657ab2a71533990049a49924712f92d364e8e2a00beaab703`

```python
import pytest
from app.calculator import Calculator


@pytest.mark.parametrize("method,a,b,expected", [
    ("add", 2, 3, 5), ("add", -2, -3, -5), ("add", .1, .2, .3),
    ("subtract", 5, 8, -3), ("subtract", -4, -4, 0), ("subtract", 0, 2, -2),
    ("multiply", 6, 7, 42), ("multiply", -2, 3, -6), ("multiply", 0, 999, 0),
    ("divide", 8, 2, 4), ("divide", 1, 4, .25), ("divide", -9, 3, -3),
    ("divide", 0, 5, 0), ("add", 10**12, 10**12, 2 * 10**12),
])
def test_arithmetic(method, a, b, expected):
    assert getattr(Calculator, method)(a, b) == pytest.approx(expected)


@pytest.mark.parametrize("a", [0, 1, -1, .5])
def test_division_by_zero(a):
    with pytest.raises(ZeroDivisionError, match="Деление на ноль"):
        Calculator.divide(a, 0)


@pytest.mark.parametrize("number,expected", [(-7, False), (0, False), (1, False), (2, True), (3, True), (4, False), (9, False), (25, False), (97, True)])
def test_prime(number, expected):
    assert Calculator.is_prime_number(number) is expected


@pytest.mark.parametrize("value", [2.5, "3", None, True])
def test_prime_rejects_non_integer(value):
    with pytest.raises(TypeError):
        Calculator.is_prime_number(value)

```
