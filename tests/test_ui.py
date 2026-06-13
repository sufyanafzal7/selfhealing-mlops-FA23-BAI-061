from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pytest

def test_web_ui_flow():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Initialize webdriver using local system binary parameters
    driver = webdriver.Chrome(options=chrome_options)
    try:
        # Check local instance deployment entry point mapping
        driver.get("http://localhost:8000/")
        time.sleep(2)
        # Locate text area entry space
        textarea = driver.find_element(By.TAG_NAME, "textarea")
        textarea.send_keys("The cinematography was breathtaking and the performances were outstanding")
        button = driver.find_element(By.TAG_NAME, "button")
        button.click()
        time.sleep(3)
        # Validate that the result structural component appears on the page
        result_div = driver.find_element(By.ID, "result")
        assert result_div is not None
        assert "Predicted Class:" in driver.page_source
    finally:
        driver.quit()

