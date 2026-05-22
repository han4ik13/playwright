import re

import psycopg2
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage
from config import Config


class AssessmentPage(BasePage):

    _ADD_ASSESSMENT_BTN = "Оценка"
    _MODAL_NAME = "Добавление оценки"
    _PIN_INPUT_LOCATOR = ".pin-input"
    _CONFIRM_BUTTON_NAME = "Сохранить"

    def __init__(self, page: Page):
        super().__init__(page)

    def _get_buy_deal_id(self) -> str:
        match = re.search(r"/buy-deal/(\d+)/", self.page.url)
        if not match:
            raise ValueError(f"Не удалось извлечь buy_deal_id из URL: {self.page.url}")
        return match.group(1)

    def _get_verification_code(self, buy_deal_id: str) -> str:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
        )
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT g.verification_code FROM garage g WHERE g.buy_deal_id = %s",
                    (buy_deal_id,)
                )
                row = cur.fetchone()
                if not row:
                    raise ValueError(f"Код не найден для buy_deal_id={buy_deal_id}")
                return str(row[0])
        finally:
            conn.close()

    def add_assessment(self):
        self.click_button(self._ADD_ASSESSMENT_BTN)
        otp_modal = self.page.get_by_text(self._MODAL_NAME)
        try:
            otp_modal.wait_for(state="visible", timeout=5000)
            current_code = self._get_verification_code(self._get_buy_deal_id())
            self.page.locator(self._PIN_INPUT_LOCATOR).first.click()
            self.page.keyboard.type(current_code, delay=100)
            self.click_button(self._CONFIRM_BUTTON_NAME)
        except PlaywrightTimeoutError:
            pass
