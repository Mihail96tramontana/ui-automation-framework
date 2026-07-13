from playwright.sync_api import Page
from config import BASE_URL


class LoginPage:

    def __init__(self, page: Page):
        self.page = page

        #в метод __init__ переносим все использованные локаторы из файла test_login.py (локаторы всегда выносятся в __init__)
        self.input_username = page.locator('#user-name')
        self.input_password = page.locator('#password')
        self.button_login = page.locator('#login-button')


    #сюда выносим все действия со страницей браузера
    def open(self):
        self.page.goto(BASE_URL)

    def login(self, username, password):
        self.input_username.fill(username)
        self.input_password.fill(password)
        self.button_login.click()


