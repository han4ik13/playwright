import re
import time

from playwright.sync_api import expect

from config import Config
from pages.login_page import LoginPage
from pages.lead_page import LeadPage


def test_login_page(page):
    login_page = LoginPage(page)

    login_page.open()
    expect(page).to_have_title("Mycar Pro")
    login_page.login(
        email=Config.EMAIL,
        password=Config.PASSWORD
    )
    if Config.SECRET_KEY != '':
        login_page.enter_2fa_code_for_prod(secret_key=Config.SECRET_KEY)
    else:
        login_page.enter_2fa_code_for_dev()
    expect(page).to_have_url(re.compile(f"{Config.BASE_URL}/tradein"))


def test_lead_page(
        page,
        client_iin,
        client_last_name,
        client_first_name,
        car_vin,
        car_issue_date,
        car_series_number,
        car_registration_number
):
    lead_page = LeadPage(page)

    lead_page.add_type_buy_deal()
    lead_page.add_client(iin=client_iin)
    lead_page.add_new_car(
        vin=car_vin,
        series_number=car_series_number,
        issue_date=car_issue_date,
        registration_number=car_registration_number,
        last_name=client_last_name,
        first_name=client_first_name
    )

    time.sleep(5)
