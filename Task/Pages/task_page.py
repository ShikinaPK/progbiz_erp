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

    # confirm button to hold
    CONFIRM_ACTION_BTN = (By.XPATH, "//div[contains(@class,'modal') and contains(@class,'show')]//div[@class='modal-footer']//button[@type='submit']")

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

    # -------- RESCHEDULE --------
    THREE_DOTS = (By.XPATH, "//a[@data-bs-toggle='dropdown']")
    RESCHEDULE_OPTION = (By.XPATH, "//a[contains(text(),'Reschedule Task')]")

    RESCHEDULE_DATE = (By.XPATH, "//input[@type='date']")
    RESCHEDULE_TIME = (By.XPATH, "//input[@type='time']")

    SCHEDULE_BTN = (By.XPATH, "//button[contains(.,'Schedule')]")

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
        # Manually entering task name
        #task_name.send_keys("Online meeting - Instant Task 13")

        # Automating task name
        task_name_value = f"Online meeting - Instant Task {datetime.now().strftime('%H%M%S')}"
        task_name.send_keys(task_name_value)

        self.driver.execute_script("window.scrollBy(0,350);")

        self.add_participants()

        self.enter_description()

        self.save_task()

        print("Instant task created successfully")
        return task_name_value

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
        #Manually Adding task Name
        #task_name.send_keys("Online meeting - Task for Later Task 4")

        #Automating Task Name
        task_name_value = f"Online meeting - Task Later {datetime.now().strftime('%H%M%S')}"
        task_name.send_keys(task_name_value)

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

        return task_name_value

    # ---------- UNSCHEDULED TASK ----------
    def create_unscheduled_task(self, days=2):

        self.wait.until(EC.visibility_of_element_located(self.TASK_NAME))

        # Select Task for Later
        later_radio = self.wait.until(
            EC.element_to_be_clickable(self.LATER_TASK_RADIO)
        )
        self.driver.execute_script("arguments[0].click();", later_radio)

        print("Task for Later radio selected")

        self.select_task_type()
        self.select_priority()

        task_name = self.wait.until(
            EC.presence_of_element_located(self.TASK_NAME)
        )
        task_name.clear()

        task_name_value = f"Unscheduled client meeting {datetime.now().strftime('%H%M%S')}"
        task_name.send_keys(task_name_value)

        self.driver.execute_script("window.scrollBy(0,350);")

        self.add_participants()

        # Select Unscheduled
        unscheduled_radio = self.wait.until(
            EC.element_to_be_clickable(self.UNSCHEDULED_RADIO)
        )
        self.driver.execute_script("arguments[0].click();", unscheduled_radio)

        print("Unscheduled task selected")

        # Finish Before
        finish_toggle = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(),'Finish Before')]")
            )
        )
        self.driver.execute_script("arguments[0].click();", finish_toggle)

        finish_date = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//label[contains(text(),'Finish Before Date')]/following::input[@type='date'][1]")
            )
        )

        finish_time = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//label[contains(text(),'Finish Before Time')]/following::input[@type='time'][1]")
            )
        )

        future_date = (datetime.today() + timedelta(days=days)).strftime("%Y-%m-%d")

        self.driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('change'));
        """, finish_date, future_date)

        self.driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('change'));
        """, finish_time, "18:30")

        print("Finish before date set:", future_date)

        self.enter_description()
        self.save_task()

        return task_name_value

    # ---------- OPEN UNSCHEDULED ----------
    def open_unscheduled_tasks(self):

        unscheduled = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//p[contains(text(),'Unscheduled')]")
            )
        )

        self.driver.execute_script("arguments[0].click();", unscheduled)
        print("Unscheduled tasks page opened")

    # ---------- OPEN OVERVIEW ----------
    def open_unscheduled_task_overview(self, task_name):

        self.search_task(task_name)

        overview_icon = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//i[contains(@class,'ri-calendar-event-fill')]")
            )
        )

        self.driver.execute_script("arguments[0].click();", overview_icon)
        print("Overview modal opened")

    # ---------- SCROLL ----------
    def scroll_overview_modal(self):

        modal = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'modal') and contains(@class,'show')]")
            )
        )

        self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
        print("Modal scrolled")

    # ---------- SCHEDULE ----------
    def schedule_unscheduled_task(self, days=1):

        new_date = (datetime.today() + timedelta(days=days)).strftime("%Y-%m-%d")

        date_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "schedule-start-date"))
        )

        self.driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('change'));
        """, date_field, new_date)

        time_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "schedule-start-time"))
        )

        self.driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('change'));
        """, time_field, "10:30")

        schedule_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class,'modal')]//button[contains(.,'Schedule')]")
            )
        )

        self.driver.execute_script("arguments[0].click();", schedule_btn)

        print("Scheduled date:", new_date)

        return new_date

    # ---------- OPEN FROM MY TASK ----------
    def open_task_from_my_tasks(self, task_name):

        self.search_task(task_name)

        task = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//td[contains(text(),'{task_name}')]")
            )
        )

        self.driver.execute_script("arguments[0].click();", task)

        print("Opened task:", task_name)

    def open_task_overview_from_my_tasks(self):
            overview_icon = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//i[contains(@class,'ri-send-plane-2-line')]")
                )
            )

            self.driver.execute_script("arguments[0].click();", overview_icon)

            print("Overview opened from My Tasks")

    # ---------- GET DATE ----------
    def get_scheduled_date_from_overview(self):

        date_text = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//p[contains(text(),'Scheduled On')]")
            )
        ).text

        print("📅 Scheduled Info:", date_text)

        return date_text

    # ---------- START NOW (UNSCHEDULED) ----------
    def start_task_now(self):

        # Click Start Now button inside modal
        start_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//div[contains(@class,'modal') and contains(@class,'show')]//button[contains(.,'Start Now')]")
            )
        )

        self.driver.execute_script("arguments[0].click();", start_btn)
        print("Start Now clicked")

        # Confirm popup
        confirm_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class,'swal2-confirm')]")
            )
        )

        self.driver.execute_script("arguments[0].click();", confirm_btn)
        print("Confirm clicked → Task started")

        # Wait until redirected to home (important for stability)
        self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        print("Redirected to Home after Start Now")
    # ------------------------- My Task page-------------------------
    def open_my_tasks(self):

        # ✅ FIXED: removed URL dependency
        self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a[aria-label='Hide Sidebar'] span")
            )
        )

        sidebar = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a[aria-label='Hide Sidebar'] span")
            )
        )

        self.driver.execute_script("arguments[0].click();", sidebar)

        task_management = self.wait.until(
            EC.element_to_be_clickable((By.ID, "nav-task-management"))
        )

        task_management.click()

        my_tasks = self.wait.until(
            EC.element_to_be_clickable((By.ID, "nav-task-management-my-tasks"))
        )

        my_tasks.click()

        print("Opened My Tasks page")

    # ---------- OPEN FIRST TASK FROM RESULTS ----------
    def open_first_task(self):

        # wait for table reload properly
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//table//tbody//tr"))
        )

        # wait until FIRST ROW is clickable & visible
        first_task = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//table//tbody//tr)[1]")
            )
        )

        # scroll into view (VERY IMPORTANT)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", first_task
        )

        # small stability wait (handles UI redraw)
        self.wait.until(lambda d: first_task.is_displayed())

        # click using JS
        self.driver.execute_script("arguments[0].click();", first_task)

        print("Opened first task from search results")

    # ---------- COMMON CONFIRM ACTION ----------
    def click_confirm_action(self):

        confirm_btn = self.wait.until(
            EC.visibility_of_element_located(self.CONFIRM_ACTION_BTN)
        )

        self.driver.execute_script("arguments[0].scrollIntoView(true);", confirm_btn)
        self.driver.execute_script("arguments[0].click();", confirm_btn)

        print("Action confirmed")

    # ---------- CLICK HOLD ----------
    def click_hold(self):

        hold_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Hold']")
            )
        )

        self.driver.execute_script("arguments[0].click();", hold_btn)

        print("Hold button clicked")

        self.click_confirm_action()

        # ✅ WAIT until redirected back to list
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//table//tbody//tr")))

        print("Returned to task list after Hold")

    # ---------- CLICK END ----------
    def click_end(self):

        end_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='End Task' or normalize-space()='End']")
            )
        )

        self.driver.execute_script("arguments[0].click();", end_btn)

        print("End button clicked")

        # ❌ DO NOT call confirm here
        # because after HOLD → no popup appears

        # wait for task to end (page change / success indication)
        self.wait.until(EC.url_contains("task"))  # or any stable condition

    # ---------- CLICK START ----------
    def click_start(self):

        start_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(.,'Start Task')]")
            )
        )

        self.driver.execute_script("arguments[0].click();", start_btn)

        print("Start button clicked")

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

