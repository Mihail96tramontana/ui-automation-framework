from playwright.sync_api import expect, Page
from config import BASE_URL, PASSWORD, STANDARD_USER
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage

class TestCart:
    def test_add_item_in_cart(self, page: Page):

        #создаём объекты Page Object
        login_page = LoginPage(page)
        cart_page = CartPage(page)
        inventory_page = InventoryPage(page)

        login_page.open() #переходим на сайт
        login_page.login(STANDARD_USER, PASSWORD) #авторизуемся

        cart_page.add_sauce_labs_backpack() #добавляем в корзину первый объект

        inventory_page.catalog_to_cart() #переходим в корзину

        expect(page).to_have_url(f'{BASE_URL}cart.html')
        expect(page.locator('.shopping_cart_badge')).to_have_text('1')
        expect(page.locator('#item_4_title_link')).to_have_text('Sauce Labs Backpack')
        expect(page.locator('#remove-sauce-labs-backpack')).to_have_text('Remove')
        description_text = page.locator('.inventory_item_desc').nth(0)
        expect(description_text).to_have_text('carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.')
        price_text = page.locator('.inventory_item_price').nth(0)
        expect(price_text).to_have_text('$29.99')
        expect(page.locator('.cart_quantity')).to_have_count(1)

        cart_page.cart_to_catalog() #переходим обратно в каталог

        expect(page).to_have_url(f'{BASE_URL}inventory.html') #проверяем, что при переходе в каталог попадаем именно в каталог

    def test_remove_item_from_cart(self, page: Page):

        #создаём объекты Page Object
        login_page = LoginPage(page)
        cart_page = CartPage(page)
        inventory_page = InventoryPage(page)

        login_page.open()  #переходим на сайт
        login_page.login(STANDARD_USER, PASSWORD)  #авторизуемся

        cart_page.add_sauce_labs_backpack() #добавляем в корзину первый объект

        inventory_page.catalog_to_cart() #переходим в корзину

        cart_page.remove_sauce_labs_backpack() #удаляем первый товар из корзины

        expect(page.locator('.cart_item')).to_be_hidden()
        expect(page.locator('.shopping_cart_badge')).to_be_hidden()

    def test_add_remove_add_item_to_cart(self, page: Page):

        #создаём объекты Page Object
        login_page = LoginPage(page)
        cart_page = CartPage(page)
        inventory_page = InventoryPage(page)

        login_page.open()  #переходим на сайт
        login_page.login(STANDARD_USER, PASSWORD)  #авторизуемся

        cart_page.add_sauce_labs_backpack() #добавляем в корзину первый объект

        inventory_page.catalog_to_cart() #переходим в корзину

        cart_page.remove_sauce_labs_backpack() #удаляем первый товар из корзины

        cart_page.cart_to_catalog() #переходим обратно в каталог

        cart_page.add_sauce_labs_backpack() #добавляем в корзину первый объект

        inventory_page.catalog_to_cart() #переходим в корзину

        expect(page.locator('.shopping_cart_badge')).to_have_text('1')
        expect(page.locator('#item_4_title_link')).to_have_text('Sauce Labs Backpack')
        expect(page.locator('#remove-sauce-labs-backpack')).to_have_text('Remove')
        description_text = page.locator('.inventory_item_desc').nth(0)
        expect(description_text).to_have_text(
            'carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.')
        price_text = page.locator('.inventory_item_price').nth(0)
        expect(price_text).to_have_text('$29.99')

    def test_add_multiple_to_cart(self, page: Page):

        #создаём объекты Page Object
        login_page = LoginPage(page)
        cart_page = CartPage(page)
        inventory_page = InventoryPage(page)

        login_page.open()  #переходим на сайт
        login_page.login(STANDARD_USER, PASSWORD)  #авторизуемся

        cart_page.add_sauce_labs_backpack() #добавляем в корзину первый объект

        cart_page.add_sauce_labs_bike_light() #добавляем в корзину второй объект

        cart_page.add_sauce_labs_bolt_t_shirt() #добавляем в корзину третий объект

        inventory_page.catalog_to_cart() #переходим в корзину

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





















