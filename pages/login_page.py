import pyotp

from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from config import Config


class LoginPage(BasePage):
    _EMAIL_LABEL_NAME = "Email"
    _PASSWORD_LABEL_NAME = "Пароль"
    _SUBMIT_BUTTON_NAME = "Войти"
    _PIN_INPUT_LOCATOR = ".pin-input"
    _CONFIRM_BUTTON_NAME = "Подтвердить"

    def __init__(self, page: Page):
        super().__init__(page)

    def open(self):
        self.open_url(Config.BASE_URL)

    def login(self, email: str, password: str):
        self.page.get_by_label(self._EMAIL_LABEL_NAME).fill(email)
        self.page.get_by_label(self._PASSWORD_LABEL_NAME).fill(password)
        self.click_button(self._SUBMIT_BUTTON_NAME)

    def enter_2fa_code_for_dev(self):
        expect(self.page).to_have_url(f'{Config.BASE_URL}/activate-two-fa')
        self.page.reload(wait_until="networkidle")

    def enter_2fa_code_for_prod(self, secret_key: str):
        totp = pyotp.TOTP(secret_key)
        current_code = totp.now()
        self.page.locator(self._PIN_INPUT_LOCATOR).first.click()
        self.page.keyboard.type(f"{current_code}", delay=100)  # delay имитирует ввод человека
        self.click_button(self._CONFIRM_BUTTON_NAME)
