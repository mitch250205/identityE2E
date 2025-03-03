import pytest
from pages.motorway_landing_page import MotorwayPage
from test_data.get_test_data import GetTestData
from config.config import CAR_INPUT_TXT_FILE

@pytest.mark.parametrize("number_plate, price", GetTestData().process_car_data_text_file(CAR_INPUT_TXT_FILE))
def test_car_valuation(browser, get_output_data, number_plate, price):
    """Test dynamically fetching car valuation data"""
    page = MotorwayPage(browser)
    page.accept_cookies()
    page.enter_car_registration(number_plate)
    page.click_get_free_valuation()

    # Wait for results to load and compare
    actual_details = page.get_car_details()
    #assert expected_details in actual_details, f"Expected {expected_details}, but got {actual_details}"
