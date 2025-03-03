import time
import pytest
from pages.motorway_landing_page import MotorwayPage
from pages.confused_landing_page import ConfusedPage
from test_data.get_test_data import GetTestData
from config.config import CAR_OUTPUT_TXT_FILE, CAR_INPUT_TXT_FILE


def get_year_from_plate(number_plate):
    """Extracts the year from a UK-style number plate."""
    if len(number_plate) < 4:
        return "Invalid plate format"

    try:
        year_part = int(number_plate[2:4])
        if 10 <= year_part < 20:
            return 2000 + year_part
        if 50 <= year_part < 60:
            return 2000 + (year_part % 10)
        if 60 <= year_part < 70:
            return 2010 + (year_part % 10)
        if 70 <= year_part < 80:
            return 2020 + (year_part % 10)
        return "Not in range 50-79"
    except ValueError:
        return "Invalid plate format"


# Load test data from input and output files
input_data = [row[0] for row in GetTestData(input_file_path=CAR_INPUT_TXT_FILE).get_data()]
output_data = {row[0]: row[1:] for row in GetTestData(output_file_path=CAR_OUTPUT_TXT_FILE).get_op_data()}


@pytest.mark.skip(reason="Temporarily disabled due to motorway.com restrictions")
@pytest.mark.parametrize("number_plate", input_data)
def test_motorway_car_valuation(browser, cookies_accepted, number_plate):
    """Validates the car valuation data on Motorway."""
    try:
        assert number_plate in output_data, f"❌ Missing expected output data for {number_plate}"
        expected_make, expected_model, expected_year = output_data[number_plate]
        page = MotorwayPage(browser)

        if not cookies_accepted["accepted"]:
            page.accept_cookies()
            cookies_accepted["accepted"] = True
        else:
            browser.refresh()

        page.enter_car_registration(number_plate)
        page.click_get_free_valuation()
        actual_details = page.get_car_details()
        actual_specifics = page.get_car_specifics()
        actual_year = actual_specifics.split("\n")[0].strip()

        expected_plate_year = get_year_from_plate(number_plate)

        assert actual_details.strip().lower() == f"{expected_make} {expected_model}".lower(), \
            f"❌ Mismatch! Expected '{expected_make} {expected_model}', but got '{actual_details.strip()}'"
        assert actual_year.strip() == expected_year.strip(), \
            f"❌ Year mismatch! Expected '{expected_year}', but got '{actual_year.strip()}'"
        assert str(expected_plate_year) == expected_year.strip(), \
            f"❌ Plate year mismatch! Expected '{expected_year}', derived '{expected_plate_year}'"
        time.sleep(60)
    except AssertionError as e:
        pytest.fail(str(e))


@pytest.mark.confused
@pytest.mark.parametrize("number_plate", input_data)
def test_confused_car_valuation(browser, cookies_accepted, number_plate):
    """Validates car valuation data on Confused.com."""
    try:
        assert number_plate in output_data, f"❌ Missing expected output data for {number_plate}"
        expected_make, expected_model, expected_year = output_data[number_plate]
        page = ConfusedPage(browser)

        if not cookies_accepted["accepted"]:
            page.accept_cookies()
            cookies_accepted["accepted"] = True
        else:
            browser.back()

        page.get_a_car_quote()
        page.enter_car_registration(number_plate)
        button = page.click_get_free_valuation()
        button.click()
        error_msg = page.get_error_message()

        if error_msg:
            browser.back()
            pytest.fail(f"❌ Confused.com error for '{number_plate}': {error_msg}")

        actual_year = page.get_car_year()
        actual_make = page.get_car_make()
        actual_model = page.get_car_model()
        expected_plate_year_full = str(get_year_from_plate(number_plate))

        assert expected_make.strip().lower() == actual_make.lower(), \
            f"❌ Make Mismatch! Expected '{expected_make}', but got '{actual_make.strip()}'"
        assert actual_year.strip() == expected_plate_year_full.strip(), \
            f"❌ Year Mismatch! Expected '{expected_plate_year_full}', but got '{actual_year.strip()}'"
        assert expected_model.strip().lower() in actual_model.strip().lower() or \
               actual_model.strip().lower() in expected_model.strip().lower(), \
            f"❌ Model Mismatch! Expected '{expected_make} {expected_model}', but got '{actual_make.strip()}'"

        page.change_car()
    except AssertionError as e:
        pytest.fail(str(e))