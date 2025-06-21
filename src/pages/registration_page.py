import allure
import random
import string
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.pages.base_page import BasePage


class PageRegistration(BasePage):
    FIRSTNAME = (By.ID, "input-firstname")
    LASTNAME = (By.ID, "input-lastname")
    EMAIL = (By.ID, "input-email")
    PASSWORD = (By.ID, "input-password")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    REGISTER_LINK = (By.XPATH, "//*[text()='My Account']")
    REGISTER_BUTTON = (By.LINK_TEXT, "Register")
    AGREEMENT_CHECKBOX = (By.NAME, "agree")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div#content h1")
    ERROR_ALERT = (By.CSS_SELECTOR, "div.alert-danger")

    def generate_test_data(self):
        """Генерация тестовых данных"""

        def random_string(length=6):
            return ''.join(random.choice(string.ascii_letters) for _ in range(length))

        data = {
            'firstname': f"Test_{random_string()}",
            'lastname': f"User_{random_string()}",
            'email': f"test_{random_string()}@example.com",
            'password': f"Pass_{random_string()}123!"
        }
        self.logger.info(f"Generated test data: {data}")
        return data

    def navigate_to_register(self):
        """Переход на страницу регистрации"""
        self.logger.info("Navigating to registration page")
        WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(self.REGISTER_LINK)
        ).click()
        WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(self.REGISTER_BUTTON)
        ).click()
        WebDriverWait(self.browser, 10).until(
            EC.title_contains("Register")
        )

    def register_user(self, first_name=None, last_name=None, email=None, password=None):
        """Регистрация пользователя"""
        test_data = self.generate_test_data()

        # Используем переданные данные или сгенерированные
        data = {
            'firstname': first_name or test_data['firstname'],
            'lastname': last_name or test_data['lastname'],
            'email': email or test_data['email'],
            'password': password or test_data['password']
        }

        self.logger.info(f"Registering user with data: {data}")

        # Заполнение формы
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(self.FIRSTNAME)
        ).send_keys(data['firstname'])

        self.browser.find_element(*self.LASTNAME).send_keys(data['lastname'])
        self.browser.find_element(*self.EMAIL).send_keys(data['email'])
        self.browser.find_element(*self.PASSWORD).send_keys(data['password'])

        # Согласие с условиями
        WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(self.AGREEMENT_CHECKBOX)
        ).click()

        # Отправка формы
        WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(self.CONTINUE_BUTTON)
        ).click()

        return data

    def is_registration_successful(self):
        """Проверка успешной регистрации"""
        try:
            # Ждем либо сообщение об успехе, либо ошибку
            WebDriverWait(self.browser, 10).until(
                lambda d: d.find_elements(*self.SUCCESS_MESSAGE) or d.find_elements(*self.ERROR_ALERT)
            )

            # Проверяем успешное сообщение
            success_elements = self.browser.find_elements(*self.SUCCESS_MESSAGE)
            if success_elements:
                success_text = success_elements[0].text
                self.logger.info(f"Registration success message: {success_text}")
                return True

            # Если есть ошибка - логируем ее
            error_elements = self.browser.find_elements(*self.ERROR_ALERT)
            if error_elements:
                error_text = error_elements[0].text
                self.logger.error(f"Registration failed: {error_text}")
                allure.attach(
                    error_text,
                    name="Registration Error",
                    attachment_type=allure.attachment_type.TEXT
                )
                return False
            return None

        except Exception as e:
            self.logger.error(f"Error checking registration status: {str(e)}")
            return False
