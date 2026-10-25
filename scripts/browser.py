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
