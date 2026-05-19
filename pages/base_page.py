from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open_url(self, url: str):
        self.page.goto(url)

    def click_button(self, name: str):
        btn = self.page.get_by_role("button", name=name)
        btn.wait_for(state="visible", timeout=5000)
        btn.click()

    def click_button_by_data_test(self, data_test: str):
        btn = self.page.get_by_test_id(data_test)
        btn.wait_for(state="visible", timeout=5000)
        btn.click()

    def navigate_sidebar(self, name: str):
        self.page.get_by_role("link", name=name).click()

    def click_by_locator(self, locator):
        element = self.page.locator(locator).first
        element.wait_for(state="visible")
        element.click()
