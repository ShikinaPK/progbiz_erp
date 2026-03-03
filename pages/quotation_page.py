from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta


class QuotationPage:

    # ---------- COMMON ----------
    BRANCH = (By.ID, "branch")
    CUSTOMER_INPUT = (By.ID, "customerNameInput")
    CUSTOMER_SEARCH_BTN = (By.ID, "btn-search-customer")
    CUSTOMER_SECOND_OPTION = (By.ID, "customer-search-row-2")

    SALES_EXECUTIVE = (By.ID, "agent")
    LEAD_SOURCE = (By.ID, "leadsource")

    VALID_UPTO = (By.ID, "expdate")
    NEXT_FOLLOWUP = (By.ID, "firstfollowupdate")

    ITEM_SEARCH = (By.ID, "item-search-input")
    ITEM_POPUP_ROW = (By.ID, "popup-item-row-0")
    ITEM_RATE = (By.XPATH, "//input[contains(@id,'item-rate')]")
    ITEM_TAX = (By.XPATH, "//select[contains(@id,'item-tax')]")
    ADD_ITEM_BTN = (By.ID, "btn-add-quotation-item")

    DISCOUNT_FIELD = (By.ID, "charge51")

    SAVE_BTN = (By.ID, "btn-save-quotation")

    # -------- FOLLOWUP LOCATORS --------
    FOLLOWUP_BTN = (By.ID, "btn-add-followup")
    FOLLOWUP_STATUS = (By.ID, "followup-status")
    LEAD_QUALITY_MODAL = (By.ID, "lead-quality")
    FOLLOWUP_DESCRIPTION = (By.ID, "followup-description")
    FOLLOWUP_DATE = (By.ID, "next-followup-date")
    FOLLOWUP_SAVE_BTN = (By.ID, "btn-save-followup")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # ---------- PAGE LOAD ----------
    def wait_for_page_load(self):

        # Wait until branch dropdown is visible
        self.wait.until(
            EC.visibility_of_element_located(self.BRANCH)
        )

        # Always start at top of page
        self.driver.execute_script("window.scrollTo(0, 0);")

    # ---------- BRANCH ----------
    def select_branch(self, value):
        Select(
            self.wait.until(
                EC.element_to_be_clickable(self.BRANCH)
            )
        ).select_by_value(value)

    # ---------- CUSTOMER ----------
    def select_customer(self, name):

        input_box = self.wait.until(
            EC.presence_of_element_located(self.CUSTOMER_INPUT)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            input_box
        )

        input_box.clear()
        input_box.send_keys(name)

        # Click search button
        search_btn = self.wait.until(
            EC.element_to_be_clickable(self.CUSTOMER_SEARCH_BTN)
        )
        self.driver.execute_script("arguments[0].click();", search_btn)

        # Wait until at least one search row appears
        rows = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//tr[starts-with(@id,'customer-search-row')]")
            )
        )

        if len(rows) == 0:
            raise Exception("No customer search results found.")

        # Click first result using JS
        self.driver.execute_script("arguments[0].click();", rows[0])

        # Wait until row disappears (means modal closed)
        self.wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//tr[starts-with(@id,'customer-search-row')]")
            )
        )

    # ---------- SALES EXECUTIVE ----------
    def select_sales_executive(self, text):
        dropdown = self.wait.until(
            EC.visibility_of_element_located(self.SALES_EXECUTIVE)
        )

        select = Select(dropdown)

        for option in select.options:
            if text.lower() in option.text.lower():
                option.click()
                return

        raise Exception("Sales Executive not found")

    # ---------- LEAD SOURCE ----------
    def select_lead_source(self, text):
        dropdown = self.wait.until(
            EC.visibility_of_element_located(self.LEAD_SOURCE)
        )

        select = Select(dropdown)

        for option in select.options:
            if text.lower() in option.text.lower():
                option.click()
                return

        raise Exception("Lead Source not found")

    # ---------- VALID UPTO ----------
    def set_valid_upto(self):

        date_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "expdate"))
        )

        from datetime import datetime, timedelta

        # Always 2 days in future (safe)
        future_date = datetime.now() + timedelta(days=2)

        formatted = future_date.strftime("%Y-%m-%d")

        self.driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, date_field, formatted)

    # ---------- NEXT FOLLOWUP DATE ----------
    def set_next_followup_date(self):

        date_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "firstfollowupdate"))
        )

        from datetime import datetime, timedelta

        # Always take future time (10 minutes ahead)
        future_time = datetime.now() + timedelta(minutes=10)

        formatted = future_time.strftime("%Y-%m-%dT%H:%M")

        self.driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, date_field, formatted)

    # ---------- ADD ITEM ----------
    def add_item(self, item_name, rate_value, tax_text):

        # Search item
        search_input = self.wait.until(
            EC.visibility_of_element_located(self.ITEM_SEARCH)
        )
        search_input.clear()
        search_input.send_keys(item_name)

        # Click search icon
        self.driver.find_element(
            By.XPATH,
            "//input[@id='item-search-input']/following-sibling::div"
        ).click()

        # Wait for modal to open
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "searchItemModal"))
        )

        # Click first row
        item_row = self.wait.until(
            EC.visibility_of_element_located(self.ITEM_POPUP_ROW)
        )

        self.driver.execute_script("arguments[0].click();", item_row)

        # 🔥 VERY IMPORTANT — wait for modal to disappear
        self.wait.until(
            EC.invisibility_of_element_located((By.ID, "searchItemModal"))
        )

        # Wait until rate field is present in DOM
        self.wait.until(
            EC.presence_of_element_located((By.ID, "item-rate"))
        )

        # Scroll page down first (important)
        self.driver.execute_script("window.scrollBy(0, 500);")

        rate_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "item-rate"))
        )

        # Scroll exactly to rate field
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            rate_field
        )

        # Small stability wait
        self.wait.until(lambda d: rate_field.is_displayed())

        # Set rate using JS (stable for Blazor)
        self.driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, rate_field, rate_value)

        # Tax dropdown
        tax_dropdown = self.wait.until(
            EC.visibility_of_element_located((By.ID, "item-tax-category"))
        )

        Select(tax_dropdown).select_by_visible_text(tax_text)

        # Scroll again before clicking +
        add_btn = self.wait.until(
            EC.presence_of_element_located(self.ADD_ITEM_BTN)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            add_btn
        )

        self.driver.execute_script("arguments[0].click();", add_btn)

    # ---------- DISCOUNT ----------
    def apply_discount_if_present(self, value):
        try:
            discount = self.wait.until(
                EC.visibility_of_element_located(self.DISCOUNT_FIELD)
            )

            if float(value) > 0:
                discount.clear()
                discount.send_keys(value)

        except:
            pass

    # ---------- SAVE ----------
    def click_save(self):

        save_btn = self.wait.until(
            EC.presence_of_element_located(self.SAVE_BTN)
        )

        # Scroll fully to bottom first
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Scroll directly to button
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            save_btn
        )

        # Small stability wait
        self.wait.until(lambda d: save_btn.is_displayed())

        # JS click (avoids interception)
        self.driver.execute_script("arguments[0].click();", save_btn)

    # ---------- VALIDATE ----------
    def validate_quotation_created(self):

        # Wait until save button disappears (means form submitted)
        self.wait.until(
            EC.invisibility_of_element_located(self.SAVE_BTN)
        )

        # OR wait until quotation number field is visible (overview indicator)
        self.wait.until(
            EC.presence_of_element_located((By.ID, "quotation-no"))

        )
