from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

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
        text_input.send_keys("The engineering design was beautiful and functional.")
        submit_btn = driver.find_element(By.ID, "submit-btn")
        submit_btn.click()
        time.sleep(4)
        result_output = driver.find_element(By.ID, "result-output")
        assert result_output.text != ""
    finally:
        driver.quit()

