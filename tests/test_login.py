import pytest
from playwright.sync_api import expect, Page


class TestLogin:
    def test_successful_login(self, page: Page):

            #переход на страницу
            page.goto('https://www.saucedemo.com/')

            #ввод логина
            input_username = page.locator('#user-name')
            input_username.fill('standard_user')

            #ввод пароля
            input_password = page.locator('#password')
            input_password.fill('secret_sauce')

            #отправка формы
            button_login = page.locator('#login-button')
            button_login.click()

            #проверки после авторизации
            expect(page).to_have_url('https://www.saucedemo.com/inventory.html') #проверка URL
            expect(page).to_have_title('Swag Labs') #проверка title страницы
            expect(page.locator('.title')).to_have_text('Products') #проверка наличия заголовка внутри страницы
            expect(page.locator('.inventory_item')).to_have_count(6) #проверка кол-ва элементов на странице


    def test_locked_out_user_login(self, page: Page):

            # переход на страницу
            page.goto('https://www.saucedemo.com/')

            # ввод логина
            input_username = page.locator('#user-name')
            input_username.fill('locked_out_user')

            # ввод пароля
            input_password = page.locator('#password')
            input_password.fill('secret_sauce')

            # отправка формы
            button_login = page.locator('#login-button')
            button_login.click()

            expect(page).to_have_url('https://www.saucedemo.com/')
            expect(page.locator('h3[data-test="error"]')).to_have_text('Epic sadface: Sorry, this user has been locked out.')


    @pytest.mark.parametrize('username, password, error_text', [
            ('standard_user', 'invalid_password', 'Epic sadface: Username and password do not match any user in this service'),
            ('invalid_username', 'secret_sauce', 'Epic sadface: Username and password do not match any user in this service'),
            ('', 'secret_sauce', 'Epic sadface: Username is required'),
            ('standard_user', '', 'Epic sadface: Password is required'),
            ('<script>alert(1)</script>', '<script>alert(1)</script>', 'Epic sadface: Username and password do not match any user in this service'),
            ('<b>test</b>', '<b>test</b>', 'Epic sadface: Username and password do not match any user in this service'),
            ("' OR '1'='1", 'secret_sauce', 'Epic sadface: Username and password do not match any user in this service'),
            ('abc'*500, 'secret_sauce', 'Epic sadface: Username and password do not match any user in this service'),
            ('😀🎉', 'secret_sauce', 'Epic sadface: Username and password do not match any user in this service'),
            ('кириллица', 'secret_sauce', 'Epic sadface: Username and password do not match any user in this service'),
            ('こんにちは', 'secret_sauce', 'Epic sadface: Username and password do not match any user in this service'),
            ('!@#$%^&*()_+', 'secret_sauce', 'Epic sadface: Username and password do not match any user in this service')
    ])
    def test_invalid_login(self, page: Page, username, password, error_text):

            # переход на страницу
            page.goto('https://www.saucedemo.com/')

            # ввод логина
            input_username = page.locator('#user-name')
            input_username.fill(username)

            # ввод пароля
            input_password = page.locator('#password')
            input_password.fill(password)

            # отправка формы
            button_login = page.locator('#login-button')
            button_login.click()

            expect(page).to_have_url('https://www.saucedemo.com/')
            expect(page.locator('h3[data-test="error"]')).to_have_text(error_text)

            page.wait_for_timeout(3000)














