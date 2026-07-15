import pytest
from playwright.sync_api import expect, Page
from config import BASE_URL, PASSWORD, STANDARD_USER, LOCKED_USER
from pages.login_page import LoginPage
import allure



@allure.feature('Авторизация')
class TestLogin:
    @allure.title('Успешная авторизация')
    @allure.description('Авторизация с валидными данными, в результате которой успешно авторизуемся и попадаем на страницу каталога товаров')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_login(self, page: Page):

            login_page = LoginPage(page)

            login_page.open() #переходим на сайт
            login_page.login(STANDARD_USER, PASSWORD) #авторизуемся

            #проверки после авторизации
            expect(page).to_have_url(f'{BASE_URL}inventory.html') #проверка URL
            expect(page).to_have_title('Swag Labs') #проверка title страницы
            expect(page.locator('.title')).to_have_text('Products') #проверка наличия заголовка внутри страницы
            expect(page.locator('.inventory_item')).to_have_count(6) #проверка кол-ва элементов на странице

    @allure.title('Авторизация заблокированным юзером')
    @allure.description('Авторизация с юзером, который является заблокированным и у которого не должно быть доступа к сайту')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_locked_out_user_login(self, page: Page):

            login_page = LoginPage(page)

            login_page.open()
            login_page.login(LOCKED_USER, PASSWORD)

            expect(page).to_have_url(BASE_URL)
            expect(page.locator('h3[data-test="error"]')).to_have_text('Epic sadface: Sorry, this user has been locked out.')

    @allure.title('Авторизация невалидными данными')
    @allure.description('Авторизация с некорректно заполненными полями, из-за чего юзер не должен попадать в приложение')
    @allure.severity(allure.severity_level.CRITICAL)
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

            login_page = LoginPage(page)

            login_page.open()
            login_page.login(username, password)

            expect(page).to_have_url(BASE_URL)
            expect(page.locator('h3[data-test="error"]')).to_have_text(error_text)














