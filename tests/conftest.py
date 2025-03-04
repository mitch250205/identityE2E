import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.ie.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from typing import Dict, Generator, Optional
from config.config import BASE_URL, HEADLESS_MODE
from config.config import CAR_OUTPUT_TXT_FILE
from test_data.get_test_data import GetTestData

@pytest.fixture(scope="session")
def browser() -> Generator[WebDriver,None,None]:
    """ Setup Selenium WebDriver """
    options = Options()
    if HEADLESS_MODE:
        options.add_argument("--headless")  # Run headless for CI/CD
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)
    driver.get(BASE_URL)

    yield driver  # Provide driver instance to tests

    driver.quit()  # Cleanup after tests complete



@pytest.fixture(scope="session")
def get_output_test_data() -> Dict[str,bool]:
    test_data = GetTestData(output_file_path=CAR_OUTPUT_TXT_FILE,input_file_path=None)
    return test_data.get_op_data()

@pytest.fixture(scope="session")
def cookies_accepted() -> Dict[str,bool]:
    """Fixture to track whether cookies have been accepted."""
    return {"accepted": False}

