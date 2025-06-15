import allure
import pytest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.pages.admin_page import PageAdmin
from src.pages.catalog_page import PageCatalog
from src.pages.main_page import PageMain
from src.pages.header_element import Header
from src.pages.registration_page import PageRegistration
from src.pages.shopping_cart_page import PageShoppingCart


@allure.title("Проврека логина, разлогина в админке")
def test_login_succeed_and_logout(browser, ):
    page_admin = PageAdmin(browser)
    page_admin.open(browser.url + "/administration")
    page_admin.login_admin_page()
    page_admin.wait_for_title()

    assert "Dashboard" in browser.title, "Редирект на страницу дашборда не выполнен"
    assert page_admin.logout_button_is_displayed(), "Кнопка логаута на странице не обнаружена"
    assert page_admin.name_is_displayed(), "Имя пользователя не выводится"

    page_admin.logout()
    page_admin.wait_for_title(title_text="Administration")

    assert "Administration" in browser.title, "Пользователь не разлогинен"


@allure.title("Проврека добавления товара в корзину")
def test_add_item(browser):
    page_shopping_cart = PageShoppingCart(browser)
    page_shopping_cart.open(browser.url + "/home")

    page_shopping_cart.add_item_to_cart()

    page_shopping_cart.open(browser.url + '/en-gb?route=checkout/cart')
    shopping_cart = page_shopping_cart.get_shopping_cart_items()

    assert len(shopping_cart) == 1, 'Товар не был добавлен в корзину'


@allure.title("Проврека изменения валюты на главной странице")
def test_currency_change_main_page(browser):
    page_main = PageMain(browser)
    page_main.open(browser.url + "/home")
    initial_currency = page_main.get_current_currency()

    header = Header(browser)
    header.select_currency("EUR")

    updated_currency = page_main.get_current_currency()

    assert initial_currency != updated_currency, 'Изменение валюты не применилось'


@allure.title("Проверка изменения валюты в каталоге")
def test_currency_change_catalog(browser):
    with allure.step("1. Открываем страницу каталога"):
        page_catalog = PageCatalog(browser)
        page_catalog.open(browser.url + "/catalog/desktops")
        initial_currency = page_catalog.get_current_currency()
        allure.attach(
            f"Начальная валюта: {initial_currency}",
            name="Initial Currency",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("2. Меняем валюту на EUR"):
        header = Header(browser)
        header.select_currency()

    with allure.step("3. Проверяем изменение валюты"):
        updated_currency = page_catalog.get_current_currency()
        allure.attach(
            f"Новая валюта: {updated_currency}",
            name="Updated Currency",
            attachment_type=allure.attachment_type.TEXT
        )
        assert initial_currency != updated_currency, (
            f"Валюта не изменилась. Было: {initial_currency}, стало: {updated_currency}"
        )


@allure.title("Проврека добавления товара в админке")
def test_add_new_product(browser):
    page_admin = PageAdmin(browser)
    with allure.step("1. Авторизация в админке"):
        page_admin.open(browser.url + "/administration")
        page_admin.login_admin_page()

    with allure.step("2. Навигация к списку товаров"):
        page_admin.navigate_to_products()
        initial_products_count = page_admin.get_products_count()

    with allure.step("3. Добавление нового товара с рандомными данными"):
        test_data = page_admin.generate_test_data()
        allure.attach(
            str(test_data),
            name="Сгенерированные тестовые данные",
            attachment_type=allure.attachment_type.TEXT
        )

        page_admin.add_new_product(
            product_name=test_data["product_name"],
            meta_tag=test_data["meta_tag"],
            model_name=test_data["model"],
            keyword_name=test_data["keyword"]
        )

    with allure.step("4. Проверка сообщения об успешном добавлении"):
        assert page_admin.is_success_message_displayed(), "Сообщение о добавлении товара не отображено"

    with allure.step("5. Проверка увеличения количества товаров"):
        page_admin.navigate_to_products()
        updated_products_count = page_admin.get_products_count()
        assert initial_products_count < updated_products_count, (
            f"Количество товаров не изменилось. Было: {initial_products_count}, стало: {updated_products_count}"
        )

    assert initial_products_count < updated_products_count, "Товар не был добавлен"


@allure.title("Проврека удаления товара в админке")
def test_delete_product(browser):
    page_admin = PageAdmin(browser)
    page_admin.open(browser.url + "/administration")
    page_admin.login_admin_page()
    page_admin.navigate_to_products()
    page_admin.delete_product()
    assert page_admin.is_success_message_displayed(), "Товар не был удален"


@allure.title("Проверка регистрации нового пользователя")
def test_register_new_user(browser):
    page_reg = PageRegistration(browser)

    with allure.step("1. Открытие главной страницы"):
        page_reg.open(browser.url)
        assert "Your Store" in browser.title

    with allure.step("2. Переход на страницу регистрации"):
        page_reg.navigate_to_register()
        assert "Register Account" in browser.title

    with allure.step("3. Регистрация нового пользователя"):
        test_data = page_reg.register_user()
        allure.attach(
            str(test_data),
            name="Использованные тестовые данные",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("4. Проверка успешности регистрации"):
        assert page_reg.is_registration_successful(), (
            f"Регистрация не удалась. Использованные данные: {test_data}"
        )

@pytest.mark.parametrize("currency,currency_symbol", [
    ("EUR", "€"),
    ("GBP", "£"),
    ("USD", "$")
])
@allure.title("Проверка переключения между валютами")
def test_switch_currency(browser, currency, currency_symbol):

    header = Header(browser)
    page_main = PageMain(browser)

    with allure.step(f"Открываем главную страницу"):
        header.open(browser.url)
        WebDriverWait(browser, 5).until(
            EC.visibility_of_element_located(page_main.PRODUCT_CARD)
        )

    with allure.step(f"Переключаем валюту на {currency}"):
        header.select_currency(currency)
        WebDriverWait(browser, 5).until(
            lambda d: currency_symbol in page_main.get_current_currency()[0]
        )

    with allure.step(f"Проверяем, что текущая валюта {currency_symbol}"):
        current_currency = page_main.get_current_currency()
        # Check that ALL prices contain the currency symbol
        assert all(currency_symbol in price for price in current_currency), \
            f"Не все цены отображаются в валюте {currency}. Найдены цены: {current_currency}"
