import re
import time

import psycopg2
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage
from config import Config


class AssessmentPage(BasePage):

    _ADD_ASSESSMENT_BTN_TEXT = "Оценка"
    _MODAL_NAME = "Добавление оценки"
    _CONFIRM_BUTTON_NAME = "Сохранить"

    _ADD_ASSESSMENT_BTN_LOCATOR = ".card-auto-actions__btn"
    _PIN_INPUT_LOCATOR = ".pin-input"
    _COLOR_BTN = ".block__color"

    def __init__(self, page: Page):
        super().__init__(page)

    def _get_buy_deal_id(self) -> str:
        match = re.search(r"/buy-deal/(\d+)/", self.page.url)
        if not match:
            raise ValueError(f"Не удалось извлечь buy_deal_id из URL: {self.page.url}")
        return match.group(1)

    def _get_verification_code(self, buy_deal_id: str, timeout: int = 10, interval: float = 2.0) -> str:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
        )
        try:
            deadline = time.time() + timeout
            while time.time() < deadline:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT g.verification_code FROM garage g WHERE g.buy_deal_id = %s",
                        (buy_deal_id,)
                    )
                    row = cur.fetchone()
                    if row and row[0]:
                        return str(row[0])
                time.sleep(interval)
            raise TimeoutError(f"Код не появился в БД за {timeout}с для buy_deal_id={buy_deal_id}")
        finally:
            conn.close()

    def add_assessment(self):
        self._click(
            self.page.locator(self._ADD_ASSESSMENT_BTN_LOCATOR).filter(has_text=self._ADD_ASSESSMENT_BTN_TEXT)
        )
        otp_modal = self.page.get_by_text(self._MODAL_NAME)
        try:
            otp_modal.wait_for(state="visible", timeout=5000)
            current_code = self._get_verification_code(self._get_buy_deal_id())
            self.page.locator(self._PIN_INPUT_LOCATOR).first.click()
            self.page.keyboard.type(current_code, delay=100)
            self.click_button(self._CONFIRM_BUTTON_NAME)
        except PlaywrightTimeoutError:
            pass

    def add_color_mileage(self):
        self.click_button(self._COLOR_BTN)

