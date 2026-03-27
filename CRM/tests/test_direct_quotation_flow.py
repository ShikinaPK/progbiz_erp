from CRM.pages import LoginPage
from CRM.pages import HomePage
from CRM.pages import QuotationPage

def test_create_direct_quotation(driver):

    login = LoginPage(driver)
    home = HomePage(driver)

    login.open("https://erptest.prog-biz.com/")
    login.enter_company_code("globrootstest")
    login.enter_username("Sadiqh")
    login.enter_password("123")
    login.click_signin()
    login.validate_login_success()

    home.open_create_quotation()

    quotation = QuotationPage(driver)
    quotation.wait_for_page_load()

    quotation.select_branch("1039")
    quotation.select_customer("arjun")
    quotation.select_sales_executive("You")
    quotation.select_lead_source("Facebook")

    quotation.set_valid_upto()
    quotation.set_next_followup_date()

    quotation.add_item("Finland", "1500", "GST 18%")

    quotation.apply_discount_if_present("100")

    quotation.click_save()
    quotation.validate_quotation_created()

    # -------------------------------- quotation 1st Followup-----------------------------------------------------------
    quotation.wait_for_overview()

    quotation.open_followup_modal()
    quotation.select_followup_status("Interested")
    quotation.handle_lead_quality_if_visible("Hot")
    quotation.enter_followup_description("Quotation under review")
    quotation.set_followup_date()
    quotation.save_followup()
    quotation.validate_followup_saved()

    # -------------------------------- quotation 2nd Followup---------------------------------------------------------
    quotation.open_followup_modal()
    quotation.select_followup_status("Fly")
    quotation.enter_followup_description("Got the deal")
    quotation.save_followup()
    quotation.validate_followup_saved()
