import re

import pytest
from faker import Faker
from playwright.sync_api import Browser, expect

from config import Config
from pages.login_page import LoginPage

faker = Faker()

Config.validate()


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1650,
            "height": 1080
        }
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "args": ["--window-size=1650,1080"]
    }


# Создаем один контекст на всю сессию
@pytest.fixture(scope="session")
def browser_context(browser: Browser, browser_context_args):
    # ВАЖНО: передаем browser_context_args сюда!
    context = browser.new_context(**browser_context_args)
    yield context
    context.close()


@pytest.fixture(scope="session", autouse=True)
def configure_selectors(playwright):
    playwright.selectors.set_test_id_attribute("data-test")


# Создаем одну страницу на всю сессию
@pytest.fixture(scope="session")
def page(browser_context, configure_selectors):
    page = browser_context.new_page()
    yield page
    page.close()  # Необязательно, закроется вместе с контекстом


@pytest.fixture(scope="session")
def login(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(email=Config.EMAIL, password=Config.PASSWORD)
    if Config.SECRET_KEY:
        login_page.enter_2fa_code_for_prod(secret_key=Config.SECRET_KEY)
    else:
        login_page.enter_2fa_code_for_dev()
    expect(page).to_have_url(re.compile(f"{Config.BASE_URL}/tradein"))


@pytest.fixture()
def client_iin():
    return '020630501048'


@pytest.fixture()
def client_last_name():
    return faker.last_name()


@pytest.fixture()
def client_first_name():
    return faker.first_name()


@pytest.fixture()
def car_vin():
    return faker.vin()


@pytest.fixture()
def car_series_number():
    return faker.bothify(text='###???##').upper()


@pytest.fixture()
def car_issue_date():
    return faker.date_this_month().strftime("%d.%m.%Y")


@pytest.fixture()
def car_registration_number():
    return faker.bothify(text='###???##').upper()
