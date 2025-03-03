from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.config import FIVE_SEC_TIMEOUT, TEN_SEC_TIMEOUT


class ConfusedPage:
    def __init__(self, driver):
        self.driver = driver

    # Locators
    BAD_REG_ERROR_MESSAGE_LOCATOR = (By.CLASS_NAME, "error-summary__heading")

    COOKIE_ACCEPT_BTN = (By.ID, "button-save-all")

    CAR_REGISTRATION_INPUT = (By.ID, "registration-number-input")

    GET_FREE_VALUATION_BTN = (By.ID, "find-vehicle-btn")

    GET_A_QUOTE = (By.XPATH, "//span[text()='Get a car quote']")


    CAR_DETAILS_RESULT = (By.XPATH, "//h1[@data-cy='vehicleMakeAndModel']")  # Adjust selector based on site structure
    CAR_SPECIFICS_RESULT = (By.CSS_SELECTOR, 'ul[data-cy="vehicleSpecifics"]')  # Adjust selector based on site structure

    REG = (By.XPATH, "//p[@id='vehicleSummaryRegNumber']/b")
    MAKE = (By.XPATH, "//div[@class='panel']/p[contains(text(), 'Manufacturer')]/b")
    MODEL = (By.XPATH, "//div[@class='panel']/p[contains(text(), 'Model')]/b")
    YEAR = (By.XPATH, "//div[@class='panel']/p[contains(text(), 'Year')]/b")
    CHANGE_CAR = (By.XPATH, "//span[text()='Change vehicle']")

    def accept_cookies(self):
        try:
            WebDriverWait(self.driver, FIVE_SEC_TIMEOUT).until(EC.element_to_be_clickable(self.COOKIE_ACCEPT_BTN)).click()
        except:
            pass

    def get_a_car_quote(self):
        return WebDriverWait(self.driver, FIVE_SEC_TIMEOUT).until(EC.visibility_of_element_located(self.GET_A_QUOTE)).click()


    def enter_car_registration(self, reg_number):
        WebDriverWait(self.driver, FIVE_SEC_TIMEOUT).until(EC.visibility_of_element_located(self.CAR_REGISTRATION_INPUT)).send_keys(reg_number)

    def click_get_free_valuation(self):
        WebDriverWait(self.driver, FIVE_SEC_TIMEOUT).until(EC.element_to_be_clickable(self.GET_FREE_VALUATION_BTN)).click()

    def get_car_reg(self):
        return WebDriverWait(self.driver, TEN_SEC_TIMEOUT).until(EC.visibility_of_element_located(self.REG)).text

    def get_car_make(self):
        return WebDriverWait(self.driver, TEN_SEC_TIMEOUT).until(EC.visibility_of_element_located(self.MAKE)).text

    def get_car_model(self):
        return WebDriverWait(self.driver, TEN_SEC_TIMEOUT).until(EC.visibility_of_element_located(self.MODEL)).text

    def get_car_year(self):
        return WebDriverWait(self.driver, TEN_SEC_TIMEOUT).until(EC.visibility_of_element_located(self.YEAR)).text

    def change_car(self):
        return WebDriverWait(self.driver, TEN_SEC_TIMEOUT).until(EC.visibility_of_element_located(self.CHANGE_CAR)).click()

    def get_error_message(self):
        """Returns the error message text if present, else None."""
        try:
            error_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.BAD_REG_ERROR_MESSAGE_LOCATOR)
            )
            return error_element.text  # Return the error message text
        except:
            return None  # No error message found
