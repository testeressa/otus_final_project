from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage


class PageProduct(BasePage):
    ADD_TO_CARD_BUTTON = By.CSS_SELECTOR, "#button-cart"
    OLD_PRICE = By.CSS_SELECTOR, ".price-old"
    SELECT_COLOR = By.CSS_SELECTOR, ".form-select"
