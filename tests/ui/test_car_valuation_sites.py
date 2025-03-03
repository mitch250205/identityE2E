import time

import pytest
from pages.motorway_landing_page import MotorwayPage
from pages.confused_landing_page import ConfusedPage
from test_data.get_test_data import GetTestData
from config.config import CAR_OUTPUT_TXT_FILE
from config.config import CAR_INPUT_TXT_FILE


def get_year_from_plate(number_plate):
    """Extracts the year from a UK-style number plate."""
    if len(number_plate) < 4:
        return "Invalid plate format"  # Prevent out-of-range errors

    year_part = int(number_plate[2:4])  # Extract two-digit year
    if 10 <= year_part < 20:
        return 2000 + year_part
    if 50 <= year_part < 60:
        return 2000 + (year_part % 10)  # Extract last digit to determine year
    if 60 <= year_part < 70:
        return 2010 + (year_part % 10)
    if 70 <= year_part < 80:
        return 2020 + (year_part % 10)
    return "Not in range 50-79"

# Load test data from input and output files
input_data = [row[0] for row in GetTestData(input_file_path=CAR_INPUT_TXT_FILE).get_data()]  # Extract just the number plates
output_data = {row[0]: row[1:] for row in GetTestData(output_file_path=CAR_OUTPUT_TXT_FILE).get_op_data()}  # Dict {reg: (make, model, year)}

@pytest.mark.motorway
@pytest.mark.parametrize("number_plate", input_data)
def test_motorway_car_valuation(browser, cookies_accepted, number_plate):
    """Test dynamically fetching car valuation data and comparing against expected"""

    try:
        # Debugging: Ensure we are using the correct expected data
        print(f"Available number plates in output data: {list(output_data.keys())}")
        assert number_plate in output_data, f"❌ Missing expected output data for {number_plate}"

        expected_make, expected_model, expected_year = output_data[number_plate]

        # Navigate to the page
        page = MotorwayPage(browser)

        # ✅ Accept cookies only once, then refresh
        if not cookies_accepted["accepted"]:
            page.accept_cookies()
            cookies_accepted["accepted"] = True
        else:
            browser.refresh()

        page.enter_car_registration(number_plate)
        page.click_get_free_valuation()

        # ✅ Extract actual details from the website
        actual_details = page.get_car_details()
        actual_specifics = page.get_car_specifics()

        # ✅ Extract the year from the specifics
        actual_year = actual_specifics.split("\n")[0].strip()  # First item is the year

        # ✅ **Fix Year Calculation**
        expected_plate_year = int(number_plate[2:4])
        if expected_plate_year >= 50:
            expected_plate_year_full = str(1900 + expected_plate_year)  # e.g., '58' -> '2008'
        else:
            expected_plate_year_full = str(2000 + expected_plate_year)  # e.g., '18' -> '2018'

        # ✅ **Debugging Print Statements**
        print(f"\n--- VALIDATION START ---")
        print(f"Number Plate Under Test: {number_plate}")
        print(f"Expected Make/Model: {expected_make} {expected_model}")
        print(f"Expected Year: {expected_year} (Derived from plate: {expected_plate_year_full})")
        print(f"Actual Details from Site: {actual_details}")
        print(f"Actual Specifics from Site: {actual_specifics}")
        print(f"--- VALIDATION END ---\n")

        # ✅ **Assertions**
        assert actual_details.strip().lower() == f"{expected_make} {expected_model}".lower(), \
            f"❌ Mismatch! Expected '{expected_make} {expected_model}', but got '{actual_details.strip()}'"

        assert actual_year.strip() == expected_year.strip(), \
            f"❌ Mismatch in year! Expected '{expected_year}', but got '{actual_year.strip()}'"

        assert expected_plate_year_full == expected_year.strip(), \
            f"❌ Mismatch between number plate and expected year! '{number_plate}' should correspond to '{expected_year}', but derived '{expected_plate_year_full}'"
        time.sleep(60)
    except AssertionError as e:
        print(f"⚠️ Test failed for {number_plate}: {e}")
        pytest.fail(str(e))  # Continue running other tests


@pytest.mark.confused
@pytest.mark.parametrize("number_plate", input_data)
def test_confused_car_valuation(browser, cookies_accepted, number_plate):
    try:
        # Debugging: Ensure we are using the correct expected data
        print(f"Available number plates in output data: {list(output_data.keys())}")
        assert number_plate in output_data, f"❌ Missing number plate in the output data file for {number_plate}"

        expected_make, expected_model, expected_year = output_data[number_plate]

        # Navigate to the page
        page = ConfusedPage(browser)

        # ✅ Accept cookies only once, then refresh
        if not cookies_accepted["accepted"]:
            page.accept_cookies()
            cookies_accepted["accepted"] = True
        else:
            browser.back()
        page.get_a_car_quote()
        page.enter_car_registration(number_plate)
        page.click_get_free_valuation()
        error_msg = page.get_error_message()
        print(f"error_msg = {error_msg}")
        if error_msg:
            browser.back()
            assert error_msg == '' , \
                f"❌ Confused.com Cannot find the reg number Expected: '{number_plate}  gives error msg : {error_msg}'"
        else:
            actual_year = page.get_car_year()
            actual_make = page.get_car_make()
            actual_model = page.get_car_model()
            actual_reg = page.get_car_reg()

            # ✅ **Fix Year Calculation**
            expected_plate_year_full = str(get_year_from_plate(number_plate))

            assert expected_make.strip().lower() == actual_make.lower(), \
                f"❌ Make Mismatch! Expected '{expected_make}', but got '{actual_make.strip()}'"
            assert actual_year.strip() == expected_plate_year_full.strip(), \
                f"❌ Year Mismatch in year! Expected '{expected_plate_year_full}', but got '{actual_year.strip()}'"
            assert expected_model.strip().lower() in actual_model.strip().lower() or \
                   actual_model.strip().lower() in expected_model.strip().lower(), \
                f"❌ Model Mismatch! Expected '{expected_make} {expected_model}', but got '{actual_make.strip()}'"
            page.change_car()
        print(f"ENDING ")

    except AssertionError as e:
        print(f"⚠️ Test failed for {number_plate}: {e}")
        pytest.fail(str(e))  # Continue running other tests
