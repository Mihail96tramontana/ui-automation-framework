from playwright.sync_api import expect, Page
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from config import BASE_URL, PASSWORD, STANDARD_USER

class TestInventory:
    def test_product_display(self, page: Page):

        login_page = LoginPage(page)
        login_page.open()  # переходим на сайт
        login_page.login(STANDARD_USER, PASSWORD)  # авторизуемся

        expect(page).to_have_url(f'{BASE_URL}inventory.html')
        expect(page.locator('.title')).to_have_text('Products')
        expect(page.locator('.inventory_item')).to_have_count(6)


    def test_adding_to_cart_single_item(self, page: Page):

        login_page = LoginPage(page)
        cart_page = CartPage(page)

        login_page.open()  # переходим на сайт
        login_page.login(STANDARD_USER, PASSWORD)  # авторизуемся

        cart_page.add_sauce_labs_backpack() #добавляем в корзину первый объект

        #проверки
        expect(page).to_have_url(f'{BASE_URL}inventory.html') #проверка URL
        expect(page.locator('#remove-sauce-labs-backpack')).to_have_text('Remove') #проверка, что кнопка Add to cart поменялась на Remove
        expect(page.locator('.shopping_cart_badge')).to_have_text('1') #проверка, что каунтер товаров в корзине равен 1

        cart_page.add_sauce_labs_bike_light() #добавляем в корзину второй объект

        #проверяем, что каунтер увеличился до 2
        expect(page.locator('.shopping_cart_badge')).to_have_text('2')


    def test_removing_item_from_cart(self, page: Page):

        login_page = LoginPage(page)
        cart_page = CartPage(page)

        login_page.open()  # переходим на сайт
        login_page.login(STANDARD_USER, PASSWORD)  # авторизуемся

        cart_page.add_sauce_labs_backpack() #добавляем в корзину первый объект

        cart_page.add_sauce_labs_bike_light() #добавляем в корзину второй объект

        cart_page.remove_sauce_labs_backpack() #удаляем первый товар из корзины
        #проверяем, что каунтер уменьшился на 1
        expect(page.locator('.shopping_cart_badge')).to_have_text('1')

        cart_page.remove_sauce_labs_bike_light() #удаляем второй товар из корзины
        #проверяем, что каунтер исчез
        expect(page.locator('.shopping_cart_badge')).to_be_hidden()


    def test_item_page(self, page: Page):

        login_page = LoginPage(page)
        cart_page = CartPage(page)

        login_page.open()  # переходим на сайт
        login_page.login(STANDARD_USER, PASSWORD)  # авторизуемся

        #проваливаемся в карточку товара
        open_item = page.locator('img[data-test="inventory-item-sauce-labs-backpack-img"]')
        open_item.click()

        #общие проверки страницы товара
        expect(page).to_have_url(f'{BASE_URL}inventory-item.html?id=4')
        expect(page.locator('.inventory_details_name.large_size')).to_have_text('Sauce Labs Backpack')
        expect(page.locator('.inventory_details_price')).to_have_text('$29.99')
        expect(page.locator('.inventory_details_desc.large_size')).to_have_text('carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.')
        expect(page.locator('.btn.btn_primary.btn_small.btn_inventory')).to_be_visible()

        cart_page.add_sauce_labs_backpack() #добавляем в корзину первый объект
        #проверяем, что каунтер стал 1
        expect(page.locator('.shopping_cart_badge')).to_have_text('1')

        cart_page.add_sauce_labs_backpack()
        #проверяем отсутствие каунтера у корзины
        expect(page.locator('.shopping_cart_badge')).to_be_hidden()

        #возвращаемся в каталог
        go_back_to_catalog = page.locator('#back-to-products')
        go_back_to_catalog.click()
        #проверяем, что успешно вернулись назад
        expect(page).to_have_url(f'{BASE_URL}inventory.html')


    def test_sorting_low_to_high(self, page: Page):

        login_page = LoginPage(page)
        login_page.open()  # переходим на сайт
        login_page.login(STANDARD_USER, PASSWORD)  # авторизуемся

        #сортируем от меньшего к большему
        select_low_to_high = page.locator('.product_sort_container')
        select_low_to_high.select_option(label='Price (low to high)')

        #все элементы найденные по селектору превращаем в список
        low_to_high_sort = page.locator('.inventory_item_price').all()
        low_to_high_sort_list = []
        for i in low_to_high_sort:
            price_text = i.inner_text() #у каждого из элементов списка вычленяем текст - '$7.99'
            price_text = float(price_text.replace('$','')) #конвертируем текст в вещественное число отбрасывая знак доллара
            low_to_high_sort_list.append(price_text) #добавляем полученный результат в пустой список заранее созданный
        assert low_to_high_sort_list == sorted(low_to_high_sort_list) #сравниваем полученный результат с аналогичным списком по возрастанию

    def test_sorting_high_to_low(self, page: Page):

        login_page = LoginPage(page)
        login_page.open()  # переходим на сайт
        login_page.login(STANDARD_USER, PASSWORD)  # авторизуемся

        #сортируем от большего к меньшему
        select_high_to_low = page.locator('.product_sort_container')
        select_high_to_low.select_option(label='Price (high to low)')

        #все элементы найденные по селектору превращаем в список
        high_to_low_sort = page.locator('.inventory_item_price').all()
        high_to_low_sort_list = []
        for i in high_to_low_sort:
            price_text = i.inner_text() #у каждого из элементов списка вычленяем текст - '$7.99', например
            price_text = float(price_text.replace('$','')) #конвертируем текст в вещественное число отбрасывая знак доллара
            high_to_low_sort_list.append(price_text) #добавляем полученный результат в пустой список заранее созданный
        assert high_to_low_sort_list == sorted(high_to_low_sort_list, reverse=True) #сравниваем полученный результат со списком по убыванию

    def test_name_z_to_a_sorting(self, page: Page):

        login_page = LoginPage(page)
        login_page.open()  # переходим на сайт
        login_page.login(STANDARD_USER, PASSWORD)  # авторизуемся

        #сортируем от большего к меньшему
        select_name_z_to_a = page.locator('.product_sort_container')
        select_name_z_to_a.select_option(label='Name (Z to A)')

        select_name_z_to_a_sort = page.locator('.inventory_item_name').all()
        select_name_z_to_a_sort_list = []
        for i in select_name_z_to_a_sort:
            name_text = i.inner_text()
            select_name_z_to_a_sort_list.append(name_text)
        assert select_name_z_to_a_sort_list == sorted(select_name_z_to_a_sort_list, reverse=True)

    def test_name_a_to_z_sorting(self, page: Page):

        login_page = LoginPage(page)
        login_page.open()  # переходим на сайт
        login_page.login(STANDARD_USER, PASSWORD)  # авторизуемся

        #сортируем от большего к меньшему
        select_name_a_to_z = page.locator('.product_sort_container')
        select_name_a_to_z.select_option(label='Name (A to Z)')

        select_name_a_to_z_sort = page.locator('.inventory_item_name').all()
        select_name_a_to_z_sort_list = []
        for i in select_name_a_to_z_sort:
            name_text = i.inner_text()
            select_name_a_to_z_sort_list.append(name_text)
        assert select_name_a_to_z_sort_list == sorted(select_name_a_to_z_sort_list)
















































