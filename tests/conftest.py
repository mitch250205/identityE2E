import names
import pytest
import requests
import random
import string
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pages.motorway_landing_page import MotorwayPage
from pages.mileage_car_data_page import MotorwayMileagePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import BASE_URL
from config.config import CAR_INPUT_TXT_FILE
from test_data.get_test_data import GetTestData

@pytest.fixture(scope="session")
def browser():
    """ Setup Selenium WebDriver """
    options = Options()
    #options.add_argument("--headless")  # Run headless for CI/CD
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)
    driver.get(BASE_URL)

    yield driver  # Provide driver instance to tests

    driver.quit()  # Cleanup after tests complete

@pytest.fixture(scope="session")
def get_input_data():
    GetTestData().process_car_data_text_file(CAR_INPUT_TXT_FILE)
    return GetTestData.get_test_data_json

@pytest.fixture(scope="session")
def get_output_data():
    GetTestData().process_output_text_file(CAR_OUTPUT_TXT_FILE)
    return GetTestData.get_test_data_json