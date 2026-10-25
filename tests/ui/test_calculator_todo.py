import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from tests.ui.pages.base_page import BasePage

pytestmark = pytest.mark.ui


def test_calculator_and_clear(browser, base_url):
    page = BasePage(browser, base_url).open("/calculator")
    page.fill("number-a", "1,5")
    page.fill("number-b", "2")
    Select(page.element("operation")).select_by_value("multiply")
    page.click("calculate")
    page.wait.until(lambda _: page.element("result").text == "3")
    page.fill("number-b", "0")
    Select(page.element("operation")).select_by_value("divide")
    page.click("calculate")

    # ВНИМАНИЕ: Если бэкенд Flask возвращает другое сообщение,
    # замените эту строку на актуальный текст ошибки из вашего сервера.
    assert page.element("calculator-error").text == "Деление на ноль запрещено."

    page.click("clear")
    assert page.element("number-a").get_attribute("value") == ""
    assert page.element("number-b").get_attribute("value") == ""
    assert page.element("result").text == "—"
    assert Select(page.element("operation")).first_selected_option.get_attribute("value") == "add"


def add(page, title):
    page.fill("task-title", title)
    page.click("add-task")


def test_todo_fixed_filter_delete_persistence(browser, base_url):
    page = BasePage(browser, base_url).open("/todo")
    add(page, "Задача А")
    add(page, "Задача Б")
    browser.find_element(By.CSS_SELECTOR, "#task-list input").click()
    assert page.element("task-counter").text == "Активных: 1"
    browser.find_element(By.CSS_SELECTOR, '[data-filter="active"]').click()
    browser.find_element(By.CSS_SELECTOR, ".delete-task").click()
    browser.find_element(By.CSS_SELECTOR, '[data-filter="all"]').click()
    assert browser.find_element(By.CSS_SELECTOR, "#task-list label").text == "Задача А"
    browser.refresh()
    assert browser.find_element(By.CSS_SELECTOR, "#task-list label").text == "Задача А"
    assert browser.find_element(By.CSS_SELECTOR, "#task-list input").is_selected()
    page.click("reset-tasks")
    add(page, "   ")

    # ВНИМАНИЕ: Мы изменили этот текст в HTML-шаблоне! Проверяем обновленную версию:
    assert page.element("todo-error").text == "Введите задачу длиной от 1 до 120 символов."
    assert not browser.find_elements(By.CSS_SELECTOR, "#task-list li")


def test_todo_bug01_whitespace_reproduced(browser, base_url):
    page = BasePage(browser, base_url).open("/todo?mode=buggy")
    add(page, "   ")
    assert len(browser.find_elements(By.CSS_SELECTOR, "#task-list li")) == 1


def test_todo_bug02_counter_reproduced(browser, base_url):
    page = BasePage(browser, base_url).open("/todo?mode=buggy")
    add(page, "Задача А")
    browser.find_element(By.CSS_SELECTOR, "#task-list input").click()
    assert page.element("task-counter").text == "Активных: 1"


def test_todo_bug03_wrong_delete_reproduced(browser, base_url):
    page = BasePage(browser, base_url).open("/todo?mode=buggy")
    add(page, "Задача А")
    add(page, "Задача Б")
    browser.find_element(By.CSS_SELECTOR, "#task-list input").click()
    browser.find_element(By.CSS_SELECTOR, '[data-filter="active"]').click()
    browser.find_element(By.CSS_SELECTOR, ".delete-task").click()
    browser.find_element(By.CSS_SELECTOR, '[data-filter="all"]').click()
    assert browser.find_element(By.CSS_SELECTOR, "#task-list label").text == "Задача Б"


@pytest.mark.parametrize("width", [390, 1440])
def test_layout_no_horizontal_overflow(browser, base_url, width):
    browser.set_window_size(width, 1000)
    os.makedirs("artifacts/ui", exist_ok=True)
    for route in ("/", "/calculator", "/todo", "/login", "/contact"):
        browser.get(base_url + route)
        assert browser.execute_script("return document.documentElement.scrollWidth <= window.innerWidth"), route
        browser.save_screenshot(f"artifacts/ui/layout-{width}-{route.strip('/') or 'home'}.png")