#------------------------------------Worked---------------------------------------------------
    # ---------------- RESCHEDULE MODAL ----------------
    def open_reschedule_modal(self):

        three_dots = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//i[contains(@class,'fe-more-vertical')]")
            )
        )

        self.driver.execute_script("arguments[0].click();", three_dots)
        print("3 dots clicked")

        reschedule = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//a[normalize-space()='Reschedule Task']")
            )
        )

        self.driver.execute_script("arguments[0].click();", reschedule)
        print("Reschedule option clicked")

    # ---------------- RESCHEDULE TASK ----------------
    def reschedule_task(self, days=2):

        new_date = (datetime.today() + timedelta(days=days)).strftime("%Y-%m-%d")

        # ---------- DATE ----------
        date_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'modal') and contains(@class,'show')]//input[@type='date']")
            )
        )

        self.driver.execute_script("arguments[0].scrollIntoView(true);", date_field)

        self.driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, date_field, new_date)

        print("Reschedule date set to:", new_date)

        # ---------- TIME ----------
        time_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'modal') and contains(@class,'show')]//input[@type='time']")
            )
        )

        self.driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, time_field, "18:30")

        print("Reschedule time set to: 18:30")

        # ---------- CLICK SCHEDULE ----------
        schedule_btn = self.wait.until(
            EC.element_to_be_clickable(
                (
                By.XPATH, "//div[contains(@class,'modal') and contains(@class,'show')]//button[contains(.,'Schedule')]")
            )
        )

        self.driver.execute_script("arguments[0].click();", schedule_btn)

        print("Schedule button clicked")

        # ✅ WAIT UNTIL MODAL CLOSES (CRITICAL FIX)
        self.wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'modal') and contains(@class,'show')]")
            )
        )

        return new_date

    # ---------------- CREATED TASK → START ----------------
    def click_start_from_created(self):

        # wait for table
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//table//tbody//tr"))
        )

        start_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//table//tbody//tr)[1]//a[contains(@class,'btn-primary-light')]")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", start_btn
        )

        self.driver.execute_script("arguments[0].click();", start_btn)

        print("Start button (Created Task) clicked")

        # wait for overview page
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//p[contains(text(),'Scheduled On')]")
            )
        )

    # ---------------- GET SCHEDULED DATE ----------------
    def get_scheduled_date_from_overview(self):

        schedule_text = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//p[contains(text(),'Scheduled On')]")
            )
        ).text.strip()

        print("✅ Scheduled Info:", schedule_text)

        return schedule_text