from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from calendar import monthrange


class EnquiryQuotationPage:

    VALID_UPTO = (By.ID, "expdate")
    NEXT_FOLLOWUP = (By.ID, "firstfollowupdate")
    LEAD_QUALITY = (By.ID, "quotation-quality")
    QUOTATION_NO = (By.ID, "quotation-no")
    DESCRIPTION = (By.XPATH, "//textarea[@rows='3']")
    RATE = (By.XPATH, "(//input[contains(@class,'number')])[1]")
    SAVE_BTN = (By.ID, "btn-save-quotation")

    # ---------- QUOTATION FOLLOWUP LOCATORS ----------

    FOLLOWUP_BTN = (By.ID, "btn-add-followup")
    FOLLOWUP_STATUS = (By.ID, "followup-status")
    LEAD_QUALITY = (By.ID, "lead-quality")
    FOLLOWUP_DESCRIPTION = (By.ID, "followup-description")
    FOLLOWUP_DATE = (By.ID, "next-followup-date")
    FOLLOWUP_SAVE_BTN = (By.ID, "btn-save-followup")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def wait_for_page_load(self):
        self.wait.until(
            EC.element_to_be_clickable(self.VALID_UPTO)
        )

    def set_valid_upto(self):
        today = datetime.today()
        last_day_number = monthrange(today.year, today.month)[1]
        last_day = today.replace(day=last_day_number)

        formatted = last_day.strftime("%d-%m-%Y")

        field = self.wait.until(
            EC.presence_of_element_located(self.VALID_UPTO)
        )
        field.clear()
        field.send_keys(formatted)

    def set_next_followup(self):

        field = self.wait.until(
            EC.presence_of_element_located(self.NEXT_FOLLOWUP)
        )

        min_value = field.get_attribute("min")

        if min_value:
            base_time = datetime.fromisoformat(min_value)
            final_time = base_time + timedelta(minutes=2)
        else:
            final_time = datetime.now() + timedelta(minutes=10)

        formatted = final_time.strftime("%Y-%m-%dT%H:%M")

        self.driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, field, formatted)

    def capture_quotation_number(self):
        element = self.wait.until(
            EC.presence_of_element_located(self.QUOTATION_NO)
        )
        qt_no = element.get_attribute("value")
        print("Quotation No:", qt_no)
        return qt_no

    def handle_lead_quality(self, text="Cold"):
        elements = self.driver.find_elements(*self.LEAD_QUALITY)
        if elements:
            Select(elements[0]).select_by_visible_text(text)

    def handle_description(self):
        desc = self.wait.until(
            EC.presence_of_element_located(self.DESCRIPTION)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            desc
        )

        value = desc.get_attribute("value")

        if not value:
            desc.send_keys("test description")

    def update_rate(self, value="10000"):
        rate = self.wait.until(
            EC.presence_of_element_located(self.RATE)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            rate
        )

        rate.clear()
        rate.send_keys(value)

    def click_save(self):
        save = self.wait.until(
            EC.presence_of_element_located(self.SAVE_BTN)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            save
        )

        self.driver.execute_script(
            "arguments[0].click();",
            save
        )

    def wait_for_overview(self):
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(., 'Followup')]")
            )
        )

        # ---------- QUOTATION FOLLOWUP FLOW ----------

    def open_followup_modal(self):
            btn = self.wait.until(
                EC.element_to_be_clickable(self.FOLLOWUP_BTN)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                btn
            )

            self.driver.execute_script("arguments[0].click();", btn)

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
                pass

    def enter_followup_description(self, text):

            desc_field = self.wait.until(
                EC.visibility_of_element_located(self.FOLLOWUP_DESCRIPTION)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                desc_field
            )

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

            if min_value:
                base_time = datetime.fromisoformat(min_value)
                final_time = base_time + timedelta(minutes=2)
            else:
                final_time = datetime.now() + timedelta(minutes=2)

            formatted = final_time.strftime("%Y-%m-%dT%H:%M")

            self.driver.execute_script("""
                arguments[0].value = arguments[1];
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, date_field, formatted)

    def save_followup(self):

            save_btn = self.wait.until(
                EC.element_to_be_clickable(self.FOLLOWUP_SAVE_BTN)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                save_btn
            )

            self.driver.execute_script("arguments[0].click();", save_btn)

    def validate_followup_saved(self):
            self.wait.until(
                EC.presence_of_element_located(self.FOLLOWUP_BTN)
            )