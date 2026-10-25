from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)

    def open(self, path):
        self.driver.get(self.base_url + path)
        return self

    def element(self, element_id):
        return self.wait.until(EC.visibility_of_element_located((By.ID, element_id)))

    def fill(self, element_id, value):
        element = self.element(element_id)
        element.clear()
        element.send_keys(value)

    def click(self, element_id):
        self.wait.until(EC.element_to_be_clickable((By.ID, element_id))).click()
