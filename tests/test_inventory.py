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
        add_to_cart_one = page.locator('#add-to-cart-sauce-labs-backpack')
        add_to_cart_one.click()

        #проверки
        expect(page).to_have_url(f'{BASE_URL}inventory.html') #проверка URL
        expect(page.locator('#remove-sauce-labs-backpack')).to_have_text('Remove') #проверка, что кнопка Add to cart поменялась на Remove
        expect(page.locator('.shopping_cart_badge')).to_have_text('1') #проверка, что каунтер товаров в корзине равен 1

        #добавляем второй товар в корзину
        add_to_cart_two = page.locator('#add-to-cart-sauce-labs-fleece-jacket')
        add_to_cart_two.click()

        #проверяем, что каунтер увеличился до 2
        expect(page.locator('.shopping_cart_badge')).to_have_text('2')



    def test_removing_item_from_cart(self, page: Page):

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
        add_to_cart_one = page.locator('#add-to-cart-sauce-labs-backpack')
        add_to_cart_one.click()

        #добавляем второй товар в корзину
        add_to_cart_two = page.locator('#add-to-cart-sauce-labs-fleece-jacket')
        add_to_cart_two.click()

        #удаляем первый товар из корзины
        delete_item_one_from_cart = page.locator('#remove-sauce-labs-backpack')
        delete_item_one_from_cart.click()
        #проверяем, что каунтер уменьшился на 1
        expect(page.locator('.shopping_cart_badge')).to_have_text('1')

        #удаляем второй товар из корзины
        delete_item_two_from_cart = page.locator('#remove-sauce-labs-fleece-jacket')
        delete_item_two_from_cart.click()
        #проверяем, что каунтер исчез
        expect(page.locator('.shopping_cart_badge')).to_be_hidden()



    def test_item_page(self, page: Page):

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

        #проваливаемся в карточку товара
        open_item = page.locator('img[data-test="inventory-item-sauce-labs-backpack-img"]')
        open_item.click()

        #общие проверки страницы товара
        expect(page).to_have_url(f'{BASE_URL}inventory-item.html?id=4')
        expect(page.locator('.inventory_details_name.large_size')).to_have_text('Sauce Labs Backpack')
        expect(page.locator('.inventory_details_price')).to_have_text('$29.99')
        expect(page.locator('.inventory_details_desc.large_size')).to_have_text('carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.')
        expect(page.locator('.btn.btn_primary.btn_small.btn_inventory')).to_be_visible()

        #добавляем товар в корзину
        add_to_cart = page.locator('#add-to-cart')
        add_to_cart.click()
        #проверяем, что каунтер стал 1
        expect(page.locator('.shopping_cart_badge')).to_have_text('1')

        #удаляем товар из корзины
        remove_item_from_cart = page.locator('#remove')
        remove_item_from_cart.click()
        #проверяем отсутствие каунтера у корзины
        expect(page.locator('.shopping_cart_badge')).to_be_hidden()

        #возвращаемся в каталог
        go_back_to_catalog = page.locator('#back-to-products')
        go_back_to_catalog.click()
        #проверяем, что успешно вернулись назад
        expect(page).to_have_url(f'{BASE_URL}inventory.html')



    def test_sorting(self, page: Page):

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




























