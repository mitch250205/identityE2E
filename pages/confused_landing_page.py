from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import Optional

from config.config import FIVE_SEC_TIMEOUT, TEN_SEC_TIMEOUT
from tests.conftest import browser


class ConfusedPage:
    def __init__(self, driver) -> None:
        self.driver = driver

    # 🔹 Reusable Method for Element Waits
    def wait_for_element(self, locator, timeout=15, condition=EC.visibility_of_element_located) -> Optional[WebElement]:
        """Generic method to wait for an element with a specified condition."""
        try:
            return WebDriverWait(self.driver, timeout).until(condition(locator))
        except TimeoutException:
            return None

    # ✅ **Locators**
    # ────────────────────────────────────────────────────────────────────────
    # 📌 General UI Elements
    COOKIE_ACCEPT_BTN = (By.ID, "button-save-all")
    GET_A_QUOTE = (By.XPATH, "//span[text()='Get a car quote']")
    GET_FREE_VALUATION_BTN = (By.ID, "find-vehicle-btn")
    CHANGE_CAR = (By.XPATH, "//span[text()='Change vehicle']")

    # 📌 Input Fields
    CAR_REGISTRATION_INPUT = (By.ID, "registration-number-input")

    # 📌 Error Messages
    BAD_REG_ERROR_MESSAGE_LOCATOR = (By.CLASS_NAME, "error-summary__heading")

    # 📌 Car Details
    CAR_DETAILS_RESULT = (By.XPATH, "//h1[@data-cy='vehicleMakeAndModel']")
    CAR_SPECIFICS_RESULT = (By.CSS_SELECTOR, 'ul[data-cy="vehicleSpecifics"]')

    # 📌 Car Info Elements
    REG = (By.XPATH, "//p[@id='vehicleSummaryRegNumber']/b")
    MAKE = (By.XPATH, "//div[@class='panel']/p[contains(text(), 'Manufacturer')]/b")
    MODEL = (By.XPATH, "//div[@class='panel']/p[contains(text(), 'Model')]/b")
    YEAR = (By.XPATH, "//div[@class='panel']/p[contains(text(), 'Year')]/b")

    # ✅ **Methods**
    # ────────────────────────────────────────────────────────────────────────
    def dismiss_popup(self) -> None:
        """Handles the unexpected AI helper pop-up if it appears."""
        try:
            # Wait for the textarea to be visible (adjust the locator if needed)
            popup_element = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'textarea')]//textarea"))

            )
            print("Popup detected! Dismissing...")
            self.driver.back()
            WebDriverWait(self.driver, 2).until(EC.invisibility_of_element_located(
                (By.XPATH, "//div[contains(@class, 'textarea')]//textarea")))
            print("Popup dismissed!")
        except:
            print("No AI helper popup detected, continuing test...")

    def accept_cookies(self)-> None:
        """Accepts cookies if the button is visible."""
        if self.wait_for_element(self.COOKIE_ACCEPT_BTN):
            self.driver.find_element(*self.COOKIE_ACCEPT_BTN).click()

    def get_a_car_quote(self)-> None:
        """Clicks the 'Get a car quote' button."""
        self.wait_for_element(self.GET_A_QUOTE, condition=EC.element_to_be_clickable).click()

    def enter_car_registration(self, reg_number)-> None:
        """Enters the car registration number."""
        self.dismiss_popup()

        input_field = self.wait_for_element(self.CAR_REGISTRATION_INPUT)
        if input_field:
            input_field.clear()
            input_field.send_keys(reg_number)

    def click_get_free_valuation(self) -> None:
        """Clicks the 'Get Free Valuation' button."""
        return self.wait_for_element(self.GET_FREE_VALUATION_BTN,
                              condition=EC.element_to_be_clickable)

    def change_car(self) -> None:
        """Clicks the 'Change vehicle' button."""
        self.wait_for_element(self.CHANGE_CAR, condition=EC.element_to_be_clickable).click()

    def get_error_message(self) -> Optional[str]:
        """Returns the error message text if present, else None."""
        error_element = self.wait_for_element(self.BAD_REG_ERROR_MESSAGE_LOCATOR, timeout=TEN_SEC_TIMEOUT)
        return error_element.text if error_element else None

    # ✅ **Car Details Retrieval Methods**
    # ────────────────────────────────────────────────────────────────────────
    def get_car_reg(self)-> Optional[str]:
        return self.wait_for_element(self.REG, timeout=TEN_SEC_TIMEOUT).text

    def get_car_make(self)-> Optional[str]:
        return self.wait_for_element(self.MAKE, timeout=TEN_SEC_TIMEOUT).text

    def get_car_model(self)-> Optional[str]:
        return self.wait_for_element(self.MODEL, timeout=TEN_SEC_TIMEOUT).text

    def get_car_year(self)-> Optional[str]:
        return self.wait_for_element(self.YEAR, timeout=TEN_SEC_TIMEOUT).text
