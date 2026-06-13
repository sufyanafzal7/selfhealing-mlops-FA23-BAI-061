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
    driver = webdriver.Chrome(options=chrome_options)
    try:
        # Route testing through the explicit Flask application port 5000
        driver.get("http://localhost:5000/")
        time.sleep(3)
        # Locate elements using the mandatory project IDs
        text_input = driver.find_element(By.ID, "text-input")
        text_input.send_keys("The cinematography was breathtaking and the performances were outstanding")
        submit_btn = driver.find_element(By.ID, "submit-btn")
        submit_btn.click()
        time.sleep(4)
        # Validate the exact result-output div container content rules
        result_output = driver.find_element(By.ID, "result-output")
        result_text = result_output.text
        assert result_text != ""
        assert any(word in result_text for word in ["POSITIVE", "NEGATIVE", "Confidence"])
    finally:
        driver.quit()
