import random
import string
from datetime import datetime

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.pages.base_page import BasePage


class PageAdmin(BasePage):

    USERNAME = 'user'
    PASSWORD = 'bitnami'
    INPUT_USERNAME = (By.CSS_SELECTOR, "#input-username")
    INPUT_PASSWORD = (By.NAME, "password")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "[type = 'submit']")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "#nav-logout")
    CATALOG_MENU = (By.CSS_SELECTOR, "#menu-catalog .fa-solid.fa-tag")
    PRODUCTS_LINK = (By.XPATH, "//a[contains(text(), 'Products')]")
    ADD_NEW_BUTTON = (By.CSS_SELECTOR, ".fa-plus")
    PRODUCT_NAME_INPUT = (By.CSS_SELECTOR, "#input-name-1")
    META_TAG_INPUT = (By.CSS_SELECTOR, "#input-meta-title-1.form-control")
    DATA_TAB = (By.CSS_SELECTOR, "a[href='#tab-data']")
    MODEL_INPUT = (By.CSS_SELECTOR, "#input-model.form-control")
    SAVE_BUTTON = (By.CSS_SELECTOR, "[type = 'submit']")
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")
    SEO_TAB = (By.CSS_SELECTOR, "a[href='#tab-seo']")
    SEO_KEYWORD_INPUT = (By.CSS_SELECTOR, "#input-keyword-0-1")
    CHECKBOX_PRODUCT = (By.CSS_SELECTOR, "input[type='checkbox'][name='selected[]']")
    DELETE_BUTTON = (By.CSS_SELECTOR, ".btn.btn-danger")
    CONFIRM_DELETE = (By.CSS_SELECTOR, ".btn-danger")
    PRODUCTS_COUNTER = (By.CSS_SELECTOR, ".col-sm-6.text-end")

    @allure.step('Filling in username input')
    def input_username(self):
        self.logger.info(f"{self.class_name}: Filling in username input")
        self.browser.find_element(*self.INPUT_USERNAME).clear()
        self.browser.find_element(*self.INPUT_USERNAME).send_keys(self.USERNAME)

    @allure.step('Filling in password')
    def input_password(self):
        self.logger.info(f"{self.class_name}: Filling in password")
        self.browser.find_element(*self.INPUT_PASSWORD).clear()
        self.browser.find_element(*self.INPUT_PASSWORD).send_keys(self.PASSWORD)

    @allure.step('Clicking SUBMIT_BUTTON')
    def submit_login(self):
        self.logger.debug(f"{self.class_name}: Clicking 'SUBMIT_BUTTON'")
        self.browser.find_element(*self.SUBMIT_BUTTON).click()

    @allure.step('Checking name displaying')
    def name_is_displayed(self):
        self.logger.debug(f"{self.class_name}: Checking name displaying")
        return self.browser.find_element(By.CSS_SELECTOR, "[alt = 'John Doe']").is_displayed()

    @allure.step('Checking LOGOUT_BUTTON displaying')
    def logout_button_is_displayed(self):
        self.logger.debug(f"{self.class_name}: Checking 'LOGOUT_BUTTON' displaying")
        return WebDriverWait(self.browser, 2).until(
            EC.element_to_be_clickable(self.LOGOUT_BUTTON))

    @allure.step('Logging out')
    def logout(self):
        self.logger.info(f"{self.class_name}: Logging out")
        self.browser.find_element(*self.LOGOUT_BUTTON).click()

    @allure.step('Logging admin page')
    def login_admin_page(self):
        self.logger.info(f"{self.class_name}: Logging admin page")
        self.input_username()
        self.input_password()
        self.submit_login()

    @allure.step('Waiting for title displayed')
    def wait_for_title(self, timeout=2, title_text="Dashboard"):
        self.logger.debug(f"{self.class_name}: Waiting for title {title_text}")
        WebDriverWait(self.browser, timeout).until(EC.title_contains(title_text))

    @allure.step('Going to products page')
    def navigate_to_products(self):
        self.logger.info(f"{self.class_name}: Going to products page")
        catalog_menu = WebDriverWait(self.browser, 2).until(
            EC.visibility_of_element_located(self.CATALOG_MENU))
        catalog_menu.click()
        product_menu = WebDriverWait(self.browser, 2).until(
            EC.visibility_of_element_located(self.PRODUCTS_LINK))
        product_menu.click()

    @allure.step('Switching tabs')
    def switch_to_tab(self, tab_name):
        self.logger.debug(f"{self.class_name}: Switching tabs")
        data_tab = WebDriverWait(self.browser, 2).until(
            EC.element_to_be_clickable(tab_name))
        data_tab.click()

    @allure.step('Adding new product')
    def add_new_product(self, product_name, meta_tag, model_name, keyword_name):
        self.logger.info(f"{self.class_name}: Adding new product")
        WebDriverWait(self.browser, 2).until(
            EC.visibility_of_element_located(self.ADD_NEW_BUTTON)
        ).click()

        WebDriverWait(self.browser, 2).until(
            EC.visibility_of_element_located(self.PRODUCT_NAME_INPUT)
        ).send_keys(product_name)

        WebDriverWait(self.browser, 2).until(
            EC.visibility_of_element_located(self.META_TAG_INPUT)
        ).send_keys(meta_tag)

        self.switch_to_tab(self.DATA_TAB)

        WebDriverWait(self.browser, 2).until(
            EC.visibility_of_element_located(self.MODEL_INPUT)
        ).send_keys(model_name)

        self.switch_to_tab(self.SEO_TAB)

        WebDriverWait(self.browser, 2).until(
            EC.visibility_of_element_located(self.SEO_KEYWORD_INPUT)
        ).send_keys(keyword_name)

        WebDriverWait(self.browser, 2).until(
            EC.visibility_of_element_located(self.SAVE_BUTTON)
        ).click()

    @allure.step('Counting products')
    def get_products_count(self):
        self.logger.debug(f"{self.class_name}: Counting products")
        products_count_text = WebDriverWait(self.browser, 2).until(
            EC.visibility_of_element_located(self.PRODUCTS_COUNTER)
        ).text
        text_split = products_count_text.split("of")[1].split("(")[0].strip()
        return int(text_split)

    @allure.step('Checking success message displaying')
    def is_success_message_displayed(self):
        self.logger.debug(f"{self.class_name}: Checking success message displaying")
        return WebDriverWait(self.browser, 2).until(
            EC.visibility_of_element_located(self.SUCCESS_ALERT)
        ).is_displayed()

    @allure.step('Deleting product')
    def delete_product(self):
        self.logger.info(f"{self.class_name}: Deleting product")
        self.browser.find_element(*self.CHECKBOX_PRODUCT).click()
        self.browser.find_element(*self.DELETE_BUTTON).click()
        Alert(self.browser).accept()

    def generate_test_data(self):
        def generate_random_string(length=6):
            return ''.join(random.choice(string.ascii_letters) for _ in range(length))

        data = {
            "product_name": f"Test Product {generate_random_string()}",
            "meta_tag": f"Meta Tag {generate_random_string(5)}",
            "model": generate_random_string(5),
            "keyword": generate_random_string(3),
            "description": f"Autogenerated product {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        }
        self.logger.info(f"Generated test data: {data}")
        return data

