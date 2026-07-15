from playwright.sync_api import Page


class CheckoutPage:

    def __init__(self, page: Page):
        self.page = page

        #локаторы для заполнения формы при покупке товара
        self.input_first_name = page.locator('#first-name')
        self.input_last_name = page.locator('#last-name')
        self.input_postal_code = page.locator('#postal-code')
        #локатор для перехода на стр с итоговой оплатой после заполнения формы
        self.button_continue = page.locator('#continue')
        #кнопка finish на втором этапе оформления заказа
        self.button_finish = page.locator('#finish')
        #возвращение назад в корзину из формы
        self.button_your_information_to_cart = page.locator('#cancel')
        


    def your_information_form(self, first_name, last_name, postal_code):

        self.input_first_name.fill(first_name)
        self.input_last_name.fill(last_name)
        self.input_postal_code.fill(postal_code)

    def your_information_form_to_total_price(self,):
        self.button_continue.click()

    def button_finish_click(self):
        self.button_finish.click()

    def button_cancel_your_information(self):
        self.button_your_information_to_cart.click()

