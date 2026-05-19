import re

from playwright.sync_api import expect

from config import Config
from pages.lead_page import LeadPage


def test_login_page(login, page):
    expect(page).to_have_url(re.compile(f"{Config.BASE_URL}/tradein"))


def test_lead_page(
        login,
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

