from .base_page import BasePage


class ContactPage(BasePage):
    def visit(self):
        return self.open("/contact")

    def submit(self, name, email, message):
        for key, value in (("name", name), ("email", email), ("message", message)):
            self.fill(key, value)
        self.click("contact-submit")
        return self

    def error(self, field):
        return self.element(f"{field}-error").text
