from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:

    COMPANY_CODE = (By.ID, "companycode")
    USERNAME = (By.ID, "signin-username")
    PASSWORD = (By.ID, "signin-password")
    SIGNIN_BTN = (By.XPATH, "//button[@type='submit']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def open(self, url):
        self.driver.get(url)
        self.wait.until(
            EC.presence_of_element_located(self.COMPANY_CODE)
        )

    def enter_company_code(self, value):
        field = self.wait.until(
            EC.presence_of_element_located(self.COMPANY_CODE)
        )
        field.clear()
        field.send_keys(value)

    def enter_username(self, value):
        self.wait.until(
            EC.presence_of_element_located(self.USERNAME)
        ).send_keys(value)

    def enter_password(self, value):
        self.wait.until(
            EC.presence_of_element_located(self.PASSWORD)
        ).send_keys(value)

    def click_signin(self):
        self.wait.until(
            EC.element_to_be_clickable(self.SIGNIN_BTN)
        ).click()

    def validate_login_success(self):
        self.wait.until(
            lambda d: "dashboard" in d.current_url or "home" in d.current_url
        )
        assert "dashboard" in self.driver.current_url or "home" in self.driver.current_url