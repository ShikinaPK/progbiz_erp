from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


class CRMSettingsPage:

    # ---------- ITEM CATEGORY ----------
    ITEM_CATEGORY_MENU = (By.ID, "nav-crm-settings-item-categories")

    CATEGORY_NAME_FIELD = (By.ID, "categoryname")

    SAVE_BUTTON = (By.XPATH, "//button[contains(.,'Save')]")

    # ---------- LEAD FOLLOW-UP STATUS ----------
    FOLLOWUP_STATUS_MENU = (By.ID, "nav-crm-settings-lead-status")

    FOLLOWUP_STATUS_NAME = (By.ID, "followupstatusname")

    FOLLOWUP_SAVE_BTN = (By.XPATH, "//button[contains(.,'Save')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # ---------- NAVIGATION ----------
    def open_crm_settings(self):

        # wait for dashboard
        self.wait.until(EC.url_contains("home"))

        # click hamburger (FIXED)
        sidebar = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@class,'sidemenu-toggle')]//span")
            )
        )

        self.driver.execute_script(
            "arguments[0].click();", sidebar
        )

        # click CRM
        crm_menu = self.wait.until(
            EC.element_to_be_clickable((By.ID, "nav-crm"))
        )
        crm_menu.click()

        # click CRM Settings
        settings = self.wait.until(
            EC.element_to_be_clickable((By.ID, "nav-crm-settings"))
        )
        settings.click()

        print("CRM Settings opened")

    # ---------- ITEMS ----------
    def open_items(self):

        self.wait.until(
            EC.element_to_be_clickable((By.ID, "nav-crm-settings-items"))
        ).click()

        print("Items page opened")

    def create_item(self):

        item_name = f"Item {datetime.now().strftime('%H%M%S')}"

        # click New Item
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(.,'New Item')]")
            )
        ).click()

        # wait for modal/input to fully appear
        name_field = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='text']"))
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", name_field
        )

        # safe clear
        self.driver.execute_script("arguments[0].value='';", name_field)

        name_field.send_keys(item_name)

        # Select Category
        self.wait.until(
            EC.element_to_be_clickable((By.ID, "category"))
        ).click()

        self.driver.find_element(By.XPATH, "//option[2]").click()

        # Select ALL branches
        checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
        for cb in checkboxes:
            if not cb.is_selected():
                self.driver.execute_script("arguments[0].click();", cb)

        # Save
        self.driver.find_element(By.XPATH, "//button[contains(.,'Save')]").click()

        # wait after save
        self.wait.until(lambda d: item_name in d.page_source)

        print("Item created:", item_name)

        return item_name

    # ---------- SEARCH ----------
    def search_name(self, name):

        search_box = self.wait.until(
            EC.element_to_be_clickable((By.ID, "filter-name"))
        )

        search_box.clear()
        search_box.send_keys(name)

        search_icon = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@id='filter-name']/following::div[1]")
            )
        )

        self.driver.execute_script("arguments[0].click();", search_icon)

        print(f"Searched: {name}")

    # ---------- ASSERTION ----------
    def verify_name_present(self, name):

        if name in self.driver.page_source:
            print(f"✅ Verified: {name}")
        else:
            raise AssertionError(f"{name} not found")

        #----------------------------- Item Category----------------------

    def open_item_categories(self):

        self.wait.until(
            EC.element_to_be_clickable(self.ITEM_CATEGORY_MENU)
        ).click()

        print("Item Categories page opened")

    def create_item_category(self):

        category_name = f"Category {datetime.now().strftime('%H%M%S')}"

        # wait for input field
        name_field = self.wait.until(
            EC.element_to_be_clickable(self.CATEGORY_NAME_FIELD)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", name_field
        )

        # safe clear
        self.driver.execute_script("arguments[0].value='';", name_field)

        name_field.send_keys(category_name)

        # click save
        save_btn = self.wait.until(
            EC.element_to_be_clickable(self.SAVE_BUTTON)
        )

        self.driver.execute_script(
            "arguments[0].click();", save_btn
        )

        # wait for save success
        self.wait.until(lambda d: category_name in d.page_source)

        print("Category created:", category_name)

        return category_name

    #-----------------------Open Followup Page----------------------------
    def open_followup_status(self):

        # wait CRM settings loaded
        self.wait.until(EC.url_contains("crm"))

        # locate sidebar scroll container
        sidebar_container = self.wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "simplebar-content-wrapper")
            )
        )

        # locate Lead Status element
        status_menu = self.wait.until(
            EC.presence_of_element_located(
                (By.ID, "nav-crm-settings-lead-status")
            )
        )

        # scroll INSIDE sidebar (IMPORTANT FIX)
        self.driver.execute_script(
            "arguments[0].scrollTop = arguments[1].offsetTop;",
            sidebar_container,
            status_menu
        )

        # wait until visible
        self.wait.until(lambda d: status_menu.is_displayed())

        # click using JS
        self.driver.execute_script(
            "arguments[0].click();", status_menu
        )

        print("Lead Status page opened")

    def create_followup_status(self):

        status_name = f"Followup {datetime.now().strftime('%H%M%S')}"

        # wait for field
        name_field = self.wait.until(
            EC.element_to_be_clickable(self.FOLLOWUP_STATUS_NAME)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", name_field
        )

        # safe clear
        self.driver.execute_script("arguments[0].value='';", name_field)

        name_field.send_keys(status_name)

        # click save
        save_btn = self.wait.until(
            EC.element_to_be_clickable(self.FOLLOWUP_SAVE_BTN)
        )

        self.driver.execute_script(
            "arguments[0].click();", save_btn
        )

        # wait for result
        self.wait.until(lambda d: status_name in d.page_source)

        print("Follow-up Status created:", status_name)

        return status_name