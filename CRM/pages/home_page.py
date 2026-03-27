from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePage:

    # Sidebar toggle (hamburger)
    SIDEBAR_TOGGLE = (
        By.XPATH,
        "//a[contains(@class,'sidemenu-toggle')]"
    )

    # CRM main menu
    CRM_MENU = (
        By.XPATH,
        "//span[normalize-space()='CRM']/parent::a"
    )

    # Submenu options
    CREATE_ENQUIRY = (By.ID, "nav-crm-create-enquiry")
    CREATE_QUOTATION = (By.ID, "nav-crm-create-quotation")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # ---------------- Sidebar ----------------
    def open_sidebar(self):
        toggle = self.wait.until(
            EC.presence_of_element_located(self.SIDEBAR_TOGGLE)
        )

        # Scroll into view (important for some layouts)
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            toggle
        )

        # Use JS click (avoids zero size error)
        self.driver.execute_script(
            "arguments[0].click();",
            toggle
        )

        # Wait until CRM becomes visible
        self.wait.until(
            EC.visibility_of_element_located(self.CRM_MENU)
        )

    # ---------------- Enquiry ----------------
    def open_create_enquiry(self):
        self.open_sidebar()

        # Click CRM
        self.wait.until(
            EC.element_to_be_clickable(self.CRM_MENU)
        ).click()

        # Click Create Enquiry
        self.wait.until(
            EC.element_to_be_clickable(self.CREATE_ENQUIRY)
        ).click()

    # ---------------- Direct Quotation ----------------
    def open_create_quotation(self):
        self.open_sidebar()

        # Click CRM
        self.wait.until(
            EC.element_to_be_clickable(self.CRM_MENU)
        ).click()

        # Click Create Quotation
        self.wait.until(
            EC.element_to_be_clickable(self.CREATE_QUOTATION)
        ).click()