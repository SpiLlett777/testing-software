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
