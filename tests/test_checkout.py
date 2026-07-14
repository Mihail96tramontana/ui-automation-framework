from playwright.sync_api import expect, Page
from config import BASE_URL, PASSWORD, STANDARD_USER
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
import pytest


class TestCheckout:

    def test_proceed_to_checkout(self, page: Page):

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

        expect(page).to_have_url(f'{BASE_URL}checkout-step-one.html')
        expect(page.locator('#first-name')).to_be_visible()
        expect(page.locator('#last-name')).to_be_visible()
        expect(page.locator('#postal-code')).to_be_visible()
        expect(page.locator('#first-name')).to_have_attribute('placeholder','First Name')
        expect(page.locator('#last-name')).to_have_attribute('placeholder','Last Name')
        expect(page.locator('#postal-code')).to_have_attribute('placeholder','Zip/Postal Code')
        expect(page.locator('#continue')).to_be_visible()
        expect(page.locator('#cancel')).to_be_visible()
        expect(page.locator('.title')).to_be_visible()
        expect(page.locator('.title')).to_have_text('Checkout: Your Information')


    @pytest.mark.parametrize('first_name, last_name, postal_code, expected_text_error', [
        ('','','','Error: First Name is required'),
        ('','test','test','Error: First Name is required'),
        ('test','','test','Error: Last Name is required'),
        ('test','test','','Error: Postal Code is required')
    ])
    def test_empty_mandatory_fields(self, page: Page, first_name, last_name, postal_code, expected_text_error):

        #создаём объекты Page Object
        login_page = LoginPage(page)
        cart_page = CartPage(page)
        inventory_page = InventoryPage(page)

        login_page.open() #переходим на сайт
        login_page.login(STANDARD_USER, PASSWORD) #авторизуемся

        cart_page.add_sauce_labs_backpack() #добавляем в корзину первый объект

        inventory_page.catalog_to_cart() #переходим в корзину

        #инициируем процесс оформления товара
        button_checkout = page.locator('#checkout')
        button_checkout.click()

        #заполнение формы
        #ввод в поле First Name
        input_first_name = page.locator('#first-name')
        input_first_name.fill(first_name)
        #ввод в поле Last Name
        input_last_name = page.locator('#last-name')
        input_last_name.fill(last_name)
        #ввод в поле Zip/Postal Code
        input_postal_code = page.locator('#postal-code')
        input_postal_code.fill(postal_code)
        #клик по кнопке continue
        button_continue = page.locator('#continue')
        button_continue.click()

        #проверяем, что ошибка отображается корректно
        expect(page.locator('h3[data-test="error"]')).to_be_visible()
        expect(page.locator('h3[data-test="error"]')).to_have_text(expected_text_error)

    def test_checkout_to_catalog(self, page: Page):

        #создаём объекты Page Object
        login_page = LoginPage(page)
        cart_page = CartPage(page)
        inventory_page = InventoryPage(page)

        login_page.open() #переходим на сайт
        login_page.login(STANDARD_USER, PASSWORD) #авторизуемся

        #добавляем товары в корзину
        cart_page.add_sauce_labs_backpack() #добавляем в корзину первый объект
        cart_page.add_sauce_labs_bike_light() #добавляем в корзину второй объект
        cart_page.add_sauce_labs_bolt_t_shirt() #добавляем в корзину третий объект

        inventory_page.catalog_to_cart() #переходим в корзину

        #инициируем процесс оформления товара
        button_checkout = page.locator('#checkout')
        button_checkout.click()

        #возвращение назад в каталог из процесса оформления товара
        checkout_to_catalog = page.locator('.continue-shopping')
        checkout_to_catalog.click()

        #проверяем, что вернулись именно в каталог
        expect(page).to_have_url(f'{BASE_URL}inventory.html')

    def test_fill_checkout_form(self, page: Page):

        #создаём объекты Page Object
        login_page = LoginPage(page)
        cart_page = CartPage(page)
        inventory_page = InventoryPage(page)

        login_page.open() #переходим на сайт
        login_page.login(STANDARD_USER, PASSWORD) #авторизуемся

        #добавляем товары в корзину
        cart_page.add_sauce_labs_backpack() #добавляем в корзину первый объект
        cart_page.add_sauce_labs_bike_light() #добавляем в корзину второй объект
        cart_page.add_sauce_labs_bolt_t_shirt() #добавляем в корзину третий объект

        inventory_page.catalog_to_cart() #переходим в корзину

        #инициируем процесс оформления товара
        button_checkout = page.locator('#checkout')
        button_checkout.click()

        #заполнение формы
        #ввод в поле First Name
        input_first_name = page.locator('#first-name')
        input_first_name.fill('test_name')
        #ввод в поле Last Name
        input_last_name = page.locator('#last-name')
        input_last_name.fill('test_name')
        #ввод в поле Zip/Postal Code
        input_postal_code = page.locator('#postal-code')
        input_postal_code.fill('test_postal_code')
        #клик по кнопке continue
        button_continue = page.locator('#continue')
        button_continue.click()

        #проверки
        expect(page).to_have_url(f'{BASE_URL}checkout-step-two.html')

        all_name_item_correct = page.locator('.inventory_item_name').all_inner_texts()
        assert all_name_item_correct == [
            'Sauce Labs Backpack',
            'Sauce Labs Bike Light',
            'Sauce Labs Bolt T-Shirt'
        ]

        all_desc_item_correct = page.locator('.inventory_item_desc').all_inner_texts()
        assert all_desc_item_correct == [
            'carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.',
            "A red light isn't the desired state in testing but it sure helps when riding your bike at night. Water-resistant with 3 lighting modes, 1 AAA battery included.",
            'Get your testing superhero on with the Sauce Labs bolt T-shirt. From American Apparel, 100% ringspun combed cotton, heather gray with red bolt.'
        ]

        all_price_item_correct = page.locator('.inventory_item_price').all_inner_texts()
        assert all_price_item_correct == [
            '$29.99',
            '$9.99',
            '$15.99'
        ]

        #проверка наличия элементов на странице
        expect(page.locator('.cart_item')).to_have_count(3)

        #проверка, что суммы считаются корректно
        #достаём сумму всех товаров
        item_total = 0
        for i in all_price_item_correct:
            float_price = float(i.replace('$',''))
            item_total += float_price
        #достаём сумму таксы
        tax = page.locator('.summary_tax_label').inner_text()
        new_tax = float(tax.replace('Tax: $',''))
        #достаём общую сумму
        total_price = page.locator('.summary_total_label').inner_text()
        total_price_new = float(total_price.replace('Total: $', ''))
        #сравниваем, что итоговая сумма равна таксе и сумме товаров
        assert total_price_new == new_tax + item_total





















