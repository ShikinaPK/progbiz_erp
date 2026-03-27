# import pytest
# from selenium import webdriver
#
# from Task.Pages.login_page import LoginPage
# from Task.Pages.task_page import TaskCreationPage
#
#
# @pytest.fixture
# def driver():
#
#     from selenium.webdriver.chrome.options import Options
#
#     chrome_options = Options()
#     chrome_options.add_argument("--disable-notifications")
#
#     driver = webdriver.Chrome(options=chrome_options)
#     driver.maximize_window()
#
#     yield driver
#
#     driver.quit()
#
#
# def test_create_task_for_later(driver):
#
#     login = LoginPage(driver)
#
#     login.open("https://erptest.prog-biz.com")
#
#     login.enter_company_code("Globrootstest")
#     login.enter_username("sadiqh")
#     login.enter_password("123")
#
#     login.click_signin()
#     login.validate_login_success()
#
#     task_page = TaskCreationPage(driver)
#
#     task_page.open_task_modal()
#
#     scheduled_date = task_page.create_task_for_later(days=1)
#
#     print("Scheduled task created for:", scheduled_date)
#
#
#     #----------------- Worked---------------------------------------------------
# #need to fix a fit -26/03 check last chatgpt chat
#     #--------------------------- Task assertions---------------------------------
# def test_create_task_for_later(driver):
#
#     login = LoginPage(driver)
#
#     login.open("https://erptest.prog-biz.com")
#     login.enter_company_code("Globrootstest")
#     login.enter_username("sadiqh")
#     login.enter_password("123")
#
#     login.click_signin()
#     login.validate_login_success()
#
#     task_page = TaskCreationPage(driver)
#
#     task_page.open_task_modal()
#
#     task_name = "Online meeting - Task for Later Task 3"
#
#     task_page.create_instant_task()
#
#     # ---------- MY TASK ----------
#     task_page.open_my_tasks()
#
#     task_page.search_task(task_name)
#
#     task_page.verify_task_in_results(task_name)
#
#     # ---------- CREATED TASK ----------
#     task_page.open_created_tasks()
#
#     task_page.search_task(task_name)
#
#     task_page.verify_task_in_results(task_name)

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


# -------- CREATE TASK FOR LATER --------
def test_create_task_for_later(driver):

    login = LoginPage(driver)

    login.open("https://erptest.prog-biz.com")
    login.enter_company_code("Globrootstest")
    login.enter_username("sadiqh")
    login.enter_password("123")

    login.click_signin()
    login.validate_login_success()

    task_page = TaskCreationPage(driver)
    task_page.open_task_modal()

    scheduled_date = task_page.create_task_for_later(days=1)

    print("Scheduled task created for:", scheduled_date)


# -------- VALIDATE TASK FOR LATER --------
def test_task_for_later_search_validation(driver):

    login = LoginPage(driver)

    login.open("https://erptest.prog-biz.com")
    login.enter_company_code("Globrootstest")
    login.enter_username("sadiqh")
    login.enter_password("123")

    login.click_signin()
    login.validate_login_success()

    task_page = TaskCreationPage(driver)
    task_page.open_task_modal()

    task_name = "Online meeting - Task for Later Task 3"

    task_page.create_task_for_later()

    # MY TASK
    task_page.open_my_tasks()
    task_page.search_task(task_name)
    task_page.verify_task_in_results(task_name)

    # CREATED TASK
    task_page.open_created_tasks()
    task_page.search_task(task_name)
    task_page.verify_task_in_results(task_name)