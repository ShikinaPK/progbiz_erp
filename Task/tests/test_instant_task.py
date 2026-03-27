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
#--------------- Worked Perfectly -----------------------

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

    task_name = "Online meeting - Instant Task 11"

    task_page.create_instant_task()

    # ---------- MY TASK ----------
    task_page.open_my_tasks()

    task_page.search_task(task_name)

    task_page.verify_task_in_results(task_name)

    # ---------- CREATED TASK ----------
    task_page.open_created_tasks()

    task_page.search_task(task_name)

    task_page.verify_task_in_results(task_name)