#-------------------Open Followup Modal--------------------------------------------------------------------------
    def open_followup_modal(self):

        btn = self.wait.until(
            EC.element_to_be_clickable(self.FOLLOWUP_BTN)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            btn
        )

        btn.click()

        self.wait.until(
            EC.visibility_of_element_located(self.FOLLOWUP_STATUS)
        )
        #---------------Select Followup Status (Dynamic)---------------------------------------------------------

    def select_followup_status(self, status_text):

        dropdown = self.wait.until(
            EC.visibility_of_element_located(self.FOLLOWUP_STATUS)
        )

        select = Select(dropdown)

        for option in select.options:
            if status_text.lower() in option.text.lower():
                option.click()
                break
        else:
            raise Exception("Followup status not found")

        #-----------------Handle Lead Quality (Only If Visible)--------------------------------------------------

    def handle_modal_lead_quality(self, quality_text="Hot"):

        elements = self.driver.find_elements(*self.LEAD_QUALITY_MODAL)

        if elements:
            dropdown = elements[0]
            Select(dropdown).select_by_visible_text(quality_text)

    #-------------------- Set Next Followup---------------------------------------------------------------------
    def set_modal_next_followup_date(self):

        field = self.wait.until(
            EC.presence_of_element_located(self.FOLLOWUP_DATE)
        )

        min_value = field.get_attribute("min")

        from datetime import datetime, timedelta

        if min_value:
            base_time = datetime.fromisoformat(min_value)
            final_time = base_time + timedelta(minutes=5)
        else:
            final_time = datetime.now() + timedelta(minutes=10)

        formatted = final_time.strftime("%Y-%m-%dT%H:%M")

        self.driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, field, formatted)

    #----------------------Save followup--------------------------------------------------------------------
    def save_followup_modal(self):

        btn = self.wait.until(
            EC.element_to_be_clickable(self.FOLLOWUP_SAVE_BTN)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            btn
        )

        # Wait until modal closes
        self.wait.until(
            EC.invisibility_of_element_located(self.FOLLOWUP_STATUS)
        )

