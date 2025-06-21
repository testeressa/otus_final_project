import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.pages.base_page import BasePage


class Header(BasePage):
    CURRENCY_DROPDOWN = (By.CSS_SELECTOR, "#form-currency")
    CURRENCY_OPTIONS = (By.CSS_SELECTOR, ".dropdown-menu.show .dropdown-item")
    CURRENCY_MAP = {
        "EUR": 0,
        "GBP": 1,
        "USD": 2
    }
    CURRENCY_SYMBOLS = {
        "EUR": "€",
        "GBP": "£",
        "USD": "$"
    }

    @allure.step('Opening current currency')
    def open_currency_dropdown(self):
        self.logger.debug(f"{self.class_name}: Opening currency dropdown")
        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable(self.CURRENCY_DROPDOWN)).click()

    @allure.step('Selecting currency {currency}')
    def select_currency(self, currency="EUR"):
        """Выбирает валюту по коду (EUR, GBP, USD)"""
        self.logger.info(f"Selecting currency: {currency}")

        if currency not in self.CURRENCY_SYMBOLS:
            raise ValueError(f"Неподдерживаемая валюта: {currency}. Доступные: {list(self.CURRENCY_SYMBOLS.keys())}")

        self.open_currency_dropdown()

        currencies = WebDriverWait(self.browser, 20).until(
            EC.visibility_of_all_elements_located(self.CURRENCY_OPTIONS)
        )

        target_currency = self.CURRENCY_SYMBOLS[currency]
        for currency_element in currencies:
            if target_currency in currency_element.text:
                currency_element.click()
                return

        raise ValueError(f"Валюта {currency} не найдена в dropdown")

    @allure.step('Getting current currency symbol')
    def get_current_currency(self):
        """Возвращает символ текущей валюты"""
        return WebDriverWait(self.browser, 20).until(
            EC.visibility_of_element_located(self.CURRENCY_DROPDOWN)
        ).text.strip()

    @allure.step('Switching currency')
    def switch_currency(self):
        self.logger.info(f"{self.class_name}: Switching currency")
        self.open_currency_dropdown()
        self.select_currency()
