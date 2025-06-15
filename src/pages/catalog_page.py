import allure
from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage


class PageCatalog(BasePage):
    COMPARE_TOTAL_BUTTON = By.CSS_SELECTOR, "#compare-total"
    GRID_BUTTON = By.CSS_SELECTOR, "#button-grid"
    LIST_BUTTON = By.CSS_SELECTOR, "#button-list"
    ITEM = By.CSS_SELECTOR, ".product-thumb"
    ALERT = By.CSS_SELECTOR, ".alert"

    ACTUAL_PRICE = (By.CSS_SELECTOR, ".price-new")

    @allure.step('Getting current currency')
    def get_current_currency(self):
        self.logger.info(f"{self.class_name}: Getting current currency")
        return [product.find_element(*self.ACTUAL_PRICE).text
                for product in self.browser.find_elements(*self.ITEM)]
