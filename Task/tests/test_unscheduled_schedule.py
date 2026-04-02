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


def test_unscheduled_task_schedule(driver):

    login = LoginPage(driver)

    login.open("https://erptest.prog-biz.com")
    login.enter_company_code("Globrootstest")
    login.enter_username("sadiqh")
    login.enter_password("123")

    login.click_signin()
    login.validate_login_success()

    task_page = TaskCreationPage(driver)

    # CREATE
    task_page.open_task_modal()
    task_name = task_page.create_unscheduled_task(days=2)

    print("Task Created:", task_name)

    # OPEN FROM HOME
    task_page.open_unscheduled_tasks()
    task_page.open_unscheduled_task_overview(task_name)

    # SCHEDULE
    task_page.scroll_overview_modal()
    new_date = task_page.schedule_unscheduled_task(days=1)

    print("✅ Scheduled")

    # VALIDATE
    task_page.open_my_tasks()
    task_page.search_task(task_name)
    task_page.open_task_from_my_tasks(task_name)

    task_page.open_task_overview_from_my_tasks()

    result = task_page.get_scheduled_date_from_overview()

    print("🎯 FINAL OUTPUT:", result)