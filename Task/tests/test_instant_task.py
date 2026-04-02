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

    driver.implicitly_wait(5)

    yield driver

    driver.quit()


def test_create_instant_task(driver):
        login = LoginPage(driver)

        login.open("https://erptest.prog-biz.com")
        login.enter_company_code("Globrootstest")
        login.enter_username("sadiqh")
        login.enter_password("123")

        login.click_signin()
        login.validate_login_success()

        task_page = TaskCreationPage(driver)

        task_page.open_task_modal()

        task_page.create_instant_task()
#-----------------------Assertion-------------------
def test_create_instant_task(driver):

    login = LoginPage(driver)

    login.open("https://erptest.prog-biz.com")
    login.enter_company_code("Globrootstest")
    login.enter_username("sadiqh")
    login.enter_password("123")

    login.click_signin()
    login.validate_login_success()

    task_page = TaskCreationPage(driver)

    task_page.open_task_modal()
# Validating Manually added Task Name
#     task_name = "Online meeting - Instant Task 13"
#     task_page.create_instant_task()

    #Validating Automated Task Name
    task_name = task_page.create_instant_task()

    # ---------- MY TASK ----------
    task_page.open_my_tasks()

    task_page.search_task(task_name)

    task_page.verify_task_in_results(task_name)

    # Open → Hold
    task_page.open_first_task()
    task_page.click_hold()

    # Re-open same task (VERY IMPORTANT)
    task_page.open_first_task()

    # End
    task_page.click_end()

    # ---------- CREATED TASK ----------
    task_page.open_created_tasks()

    task_page.search_task(task_name)

    task_page.verify_task_in_results(task_name)

    # --------------- Worked Perfectly -----------------------