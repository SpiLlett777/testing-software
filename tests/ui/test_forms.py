import pytest
from selenium.webdriver.common.by import By
from tests.ui.pages.contact_page import ContactPage
from tests.ui.pages.login_page import LoginPage

pytestmark = pytest.mark.ui


def test_valid_login_and_logout(browser, base_url):
    page = LoginPage(browser, base_url).visit().login()
    assert page.element("logout").text == "Logout"
    assert page.element("login-success").text == "Вход выполнен успешно."
    page.click("logout")
    page.element("username")
    browser.get(base_url + "/account")
    assert browser.current_url.endswith("/login")


def test_invalid_login(browser, base_url):
    page = LoginPage(browser, base_url).visit().login(password="wrong")
    assert page.element("login-error").text == "Неверный логин или пароль."
    assert not browser.find_elements(By.ID, "logout")


def test_contact_success(browser, base_url):
    page = ContactPage(browser, base_url).visit().submit("Иван", "ivan@example.com", "Проверка контактной формы")
    assert page.element("contact-success").text == "Форма успешно отправлена."


@pytest.mark.parametrize("field,name,email,message,error", [
    ("name", "", "ivan@example.com", "Тестовое сообщение", "Имя должно содержать от 2 до 60 символов."),
    ("email", "Иван", "", "Тестовое сообщение", "Введите корректный email."),
    ("email", "Иван", "bad-email", "Тестовое сообщение", "Введите корректный email."),
    ("message", "Иван", "ivan@example.com", "", "Сообщение должно содержать от 10 до 1000 символов."),
])
def test_contact_invalid(browser, base_url, field, name, email, message, error):
    page = ContactPage(browser, base_url).visit().submit(name, email, message)
    assert page.error(field) == error
    assert not browser.find_elements(By.ID, "contact-success")
