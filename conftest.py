from playwright.sync_api import Page
import pytest
from config import PASSWORD, STANDARD_USER
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage


#фикстура с авторизацией/добавлением 1 товара в корзину/переходом к заполнению формы при покупке
@pytest.fixture()
def fixture_login_add_item_checkout(page: Page):

    #создаём объекты Page Object
    login_page = LoginPage(page)
    cart_page = CartPage(page)
    inventory_page = InventoryPage(page)

    login_page.open()  #переходим на сайт
    login_page.login(STANDARD_USER, PASSWORD)  #авторизуемся

    cart_page.add_sauce_labs_backpack()  #добавляем в корзину первый объект

    inventory_page.catalog_to_cart()  #переходим в корзину

    #инициируем процесс оформления товара
    button_checkout = page.locator('#checkout')
    button_checkout.click()

    return page


#фикстура с авторизацией/добавлением 3 товаров в корзину/переходом к заполнению формы при покупке
@pytest.fixture()
def fixture_login_add_three_item_checkout(page: Page):

    #создаём объекты Page Object
    login_page = LoginPage(page)
    cart_page = CartPage(page)
    inventory_page = InventoryPage(page)

    login_page.open()  #переходим на сайт
    login_page.login(STANDARD_USER, PASSWORD)  #авторизуемся

    # добавляем товары в корзину
    cart_page.add_sauce_labs_backpack()  #добавляем в корзину первый объект
    cart_page.add_sauce_labs_bike_light()  #добавляем в корзину второй объект
    cart_page.add_sauce_labs_bolt_t_shirt()  #добавляем в корзину третий объект

    inventory_page.catalog_to_cart()  #переходим в корзину

    #инициируем процесс оформления товара
    button_checkout = page.locator('#checkout')
    button_checkout.click()

    return page
