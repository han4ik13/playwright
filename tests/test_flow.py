import re
import time

from playwright.sync_api import expect
from faker import Faker

from config import Config
from pages.login_page import LoginPage
from pages.lead_page import LeadPage

faker = Faker()

VIN = faker.vin()
SERIES_NUMBER = faker.bothify(text='###???##').upper()
ISSUE_DATE = faker.date_this_month().strftime("%d.%m.%Y")
REGISTRATION_NUMBER = faker.bothify(text='###???##').upper()
LAST_NAME = faker.last_name()
FIRST_NAME = faker.first_name()


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



def test_lead_page(page, client_iin):
    lead_page = LeadPage(page)

    lead_page.add_type_buy_deal()
    lead_page.add_client(iin=client_iin)
    lead_page.add_new_car(VIN, SERIES_NUMBER, ISSUE_DATE, REGISTRATION_NUMBER, LAST_NAME, FIRST_NAME)

    time.sleep(5)
