from .base_page import BasePage


class LoginPage(BasePage):
    def visit(self):
        return self.open("/login")

    def login(self, username="student", password="Test123!"):
        self.fill("username", username)
        self.fill("password", password)
        self.click("login-submit")
        return self
