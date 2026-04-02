import pytest
from selenium import webdriver

from Task.Pages.login_page import LoginPage
from Task.Pages.task_page import TaskCreationPage


@pytest.fixture
def driver():

    from selenium.webdriver.chrome.options import Options

    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    yield driver

    driver.quit()


def test_unscheduled_task_start_now(driver):

    login = LoginPage(driver)

    login.open("https://erptest.prog-biz.com")
    login.enter_company_code("Globrootstest")
    login.enter_username("sadiqh")
    login.enter_password("123")

    login.click_signin()
    login.validate_login_success()

    task_page = TaskCreationPage(driver)

    # ✅ STEP 1: CREATE UNSCHEDULED TASK (MANDATORY FOR STABILITY)
    task_page.open_task_modal()
    task_name = task_page.create_unscheduled_task(days=2)

    print("Task Created:", task_name)

    # ✅ STEP 2: OPEN UNSCHEDULED PAGE
    task_page.open_unscheduled_tasks()

    # ✅ STEP 3: OPEN SPECIFIC TASK (NOT RANDOM)
    task_page.open_unscheduled_task_overview(task_name)

    # ✅ STEP 4: SCROLL
    task_page.scroll_overview_modal()

    # ✅ STEP 5: START NOW
    task_page.start_task_now()

    print("✅ Task started immediately")

    #------------------------------ Worked---------------------------