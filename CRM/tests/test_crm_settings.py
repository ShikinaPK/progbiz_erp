import pytest
from selenium import webdriver

from CRM.pages.crm_settings_page import CRMSettingsPage
from Task.Pages.login_page import LoginPage


@pytest.fixture
def driver():

    from selenium.webdriver.chrome.options import Options

    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    yield driver

    driver.quit()


def test_crm_items(driver):

    login = LoginPage(driver)

    login.open("https://erptest.prog-biz.com")
    login.enter_company_code("Globrootstest")
    login.enter_username("sadiqh")
    login.enter_password("123")

    login.click_signin()
    login.validate_login_success()

    crm = CRMSettingsPage(driver)

    crm.open_crm_settings()
    crm.open_items()

    item = crm.create_item()

    crm.search_name(item)
    crm.verify_name_present(item)