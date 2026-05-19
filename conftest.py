import pytest
from playwright.sync_api import Browser

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
        "args": [
            "--start-maximized",
            "--window-size=1920,1080"
        ]
    }

# 1. Создаем один контекст на всю сессию
@pytest.fixture(scope="session")
def browser_context(browser: Browser, browser_context_args):
    # ВАЖНО: передаем browser_context_args сюда!
    context = browser.new_context(**browser_context_args)
    yield context
    context.close()

# 2. Создаем одну страницу на всю сессию
@pytest.fixture(scope="session")
def page(browser_context):
    page = browser_context.new_page()
    yield page
    page.close()  # Необязательно, закроется вместе с контекстом

@pytest.fixture(scope="session", autouse=True)
def configure_selectors(playwright):
    playwright.selectors.set_test_id_attribute("data-test")

@pytest.fixture()
def client_iin():
    return '020630501048'