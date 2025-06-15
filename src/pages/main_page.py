import allure
from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage


class PageMain(BasePage):
    LOGO_BUTTON = (By.ID, "logo")
    SEARCH = (By.NAME, "search")
    CURRENCY_BUTTON = (By.XPATH, "//*[text()='Currency']")
    ACTUAL_PRICE = (By.CSS_SELECTOR, ".price-new")
    PRODUCT_CARD = (By.CSS_SELECTOR, ".product-thumb")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".price-new, .price")

    @allure.step('Getting current currency')
    def get_current_currency(self):
        self.logger.info(f"{self.class_name}: Getting current currency")
        products = self.browser.find_elements(*self.PRODUCT_CARD)
        return [product.find_element(*self.PRODUCT_PRICE).text for product in products]

