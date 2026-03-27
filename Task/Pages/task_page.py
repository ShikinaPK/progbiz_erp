from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta


class TaskCreationPage:

    CREATE_NEW_BTN = (By.ID, "new-task")
    TASK_OPTION = (By.ID, "new-task-item")

    TASK_NAME = (By.ID, "taskName")

    TASK_TYPE = (By.ID, "taskType")
    PRIORITY = (By.ID, "priority")

    ADD_PARTICIPANT_BTN = (By.ID, "addParticipantBtn")
    PARTICIPANT_FIELD = (By.XPATH, "//input[@placeholder='Choose Task Participants']")
    PARTICIPANT_SELECT_ALL = (By.ID, "participantMultiselect-select-all")
    PARTICIPANT_DONE = (By.ID, "participantMultiselect-done")

    DESCRIPTION = (By.ID, "description")

    SAVE_BTN = (By.ID, "saveBtn")
    CONFIRM_BTN = (By.CSS_SELECTOR, "button.swal2-confirm")

    # -------- TASK FOR LATER --------
    LATER_TASK_RADIO = (By.ID, "laterTask")
    SCHEDULED_RADIO = (By.ID, "scheduled")

    START_DATE = (By.XPATH, "//input[@type='date']")
    START_TIME = (By.XPATH, "//input[@type='time']")

    # -------- UNSCHEDULED TASK --------
    UNSCHEDULED_RADIO = (By.ID, "unscheduled")

    SET_FINISH_BEFORE = (
        By.XPATH,
        "//label[contains(.,'Finish Before')]"
    )

    FINISH_BEFORE_DATE = (
        By.XPATH,
        "(//input[@type='date'])[2]"
    )

    FINISH_BEFORE_TIME = (
        By.XPATH,
        "(//input[@type='time'])[2]"
    )
    # ---------- TASK MANAGEMENT NAVIGATION ----------
    # Sidebar toggle (hamburger)
    SIDEBAR_TOGGLE = (
        By.XPATH,
        "//a[contains(@class,'sidemenu-toggle')]"
    )
    TASK_MANAGEMENT_MENU = (By.ID, "nav-task-management")
    MY_TASK_MENU = (By.ID, "nav-task-management-my-tasks")
    CREATED_TASK_MENU = (By.ID, "nav-task-management-created-tasks")

    #------------------- Search in Created page--------------------------------

    SEARCH_FIELD = (By.ID, "task")

    SEARCH_ICON = (By.CSS_SELECTOR, "div.input-group-text")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # ---------- OPEN TASK MODAL ----------
    def open_task_modal(self):

        self.wait.until(EC.url_contains("home"))

        create_btn = self.wait.until(
            EC.element_to_be_clickable(self.CREATE_NEW_BTN)
        )
        create_btn.click()

        task_option = self.wait.until(
            EC.visibility_of_element_located(self.TASK_OPTION)
        )

        self.driver.execute_script("arguments[0].click();", task_option)

        self.wait.until(
            EC.visibility_of_element_located(self.TASK_NAME)
        )

        print("Task modal opened")

    # ---------- DROPDOWNS ----------
    def select_task_type(self):
        Select(
            self.wait.until(EC.element_to_be_clickable(self.TASK_TYPE))
        ).select_by_visible_text("Online Meeting")
    # def select_task_type(self):
    #
    #     dropdown = self.wait.until(
    #         EC.element_to_be_clickable(self.TASK_TYPE)
    #     )
    #
    #     select = Select(dropdown)
    #
    #     self.wait.until(lambda d: any(
    #         "Online" in option.text for option in select.options
    #     ))
    #
    #     for option in select.options:
    #         if "Online" in option.text:
    #             option.click()
    #             break

    def select_priority(self):
        Select(
            self.wait.until(EC.element_to_be_clickable(self.PRIORITY))
        ).select_by_visible_text("Normal")

    # ---------- PARTICIPANTS ----------
    def add_participants(self):

        add_btn = self.wait.until(
            EC.element_to_be_clickable(self.ADD_PARTICIPANT_BTN)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", add_btn
        )

        add_btn.click()

        participant_field = self.wait.until(
            EC.presence_of_element_located(self.PARTICIPANT_FIELD)
        )

        self.driver.execute_script(
            "arguments[0].click();", participant_field
        )

        self.wait.until(
            EC.element_to_be_clickable(self.PARTICIPANT_SELECT_ALL)
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(self.PARTICIPANT_DONE)
        ).click()

        print("Participants added")

    # ---------- DESCRIPTION ----------
    def enter_description(self):

        self.wait.until(
            EC.presence_of_element_located(self.DESCRIPTION)
        ).send_keys("Task created using Selenium automation")

    # ---------- SAVE TASK ----------
    def save_task(self):

        self.wait.until(
            EC.element_to_be_clickable(self.SAVE_BTN)
        ).click()

        print("Save clicked")

        try:
            confirm = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.CONFIRM_BTN)
            )
            confirm.click()
            print("Confirm popup clicked")
        except:
            print("No confirm popup")

        self.wait.until(EC.url_contains("home"))

        print("Redirected to home")

    # ---------- INSTANT TASK ----------
    def create_instant_task(self):

        self.wait.until(
            EC.visibility_of_element_located(self.TASK_NAME)
        )

        print("Instant task form loaded")

        self.select_task_type()
        self.select_priority()

        task_name = self.wait.until(
            EC.presence_of_element_located(self.TASK_NAME)
        )

        task_name.clear()
        task_name.send_keys("Online meeting - Instant Task 11")

        self.driver.execute_script("window.scrollBy(0,350);")

        self.add_participants()

        self.enter_description()

        self.save_task()

        print("Instant task created successfully")

    # ---------- TASK FOR LATER ----------
    def create_task_for_later(self, days=1):

        self.wait.until(
            EC.visibility_of_element_located(self.TASK_NAME)
        )

        later_radio = self.wait.until(
            EC.element_to_be_clickable(self.LATER_TASK_RADIO)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", later_radio
        )

        self.driver.execute_script(
            "arguments[0].click();", later_radio
        )

        self.wait.until(lambda d: later_radio.is_selected())
        # self.wait.until(lambda d: len(
        #     Select(d.find_element(*self.TASK_TYPE)).options
        # ) > 1)

        print("Task for Later radio selected")

        self.select_task_type()
        self.select_priority()

        task_name = self.wait.until(
            EC.presence_of_element_located(self.TASK_NAME)
        )

        task_name.clear()
        task_name.send_keys("Online meeting - Task for Later Task 3")

        self.driver.execute_script("window.scrollBy(0,350);")

        self.add_participants()

        self.wait.until(
            EC.element_to_be_clickable(self.SCHEDULED_RADIO)
        ).click()

        # ---------- DATE ----------
        future_date = (datetime.today() + timedelta(days=days)).strftime("%Y-%m-%d")

        date_field = self.wait.until(
            EC.presence_of_element_located(self.START_DATE)
        )

        self.driver.execute_script(
            "arguments[0].value = arguments[1];", date_field, future_date
        )

        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('change'));", date_field
        )

        print("Scheduled date set to:", future_date)

        # ---------- TIME ----------
        time_field = self.wait.until(
            EC.presence_of_element_located(self.START_TIME)
        )

        self.driver.execute_script(
            "arguments[0].value = arguments[1];", time_field, "18:30"
        )

        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('change'));", time_field
        )

        self.enter_description()

        self.save_task()

        return future_date

    # ---------- UNSCHEDULED TASK ----------
    def create_unscheduled_task(self, days=2):

        # wait until modal loads
        self.wait.until(
            EC.visibility_of_element_located(self.TASK_NAME)
        )

        # select Task for Later
        later_radio = self.wait.until(
            EC.element_to_be_clickable(self.LATER_TASK_RADIO)
        )

        self.driver.execute_script(
            "arguments[0].click();", later_radio
        )

        self.wait.until(lambda d: later_radio.is_selected())

        print("Task for Later radio selected")

        # dropdowns
        self.select_task_type()
        self.select_priority()

        # task name
        task_name = self.wait.until(
            EC.presence_of_element_located(self.TASK_NAME)
        )

        task_name.clear()
        task_name.send_keys("Unscheduled client meeting")

        # scroll down
        self.driver.execute_script("window.scrollBy(0,350);")

        # add participants
        self.add_participants()

        # select Unscheduled
        unscheduled_radio = self.wait.until(
            EC.element_to_be_clickable(self.UNSCHEDULED_RADIO)
        )

        self.driver.execute_script(
            "arguments[0].click();", unscheduled_radio
        )

        print("Unscheduled task selected")

        # ---------- OPEN FINISH BEFORE ----------
        finish_toggle = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[contains(text(),'Finish Before')]")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", finish_toggle
        )

        self.driver.execute_script(
            "arguments[0].click();", finish_toggle
        )

        print("Finish Before section opened")

        # ---------- WAIT FOR NEW DATE FIELD ----------
        finish_date = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH,
                 "//label[contains(text(),'Finish Before Date')]/following::input[@type='date'][1]")
            )
        )

        finish_time = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH,
                 "//label[contains(text(),'Finish Before Time')]/following::input[@type='time'][1]")
            )
        )

        # ---------- SET FUTURE DATE ----------
        future_date = (datetime.today() + timedelta(days=days)).strftime("%Y-%m-%d")

        self.driver.execute_script(
            "arguments[0].value = arguments[1];", finish_date, future_date
        )

        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('change'));", finish_date
        )

        print("Finish before date set:", future_date)

        # ---------- SET TIME ----------
        self.driver.execute_script(
            "arguments[0].value = arguments[1];", finish_time, "18:30"
        )

        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('change'));", finish_time
        )

        # description
        self.enter_description()

        # save task
        self.save_task()


        return future_date

    #------------------------- My Task page-------------------------
    def open_my_tasks(self):

        # wait until homepage loads
        self.wait.until(EC.url_contains("home"))

        # open hamburger menu
        sidebar = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a[aria-label='Hide Sidebar'] span")
            )
        )

        self.driver.execute_script("arguments[0].click();", sidebar)

        # wait until task management appears
        task_management = self.wait.until(
            EC.element_to_be_clickable((By.ID, "nav-task-management"))
        )

        task_management.click()

        # wait until my tasks menu appears
        my_tasks = self.wait.until(
            EC.element_to_be_clickable((By.ID, "nav-task-management-my-tasks"))
        )

        my_tasks.click()

        print("Opened My Tasks page")

    # ------------------------- Created page-------------------------
    def open_created_tasks(self):

        # open sidebar
        sidebar = self.wait.until(
            EC.element_to_be_clickable(self.SIDEBAR_TOGGLE)
        )
        self.driver.execute_script("arguments[0].click();", sidebar)

        # open task management menu
        task_menu = self.wait.until(
            EC.element_to_be_clickable(self.TASK_MANAGEMENT_MENU)
        )
        task_menu.click()

        # click created tasks
        created_tasks = self.wait.until(
            EC.element_to_be_clickable((By.ID, "nav-task-management-created-tasks"))
        )
        created_tasks.click()

        print("Opened Created Tasks page")

        print("Opened Created Tasks page")
#--------------------------- Search in Created Page------------------------------------
    def search_task(self, task_name):

        # wait for search field
        search_box = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_FIELD)
        )

        search_box.clear()
        search_box.send_keys(task_name)

        print("Task searched:", task_name)

        # wait for search icon
        search_icon = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_ICON)
        )

        # scroll to icon
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", search_icon
        )

        # click icon
        self.driver.execute_script(
            "arguments[0].click();", search_icon
        )

        print("Search icon clicked")

        # wait until result appears
        self.wait.until(lambda d: task_name in d.page_source)

        print("Search results loaded")

#------------------- Assertion-----------------------------------------
    def verify_task_in_results(self, task_name):

        if task_name in self.driver.page_source:
            print(f"Assertion passed → {task_name} found")
        else:
            raise AssertionError(f"Task '{task_name}' not found in results")