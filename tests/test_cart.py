from playwright.sync_api import expect, Page
from pytest_playwright.pytest_playwright import page

from config import BASE_URL, PASSWORD, STANDARD_USER
from pages.login_page import LoginPage

class TestCart:
    def test_add_item_in_cart(self, page: Page):

        login_page = LoginPage(page)
        login_page.open() #переходим на сайт
        login_page.login(STANDARD_USER, PASSWORD) #авторизуемся

        add_item = page.locator('#add-to-cart-sauce-labs-backpack')
        add_item.click()

        open_cart = page.locator('.shopping_cart_link')
        open_cart.click()

        expect(page).to_have_url(f'{BASE_URL}cart.html')
        expect(page.locator('.shopping_cart_badge')).to_have_text('1')
        expect(page.locator('#item_4_title_link')).to_have_text('Sauce Labs Backpack')
        expect(page.locator('#remove-sauce-labs-backpack')).to_have_text('Remove')
        description_text = page.locator('.inventory_item_desc').nth(0)
        expect(description_text).to_have_text('carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.')
        price_text = page.locator('.inventory_item_price').nth(0)
        expect(price_text).to_have_text('$29.99')
        expect(page.locator('.cart_quantity')).to_have_count(1)

        button_catalog = page.locator('#continue-shopping')
        button_catalog.click()

    def test_remove_item_from_cart(self, page: Page):

        login_page = LoginPage(page)
        login_page.open()  #переходим на сайт
        login_page.login(STANDARD_USER, PASSWORD)  #авторизуемся

        add_item = page.locator('#add-to-cart-sauce-labs-backpack')
        add_item.click()

        open_cart = page.locator('.shopping_cart_link')
        open_cart.click()

        #удаление товара из корзины
        button_remove = page.locator('#remove-sauce-labs-backpack')
        button_remove.click()

        expect(page.locator('.cart_item')).to_be_hidden()
        expect(page.locator('.shopping_cart_badge')).to_be_hidden()

    def test_add_remove_add_item_to_cart(self, page: Page):

        login_page = LoginPage(page)
        login_page.open()  #переходим на сайт
        login_page.login(STANDARD_USER, PASSWORD)  #авторизуемся

        add_item = page.locator('#add-to-cart-sauce-labs-backpack')
        add_item.click()

        open_cart = page.locator('.shopping_cart_link')
        open_cart.click()

        #удаление товара из корзины
        button_remove = page.locator('#remove-sauce-labs-backpack')
        button_remove.click()

        #возвращаемся в каталог
        button_catalog = page.locator('#continue-shopping')
        button_catalog.click()

        #добавление товара в корзину
        add_item = page.locator('#add-to-cart-sauce-labs-backpack')
        add_item.click()

        #переход в корзину
        open_cart = page.locator('.shopping_cart_link')
        open_cart.click()

        expect(page.locator('.shopping_cart_badge')).to_have_text('1')
        expect(page.locator('#item_4_title_link')).to_have_text('Sauce Labs Backpack')
        expect(page.locator('#remove-sauce-labs-backpack')).to_have_text('Remove')
        description_text = page.locator('.inventory_item_desc').nth(0)
        expect(description_text).to_have_text(
            'carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.')
        price_text = page.locator('.inventory_item_price').nth(0)
        expect(price_text).to_have_text('$29.99')

    def test_add_multiple_to_cart(self, page: Page):

        login_page = LoginPage(page)
        login_page.open()  #переходим на сайт
        login_page.login(STANDARD_USER, PASSWORD)  #авторизуемся

        #добавляем первый товар в корзину
        add_item_one = page.locator('#add-to-cart-sauce-labs-backpack')
        add_item_one.click()

        #добавляем второй товар в корзину
        add_item_two = page.locator('#add-to-cart-sauce-labs-bike-light')
        add_item_two.click()

        #добавляем третий товар в корзину
        add_item_three = page.locator('#add-to-cart-sauce-labs-bolt-t-shirt')
        add_item_three.click()

        open_cart = page.locator('.shopping_cart_link')
        open_cart.click()

        expect(page.locator('.shopping_cart_badge')).to_have_text('3')
        expect(page.locator('.cart_item')).to_have_count(3)
        #проверка, что все наименования товаров есть на странице
        cart_names = page.locator('.inventory_item_name').all_inner_texts() #превращаем все объекты с этим элементов в строчный список
        assert cart_names == [
            'Sauce Labs Backpack',
            'Sauce Labs Bike Light',
            'Sauce Labs Bolt T-Shirt'
        ]
        #проверка, что все цены товаров есть на странице
        cart_price = page.locator('.inventory_item_price').all_inner_texts() #превращаем все объекты с этим элементов в строчный список
        assert cart_price == [
            '$29.99',
            '$9.99',
            '$15.99',
        ]
        #проверка, что все описания товаров есть на странице
        cart_desc = page.locator('.inventory_item_desc').all_inner_texts() #превращаем все объекты с этим элементов в строчный список
        assert cart_desc == [
            'carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.',
            "A red light isn't the desired state in testing but it sure helps when riding your bike at night. Water-resistant with 3 lighting modes, 1 AAA battery included.",
            'Get your testing superhero on with the Sauce Labs bolt T-shirt. From American Apparel, 100% ringspun combed cotton, heather gray with red bolt.',
        ]

        expect(page.locator('#remove-sauce-labs-backpack')).to_have_text('Remove')
        expect(page.locator('#remove-sauce-labs-bike-light')).to_have_text('Remove')
        expect(page.locator('#remove-sauce-labs-bolt-t-shirt')).to_have_text('Remove')





















