from playwright.sync_api import Page, Locator

DEFAULT_TIMEOUT = 10000


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def _click(self, locator: Locator):
        locator.wait_for(state="visible", timeout=DEFAULT_TIMEOUT)
        locator.click()

    def open_url(self, url: str):
        self.page.goto(url, wait_until="networkidle")

    def click_button(self, name: str):
        self._click(self.page.get_by_role("button", name=name))

    def click_button_by_data_test(self, data_test: str):
        self._click(self.page.get_by_test_id(data_test))

    def navigate_sidebar(self, name: str):
        self._click(self.page.get_by_role("link", name=name))

    def click_by_locator(self, locator: str):
        self._click(self.page.locator(locator).first)
