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


# ---------------------- RESCHEDULE FLOW ----------------------
def test_task_reschedule_flow(driver):

    login = LoginPage(driver)

    login.open("https://erptest.prog-biz.com")
    login.enter_company_code("Globrootstest")
    login.enter_username("sadiqh")
    login.enter_password("123")

    login.click_signin()
    login.validate_login_success()

    task_page = TaskCreationPage(driver)
    task_page.open_task_modal()

    # ---------- CREATE TASK ----------
    task_name = task_page.create_task_for_later()

    # ---------- GO TO MY TASKS ----------
    task_page.open_my_tasks()
    task_page.search_task(task_name)
    task_page.verify_task_in_results(task_name)

    # ---------- OPEN TASK ----------
    task_page.open_first_task()

    # ---------- RESCHEDULE ----------
    task_page.open_reschedule_modal()
    task_page.reschedule_task(days=2)

    # ✅ SMALL STABILITY WAIT (ensures UI settled before navigation)
    task_page.wait.until(lambda d: "task" in d.current_url.lower() or "home" in d.current_url.lower())

    # ---------- CREATED TASK FLOW ----------
    task_page.open_created_tasks()
    task_page.search_task(task_name)
    task_page.verify_task_in_results(task_name)

    # ---------- START TASK FROM CREATED ----------
    task_page.click_start_from_created()

    # ---------- GET SCHEDULED DATE ----------
    scheduled_info = task_page.get_scheduled_date_from_overview()

    print("🎯 Final Output →", scheduled_info)
    
    #---------worked------------