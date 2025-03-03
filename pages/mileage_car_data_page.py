from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MotorwayMileagePage:
    def __init__(self, driver):
        self.driver = driver

    # Locators
    COOKIE_ACCEPT_BTN = (By.ID, "onetrust-accept-btn-handler")  # Cookie acceptance button
    CAR_REGISTRATION_INPUT = (By.ID, "registration")  # Car registration input field
    CAR_MILEAGE_INPUT = (By.ID, "mileage")  # Car mileage input field
    GET_FREE_VALUATION_BTN = (By.XPATH, "//button[contains(text(), 'Get your free valuation')]")  # Valuation button
    HOW_IT_WORKS_LINK = (By.LINK_TEXT, "How it works")  # "How it works" link
    HELP_LINK = (By.LINK_TEXT, "Help")  # Help section link
    SIGN_IN_LINK = (By.LINK_TEXT, "Sign in")  # Sign in link
    FOOTER_PRIVACY_POLICY = (By.LINK_TEXT, "Privacy Policy")  # Footer Privacy Policy link
    FOOTER_TERMS_CONDITIONS = (By.LINK_TEXT, "Terms & Conditions")  # Footer Terms & Conditions link

    # Methods
    def accept_cookies(self):
        """Click the accept cookies button"""
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.COOKIE_ACCEPT_BTN)).click()
        except:
            pass  # If the cookie button is not present, continue without failing

    def enter_car_registration(self, reg_number):
        """Enter a car registration number"""
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.CAR_REGISTRATION_INPUT)).send_keys(reg_number)

    def enter_car_mileage(self, mileage):
        """Enter the car's mileage"""
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.CAR_MILEAGE_INPUT)).send_keys(mileage)

    def click_get_free_valuation(self):
        """Click the button to get a car valuation"""
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.GET_FREE_VALUATION_BTN)).click()

    def go_to_how_it_works(self):
        """Navigate to the 'How it works' page"""
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.HOW_IT_WORKS_LINK)).click()

    def go_to_help(self):
        """Navigate to the Help page"""
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.HELP_LINK)).click()

    def go_to_sign_in(self):
        """Navigate to the Sign In page"""
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.SIGN_IN_LINK)).click()

    def go_to_privacy_policy(self):
        """Navigate to the Privacy Policy page"""
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.FOOTER_PRIVACY_POLICY)).click()

    def go_to_terms_conditions(self):
        """Navigate to the Terms & Conditions page"""
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.FOOTER_TERMS_CONDITIONS)).click()
