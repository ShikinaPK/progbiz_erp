from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time
from selenium.webdriver.support.ui import Select


def select_lead_quality(self, text):

    dropdown = self.wait.until(
        EC.presence_of_element_located((By.ID, "leadquality"))
    )

    self.driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        dropdown
    )

    self.wait.until(
        EC.element_to_be_clickable((By.ID, "leadquality"))
    )

    Select(dropdown).select_by_visible_text(text)

class EnquiryPage:

    CREATE_ENQUIRY = (By.ID, "nav-crm-create-enquiry")

    BRANCH = (By.ID, "branch")
    CUSTOMER_PHONE = (By.ID, "customer-phone")
    CUSTOMER_NAME = (By.ID, "TxtCustomer")
    ASSIGN_TO = (By.ID, "assignto")
    NEXT_FOLLOWUP_DATE = (By.ID, "next-followup-date")
    LEAD_SOURCE = (By.ID, "leadsource")
    ITEM_SEARCH = (By.ID, "item-search-input")
    ITEM_ROW = (By.ID, "popup-item-row-5")
    ADD_ITEM_BTN = (By.ID, "btn-add-item")
    SAVE_BTN = (By.ID, "btn-save-enquiry")

#follow-up
    FOLLOWUP_BTN = (By.ID, "btn-add-followup")
    FOLLOWUP_STATUS = (By.ID, "followup-status")
    LEAD_QUALITY = (By.ID, "lead-quality")
    BUSINESS_VALUE = (By.ID, "business-value")
    FOLLOWUP_DESCRIPTION = (By.ID, "followup-description")
    FOLLOWUP_DATE = (By.ID, "next-followup-date")
    FOLLOWUP_SAVE_BTN = (By.ID, "btn-save-followup")

    #Quotation through enquiry
    CREATE_QUOTATION_BTN = (By.ID, "btn-create-quotation")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def open_create_enquiry(self):
        self.wait.until(
            EC.element_to_be_clickable(self.CREATE_ENQUIRY)
        ).click()

    def select_branch(self, value):
        Select(self.wait.until(
            EC.visibility_of_element_located(self.BRANCH)
        )).select_by_value(value)

    def enter_customer_phone(self, phone):
        self.driver.find_element(*self.CUSTOMER_PHONE).send_keys(phone)

    def enter_customer_name(self, name):
        self.driver.find_element(*self.CUSTOMER_NAME).send_keys(name)

    def select_assign_to(self, value):
        Select(self.driver.find_element(*self.ASSIGN_TO)).select_by_value(value)

    def set_next_followup_date(self):
        date_field = self.wait.until(
            EC.presence_of_element_located(self.NEXT_FOLLOWUP_DATE)
        )

        min_value = date_field.get_attribute("min")

        # If min is empty, use current time instead
        if not min_value:
            from datetime import datetime, timedelta
            final_time = datetime.now() + timedelta(minutes=2)
        else:
            from datetime import datetime, timedelta
            min_time = datetime.fromisoformat(min_value)
            final_time = min_time + timedelta(minutes=2)

        formatted = final_time.strftime("%Y-%m-%dT%H:%M")

        self.driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, date_field, formatted)

    def enter_lead_source(self, source):
        self.driver.find_element(*self.LEAD_SOURCE).send_keys(source)

    def add_item(self, item_name):

        # Step 1: Type item
        search_input = self.wait.until(
            EC.visibility_of_element_located(self.ITEM_SEARCH)
        )
        search_input.clear()
        search_input.send_keys(item_name)

        # Step 2: Click search icon
        search_icon = self.driver.find_element(
            By.XPATH,
            "//input[@id='item-search-input']/following-sibling::div"
        )
        self.driver.execute_script("arguments[0].click();", search_icon)

        # Step 3: Wait for modal
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "searchItemModal"))
        )

        # Step 4: Click the cell containing item text (NOT the entire row)
        item_cell = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH,
                 f"//div[@id='searchItemModal']//td[normalize-space()='{item_name}']")
            )
        )

        self.driver.execute_script("arguments[0].click();", item_cell)

        # Step 5: Click + button safely
        add_btn = self.wait.until(
            EC.presence_of_element_located(self.ADD_ITEM_BTN)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            add_btn
        )
        self.driver.execute_script("arguments[0].click();", add_btn)

    def click_save(self):

        save_btn = self.wait.until(
            EC.presence_of_element_located(self.SAVE_BTN)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            save_btn
        )

        self.driver.execute_script(
            "arguments[0].click();",
            save_btn
        )

    def validate_enquiry_created(self):
        self.wait.until(lambda d: "enquiry-overview" in d.current_url)
        assert "enquiry-overview" in self.driver.current_url

    # ---------- FOLLOWUP FLOW ----------

    def open_followup_modal(self):
        self.wait.until(
            EC.element_to_be_clickable(self.FOLLOWUP_BTN)
        ).click()

    def select_followup_status(self, status_text):
        status_dropdown = self.wait.until(
            EC.visibility_of_element_located(self.FOLLOWUP_STATUS)
        )
        Select(status_dropdown).select_by_visible_text(status_text)

    def handle_lead_quality_if_visible(self, quality_value):
        try:
            lead_quality_dropdown = self.wait.until(
                EC.visibility_of_element_located(self.LEAD_QUALITY)
            )
            Select(lead_quality_dropdown).select_by_visible_text(quality_value)
        except:
            # Field not displayed for Won/Lost
            pass

    def enter_business_value(self, value):
        field = self.wait.until(
            EC.visibility_of_element_located(self.BUSINESS_VALUE)
        )
        field.clear()
        field.send_keys(value)

    def enter_followup_description(self, text):

        desc_field = self.wait.until(
            EC.visibility_of_element_located(self.FOLLOWUP_DESCRIPTION)
        )

        # Scroll into view
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            desc_field
        )

        # Clear properly
        desc_field.clear()

        # Use JS to set value (most reliable for modern UIs)
        self.driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, desc_field, text)

    def set_followup_date(self):
        date_field = self.wait.until(
            EC.presence_of_element_located(self.FOLLOWUP_DATE)
        )

        min_value = date_field.get_attribute("min")

        if not min_value:
            final_time = datetime.now() + timedelta(minutes=2)
        else:
            min_time = datetime.fromisoformat(min_value)
            final_time = min_time + timedelta(minutes=2)

        formatted = final_time.strftime("%Y-%m-%dT%H:%M")

        self.driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, date_field, formatted)

    def save_followup(self):
        save_btn = self.wait.until(
            EC.presence_of_element_located(self.FOLLOWUP_SAVE_BTN)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            save_btn
        )

        self.driver.execute_script(
            "arguments[0].click();",
            save_btn
        )

    def validate_followup_saved(self):
        self.wait.until(lambda d: "enquiry-overview" in d.current_url)
        assert "enquiry-overview" in self.driver.current_url
        time.sleep(2)

    #Quotation creation through enquiry
    def click_create_quotation(self):

        btn = self.wait.until(
            EC.element_to_be_clickable(self.CREATE_QUOTATION_BTN)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            btn
        )

        self.driver.execute_script(
            "arguments[0].click();",
            btn
        )

        # Wait until redirected to quotation page
        self.wait.until(
            lambda d: "quotation" in d.current_url.lower()
        )