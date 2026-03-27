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


def test_create_unscheduled_task(driver):

    login = LoginPage(driver)

    login.open("https://erptest.prog-biz.com")

    login.enter_company_code("Globrootstest")
    login.enter_username("sadiqh")
    login.enter_password("123")

    login.click_signin()
    login.validate_login_success()

    task_page = TaskCreationPage(driver)

    task_page.open_task_modal()

    finish_date = task_page.create_unscheduled_task(days=2)

    print("Unscheduled task created with finish before:", finish_date)

    #-----------------------Worked Perfectly----------------------------