from CRM.pages import LoginPage
from CRM.pages import HomePage
from CRM.pages import EnquiryPage
from CRM.pages import EnquiryQuotationPage
from CRM.tests.conftest import driver


def test_create_enquiry(driver):

    # Initialize page objects
    login = LoginPage(driver)
    homepage = HomePage(driver)
    enquiry = EnquiryPage(driver)

    # ---------------- LOGIN ----------------
    print('opening login page')
    login.open("https://erptest.prog-biz.com/")
    login.enter_company_code("globrootstest")
    login.enter_username("Sadiqh")
    login.enter_password("123")
    login.click_signin()
    print("\signin")
    login.validate_login_success()

    # -------- NAVIGATE TO CREATE ENQUIRY --------
    homepage.open_create_enquiry()

    # ---------------- ENQUIRY ----------------
    enquiry.select_branch("1039")
    enquiry.enter_customer_phone("9875000070")
    enquiry.enter_customer_name("Pravin")
    enquiry.select_assign_to("33518")
    enquiry.set_next_followup_date()
    enquiry.enter_lead_source("Facebook")
    enquiry.add_item("Dubai")

    enquiry.click_save()
    enquiry.validate_enquiry_created()

    # ---------------- FOLLOWUP ----------------
    enquiry.open_followup_modal()
    enquiry.select_followup_status("Interested")
    enquiry.handle_lead_quality_if_visible("Hot")
    enquiry.enter_business_value("50000")
    enquiry.enter_followup_description("Test followup description")
    enquiry.set_followup_date()
    enquiry.save_followup()
    enquiry.validate_followup_saved()

    # ---------------- QUOTATION THROUGH ENQUIRY ----------------
    enquiry.click_create_quotation()

    quotation = EnquiryQuotationPage(driver)
    quotation.wait_for_page_load()

    quotation.set_valid_upto()
    quotation.set_next_followup()
    quotation.capture_quotation_number()
    quotation.handle_lead_quality("Cold")
    quotation.handle_description()
    quotation.update_rate("10000")
    quotation.click_save()
    quotation.wait_for_overview()


    #-------------------------------- quotation 1st Followup-----------------------------------------------------------
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

