from playwright.sync_api import Page


class CheckoutPage:

    def __init__(self, page: Page):
        self.page = page

        #локаторы для заполнения формы при покупке товара
        self.input_first_name = page.locator('#first-name')
        self.input_last_name = page.locator('#last-name')
        self.input_postal_code = page.locator('#postal-code')
        self.button_continue = page.locator('#continue')


    def your_information_form(self, first_name, last_name, postal_code):

        self.input_first_name.fill(first_name)
        self.input_last_name.fill(last_name)
        self.input_postal_code.fill(postal_code)
        self.button_continue.click()