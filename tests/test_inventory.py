from playwright.sync_api import expect, Page
from config import BASE_URL, PASSWORD, STANDARD_USER, LOCKED_USER

class TestInventory:
    def test_product_display(self, page: Page):

        # переход на страницу
        page.goto(BASE_URL)

        # ввод логина
        input_username = page.locator('#user-name')
        input_username.fill(STANDARD_USER)

        # ввод пароля
        input_password = page.locator('#password')
        input_password.fill(PASSWORD)

        # отправка формы/авторизация
        button_login = page.locator('#login-button')
        button_login.click()

        expect(page).to_have_url(f'{BASE_URL}inventory.html')
        expect(page.locator('.title')).to_have_text('Products')
        expect(page.locator('.inventory_item')).to_have_count(6)

        page.wait_for_timeout(3000)

    def test_adding_to_cart_single_item(self, page: Page):

        #переход на страницу
        page.goto(BASE_URL)

        #ввод логина
        input_username = page.locator('#user-name')
        input_username.fill(STANDARD_USER)

        #ввод пароля
        input_password = page.locator('#password')
        input_password.fill(PASSWORD)

        #отправка формы/авторизация
        button_login = page.locator('#login-button')
        button_login.click()

        #добавляем товар в корзину
        add_to_cart = page.locator('#add-to-cart-sauce-labs-backpack')
        add_to_cart.click()

        #проверки
        expect(page).to_have_url(f'{BASE_URL}inventory.html') #проверка URL
        expect(page.locator('#remove-sauce-labs-backpack')).to_have_text('Remove') #проверка, что кнопка Add to cart поменялась на Remove
        expect(page.locator('.shopping_cart_badge')).to_have_text('1') #проверка, что каунтер товаров в корзине равен 1

        #переходим в корзину
        item_in_cart = page.locator('.shopping_cart_link')
        item_in_cart.click()

        #проверяем наличие добавленного товара в корзине
        expect(page.locator('.inventory_item_name')).to_have_text('Sauce Labs Backpack')


    def test_adding_to_cart_multiple_items(self, page: Page):

        #переход на страницу
        page.goto(BASE_URL)

        #ввод логина
        input_username = page.locator('#user-name')
        input_username.fill(STANDARD_USER)

        #ввод пароля
        input_password = page.locator('#password')
        input_password.fill(PASSWORD)

        #отправка формы/авторизация
        button_login = page.locator('#login-button')
        button_login.click()


        #добавляем товары в корзину

        add_first_product = page.locator('#add-to-cart-sauce-labs-backpack')
        add_first_product.click()
        #проверяем, что каунтер корзины - 1
        expect(page.locator('.shopping_cart_badge')).to_have_text('1')
        #проверяем, что кнопка изменилась с Add to cart на Remove
        expect(page.locator('#remove-sauce-labs-backpack')).to_have_text('Remove')
        #переходим в корзину
        item_first_in_cart = page.locator('.shopping_cart_link')
        item_first_in_cart.click()
        #проверяем, что товар добавлен
        expect(page.locator('#item_4_title_link .inventory_item_name')).to_have_text('Sauce Labs Backpack')
        #возвращаемся на страницу списка товаров
        page.go_back()

        add_second_product = page.locator('#add-to-cart-sauce-labs-fleece-jacket')
        add_second_product.click()
        #проверяем, что каунтер корзины - 2
        expect(page.locator('.shopping_cart_badge')).to_have_text('2')
        #проверяем, что кнопка изменилась с Add to cart на Remove
        expect(page.locator('#remove-sauce-labs-fleece-jacket')).to_have_text('Remove')
        #переходим в корзину
        item_first_in_cart = page.locator('.shopping_cart_link')
        item_first_in_cart.click()
        #проверяем, что товар добавлен
        expect(page.locator('#item_5_title_link .inventory_item_name')).to_have_text('Sauce Labs Fleece Jacket')
        #возвращаемся на страницу списка товаров
        page.go_back()

        add_third_product = page.locator('#add-to-cart-sauce-labs-onesie')
        add_third_product.click()
        #проверяем, что каунтер корзины - 3
        expect(page.locator('.shopping_cart_badge')).to_have_text('3')
        #проверяем, что кнопка изменилась с Add to cart на Remove
        expect(page.locator('#remove-sauce-labs-onesie')).to_have_text('Remove')
        #переходим в корзину
        item_first_in_cart = page.locator('.shopping_cart_link')
        item_first_in_cart.click()
        #проверяем, что товар добавлен
        expect(page.locator('#item_2_title_link .inventory_item_name')).to_have_text('Sauce Labs Onesie')


        #итоговые проверки добавленных товаров в корзину

        #проверяем, что всего 3 карточки товаров
        expect(page.locator('.cart_item')).to_have_count(3)

        #проверяем, что цены соответствуют добавленным товарам
        index_price_one = page.locator('.inventory_item_price').nth(0)
        expect(index_price_one).to_have_text('$29.99')

        index_price_two = page.locator('.inventory_item_price').nth(1)
        expect(index_price_two).to_have_text('$49.99')

        index_price_three = page.locator('.inventory_item_price').nth(2)
        expect(index_price_three).to_have_text('$7.99')

        #проверяем, что у всех товаров есть кнопки удаления из корзины - Remove
        expect(page.locator('#remove-sauce-labs-backpack')).to_have_text('Remove')
        expect(page.locator('#remove-sauce-labs-fleece-jacket')).to_have_text('Remove')
        expect(page.locator('#remove-sauce-labs-onesie')).to_have_text('Remove')

        #проверяем, что добавлены нужные товары
        index_name_item_one = page.locator('.inventory_item_name').nth(0)
        expect(index_name_item_one).to_have_text('Sauce Labs Backpack')

        index_name_item_two = page.locator('.inventory_item_name').nth(1)
        expect(index_name_item_two).to_have_text('Sauce Labs Fleece Jacket')

        index_name_item_three = page.locator('.inventory_item_name').nth(2)
        expect(index_name_item_three).to_have_text('Sauce Labs Onesie')














