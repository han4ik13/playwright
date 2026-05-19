from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage
from config import Config


class LeadPage(BasePage):
    # Поиск по тексту
    _SIDEBAR_NEW_BUY_DEAL = "Новая сделка"
    _DC_NAME = "Mycar Almaty"
    _BUTTON_NAME = "Выкуп"
    _IIN_INPUT_NAME = "Поиск клиента"
    _VIN_INPUT_NAME = "Поиск по VIN"
    _NEXT_BTN_NAME = "Далее"
    _CREATE_BTN = "Создать"
    _DEAL_TYPE_NEXT_BTN = "deal-type__next"
    _LEAD_CLIENT_NEXT_BTN = "lead-client__next"

    # поиск по data-test
    _ORGS_SELECT = "deal-type__org"
    _SERIES_NUMBER = "new-car-technical-passport__passport-series-number"
    _ISSUE_DATE = "new-car-technical-passport__passport-issue-date"
    _REGISTRATION_NUMBER = "new-car-technical-passport__registration-number"
    _LAST_NAME = "new-car-technical-passport__owner-last-name"
    _FIRST_NAME = "new-car-technical-passport__owner-first-name"
    _NEXT_BTN = "new-car-coupe-type__next"
    _GENERATION_LIST = "new-car-generation__generation"
    _MODIFICATION_LIST = "new-car-characteristics__modification"
    _FINISH_BTN = "new-car-characteristics__next"

    # поиск по локатору
    _DROPDOWN_LIST_LOCATOR = ".mcp-select__dd-list"
    _DROPDOWN_ITEM_LOCATOR = ".mcp-select__dd-item"
    _ACTIVE_DROPDOWN_LOCATOR = ".app-dropdown__menu-wrap.is-open"
    _CLOSE_MODAL_BTN = ".mcp-btn--icon-plain"
    _BRAND_BTN_LOCATOR = ".deal-brand__btn"
    _MODEL_BTN_LOCATOR = ".deal-model__btn"
    _YEAR_BTN_LOCATOR = ".deal-year__btn"
    _COUPE_TYPE_LOCATOR = ".coupe-type__card"
    _COUPE_TYPE_ACTIVE_LOCATOR = ".coupe-type__card.is-active"

    def __init__(self, page: Page):
        super().__init__(page)
        self.dc_selectors = page.get_by_test_id(self._ORGS_SELECT)
        self.dropdown_list = page.locator(self._DROPDOWN_LIST_LOCATOR)
        self.dropdown_item = page.locator(self._DROPDOWN_ITEM_LOCATOR)

    def add_type_buy_deal(self):
        self.navigate_sidebar(self._SIDEBAR_NEW_BUY_DEAL)
        expect(self.page).to_have_url(f"{Config.BASE_URL}/tradein/buy-deal/lead/")

        for i in range(2):
            self.dc_selectors.nth(i).click()
            self.dropdown_list.last.get_by_text(self._DC_NAME, exact=True).click(force=True)

        self.page.get_by_text(self._BUTTON_NAME, exact=True).click()
        self.click_button_by_data_test(self._DEAL_TYPE_NEXT_BTN)

    def add_client(self, iin: str):
        self.page.get_by_placeholder(self._IIN_INPUT_NAME).fill(iin)
        self.click_by_locator(self._ACTIVE_DROPDOWN_LOCATOR)
        close_btn = self.page.locator(self._CLOSE_MODAL_BTN)
        try:
            close_btn.wait_for(state="visible", timeout=5000)
            close_btn.click()
        except PlaywrightTimeoutError:
            pass  # модальное окно не появилось — ок
        self.click_button_by_data_test(self._LEAD_CLIENT_NEXT_BTN)

    def add_new_car(self,
                    vin: str,
                    series_number: str,
                    issue_date: str,
                    registration_number: str,
                    last_name: str,
                    first_name: str
                    ):
        self.page.get_by_label(self._VIN_INPUT_NAME).fill(vin)
        self.click_button(self._CREATE_BTN)

        self.page.get_by_test_id(self._SERIES_NUMBER).fill(series_number)
        self.page.get_by_test_id(self._ISSUE_DATE).fill(issue_date)
        self.page.get_by_test_id(self._REGISTRATION_NUMBER).fill(registration_number)
        self.page.get_by_test_id(self._LAST_NAME).fill(last_name)
        self.page.get_by_test_id(self._FIRST_NAME).fill(first_name)
        self.click_button(self._NEXT_BTN_NAME)

        for selector in [self._BRAND_BTN_LOCATOR, self._MODEL_BTN_LOCATOR, self._YEAR_BTN_LOCATOR]:
            self.click_by_locator(selector)

        self.click_button_by_data_test(self._GENERATION_LIST)
        self.dropdown_item.first.click()

        if self.page.locator(self._COUPE_TYPE_ACTIVE_LOCATOR).count() == 0:
            self.page.locator(self._COUPE_TYPE_LOCATOR).first.click()
        self.click_button_by_data_test(self._NEXT_BTN)

        self.click_button_by_data_test(self._MODIFICATION_LIST)
        self.dropdown_item.first.click()

        self.click_button_by_data_test(self._FINISH_BTN)
