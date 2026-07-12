import pytest
from playwright.sync_api import expect, Page
from config import BASE_URL, PASSWORD, STANDARD_USER, LOCKED_USER


class TestLogin:
    def test_successful_login(self, page: Page):

            #переход на страницу
            page.goto(BASE_URL)

            #ввод логина
            input_username = page.locator('#user-name')
            input_username.fill(STANDARD_USER)

            #ввод пароля
            input_password = page.locator('#password')
            input_password.fill(PASSWORD)

            #отправка формы
            button_login = page.locator('#login-button')
            button_login.click()

            #проверки после авторизации
            expect(page).to_have_url(f'{BASE_URL}inventory.html') #проверка URL
            expect(page).to_have_title('Swag Labs') #проверка title страницы
            expect(page.locator('.title')).to_have_text('Products') #проверка наличия заголовка внутри страницы
            expect(page.locator('.inventory_item')).to_have_count(6) #проверка кол-ва элементов на странице


    def test_locked_out_user_login(self, page: Page):

            # переход на страницу
            page.goto(BASE_URL)

            # ввод логина
            input_username = page.locator('#user-name')
            input_username.fill(LOCKED_USER)

            # ввод пароля
            input_password = page.locator('#password')
            input_password.fill(PASSWORD)

            # отправка формы
            button_login = page.locator('#login-button')
            button_login.click()

            expect(page).to_have_url(BASE_URL)
            expect(page.locator('h3[data-test="error"]')).to_have_text('Epic sadface: Sorry, this user has been locked out.')


    @pytest.mark.parametrize('username, password, error_text', [
            (STANDARD_USER, 'invalid_password', 'Epic sadface: Username and password do not match any user in this service'),
            ('invalid_username', PASSWORD, 'Epic sadface: Username and password do not match any user in this service'),
            ('', PASSWORD, 'Epic sadface: Username is required'),
            (STANDARD_USER, '', 'Epic sadface: Password is required'),
            ('<script>alert(1)</script>', '<script>alert(1)</script>', 'Epic sadface: Username and password do not match any user in this service'),
            ('<b>test</b>', '<b>test</b>', 'Epic sadface: Username and password do not match any user in this service'),
            ("' OR '1'='1", PASSWORD, 'Epic sadface: Username and password do not match any user in this service'),
            ('abc'*500, PASSWORD, 'Epic sadface: Username and password do not match any user in this service'),
            ('😀🎉', PASSWORD, 'Epic sadface: Username and password do not match any user in this service'),
            ('кириллица', PASSWORD, 'Epic sadface: Username and password do not match any user in this service'),
            ('こんにちは', PASSWORD, 'Epic sadface: Username and password do not match any user in this service'),
            ('!@#$%^&*()_+', PASSWORD, 'Epic sadface: Username and password do not match any user in this service')
    ])
    def test_invalid_login(self, page: Page, username, password, error_text):

            # переход на страницу
            page.goto(BASE_URL)

            # ввод логина
            input_username = page.locator('#user-name')
            input_username.fill(username)

            # ввод пароля
            input_password = page.locator('#password')
            input_password.fill(password)

            # отправка формы
            button_login = page.locator('#login-button')
            button_login.click()

            expect(page).to_have_url(BASE_URL)
            expect(page.locator('h3[data-test="error"]')).to_have_text(error_text)














