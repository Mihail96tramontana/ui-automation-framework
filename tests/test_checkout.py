from playwright.sync_api import expect, Page
from config import BASE_URL, NAME, LAST_NAME, POSTAL_CODE
from pages.checkout_page import CheckoutPage
import pytest


class TestCheckout:

    #переходим на страницу заполнения формы
    def test_proceed_to_checkout(self, page: Page, fixture_login_add_item_checkout):

        #фикстура с авторизацией/добавлением 1 товара в корзину/переходом к заполнению формы при покупке
        page=fixture_login_add_item_checkout

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


    #заполняем форму на странице Checkout: Your Information и пробуем вернуться в корзину обратно
    @pytest.mark.parametrize('first_name, last_name, postal_code, expected_text_error', [
        ('','','','Error: First Name is required'),
        ('','test','test','Error: First Name is required'),
        ('test','','test','Error: Last Name is required'),
        ('test','test','','Error: Postal Code is required')
    ])
    def test_empty_fields(self, page: Page, first_name, last_name, postal_code, expected_text_error, fixture_login_add_item_checkout):

        #создаём объект Page Object
        checkout_page = CheckoutPage(page)

        #фикстура с авторизацией/добавлением 1 товара в корзину/переходом к заполнению формы при покупке
        page = fixture_login_add_item_checkout

        #заполнение формы
        checkout_page.your_information_form(first_name, last_name, postal_code)

        #переход с формы к итоговой сумме оплаты
        checkout_page.your_information_form_to_total_price()

        #проверки
        #проверяем, что ошибка отображается корректно
        expect(page.locator('h3[data-test="error"]')).to_be_visible()
        expect(page.locator('h3[data-test="error"]')).to_have_text(expected_text_error)
        #проверяем, что кнопка возвращения в корзину отображается
        expect(page.locator('#cancel')).to_be_visible()

        #возвращение назад в корзину из процесса заполнения формы
        checkout_page.button_cancel_your_information()

        #проверяем, что вернулись именно в корзину
        expect(page).to_have_url(f'{BASE_URL}cart.html')


    #переходим со страницы заполнения формы на стр с итоговой суммой покупки и проверяем её, после чего возвращаемся в каталог (перехода в корзину нет)
    def test_checkout_your_information_to_overview(self, page: Page, fixture_login_add_three_item_checkout):

        checkout_page = CheckoutPage(page)

        #фикстура с авторизацией/добавлением 3 товаров в корзину/переходом к заполнению формы при покупке
        page = fixture_login_add_three_item_checkout

        #заполнение формы
        checkout_page.your_information_form(NAME, LAST_NAME, POSTAL_CODE)

        #переход с формы к итоговой сумме оплаты
        checkout_page.your_information_form_to_total_price()

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
        expect(page.locator('#cancel')).to_be_visible()
        expect(page.locator('#finish')).to_be_visible()



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



        #клик по кнопке возвращения к каталогу
        button_overview_to_catalog = page.locator('#cancel')
        button_overview_to_catalog.click()

        expect(page).to_have_url(f'{BASE_URL}inventory.html')


    #переходим на финальную со стр итоговой суммы после прожатия на кнопку finish и возвращаемся в каталог обратно (перехода на стр с итоговой суммой нет)
    def test_checkout_overview_to_finish(self, page: Page, fixture_login_add_three_item_checkout):

        checkout_page = CheckoutPage(page)

        #фикстура с авторизацией/добавлением 3 товаров в корзину/переходом к заполнению формы при покупке
        page = fixture_login_add_three_item_checkout

        #заполнение формы
        checkout_page.your_information_form(NAME, LAST_NAME, POSTAL_CODE)

        #переход с формы к итоговой сумме оплаты
        checkout_page.your_information_form_to_total_price()

        #клик по кнопке finish
        checkout_page.button_finish_click()

        expect(page).to_have_url(f'{BASE_URL}checkout-complete.html')
        expect(page.locator('.complete-header')).to_be_visible()
        expect(page.locator('.complete-header')).to_have_text('Thank you for your order!')
        expect(page.locator('.complete-text')).to_be_visible()
        expect(page.locator('.complete-text')).to_have_text('Your order has been dispatched, and will arrive just as fast as the pony can get there!')
        expect(page.locator('#back-to-products')).to_be_visible()
        expect(page.locator('#generate-pdf-order')).to_be_visible()

        #возвращаемся в каталог обратно
        go_back_catalog = page.locator('#back-to-products')
        go_back_catalog.click()

        expect(page).to_have_url(f'{BASE_URL}inventory.html')

    def test_download_pdf(self, page: Page, fixture_login_add_three_item_checkout):

        checkout_page = CheckoutPage(page)

        #фикстура с авторизацией/добавлением 3 товаров в корзину/переходом к заполнению формы при покупке
        page = fixture_login_add_three_item_checkout

        #заполнение формы
        checkout_page.your_information_form(NAME, LAST_NAME, POSTAL_CODE)

        #переход с формы к итоговой сумме оплаты
        checkout_page.your_information_form_to_total_price()

        #клик по кнопке finish
        checkout_page.button_finish_click()

        #скачивание пдф-файла и проверка, что он имеет формат pdf
        with page.expect_download() as download_info:
            button_pdf = page.locator('#generate-pdf-order') #локатор оборачиваем в контекстный менеджер
            button_pdf.click()

        download = download_info.value
        assert '.pdf' in download.suggested_filename #проверяем через имя файла его формат






























