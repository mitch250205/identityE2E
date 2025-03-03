from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.config import FIVE_SEC_TIMEOUT, TEN_SEC_TIMEOUT


class MotorwayPage:
    def __init__(self, driver):
        self.driver = driver

    # Locators
    COOKIE_ACCEPT_BTN = (By.CLASS_NAME, "CookieWarning__dismiss-UVgy")
    CAR_REGISTRATION_INPUT = (By.ID, "vrm-input")
    GET_FREE_VALUATION_BTN = (By.CSS_SELECTOR, "[data-cy='valueButton']")

    CAR_DETAILS_RESULT = (By.XPATH, "//h1[@data-cy='vehicleMakeAndModel']")  # Adjust selector based on site structure
    CAR_SPECIFICS_RESULT = (By.CSS_SELECTOR, 'ul[data-cy="vehicleSpecifics"]')  # Adjust selector based on site structure


    def accept_cookies(self):
        try:
            WebDriverWait(self.driver, FIVE_SEC_TIMEOUT).until(EC.element_to_be_clickable(self.COOKIE_ACCEPT_BTN)).click()
        except:
            pass

    def enter_car_registration(self, reg_number):
        WebDriverWait(self.driver, FIVE_SEC_TIMEOUT).until(EC.visibility_of_element_located(self.CAR_REGISTRATION_INPUT)).send_keys(reg_number)

    def click_get_free_valuation(self):
        WebDriverWait(self.driver, FIVE_SEC_TIMEOUT).until(EC.element_to_be_clickable(self.GET_FREE_VALUATION_BTN)).click()

    def get_car_details(self):
        return WebDriverWait(self.driver, TEN_SEC_TIMEOUT).until(EC.visibility_of_element_located(self.CAR_DETAILS_RESULT)).text

    def get_car_specifics(self):
        return WebDriverWait(self.driver, TEN_SEC_TIMEOUT).until(EC.visibility_of_element_located(self.CAR_SPECIFICS_RESULT)).text

