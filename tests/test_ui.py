from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pytest

def test_frontend_sentiment():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get("http://localhost:5000/")
        time.sleep(3)
        text_input = driver.find_element(By.ID, "text-input")
        text_input.send_keys("The cinematography was breathtaking and the performances were outstanding")
        submit_btn = driver.find_element(By.ID, "submit-btn")
        submit_btn.click()
        time.sleep(4)
        result_output = driver.find_element(By.ID, "result-output")
        result_text = result_output.text
        assert result_text != ""
        assert any(word in result_text for word in ["POSITIVE", "NEGATIVE", "Confidence"])
    finally:
        driver.quit()
