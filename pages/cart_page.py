from playwright.sync_api import Page


class CartPage:

    def __init__(self, page: Page):
        self.page = page

        self.add_item_one = page.locator('#add-to-cart-sauce-labs-backpack') #добавление первого товара
        self.add_item_two = page.locator('#add-to-cart-sauce-labs-bike-light')  # добавление первого товара
        self.add_item_three = page.locator('#add-to-cart-sauce-labs-bolt-t-shirt')  # добавление первого товара

        self.go_back_catalog = page.locator('#continue-shopping') #переход в каталог обратно из корзины

        self.button_remove_item_one = page.locator('#remove-sauce-labs-backpack') #удаление первого товара из корзины
        self.button_remove_item_two = page.locator('#remove-sauce-labs-bike-light')  # удаление второго товара из корзины
        self.button_remove_item_three = page.locator('#remove-sauce-labs-bolt-t-shirt')  # удаление третьего товара из корзины

    def add_sauce_labs_backpack(self):
        self.add_item_one.click()

    def add_sauce_labs_bike_light(self):
        self.add_item_two.click()

    def add_sauce_labs_bolt_t_shirt(self):
        self.add_item_three.click()

    def remove_sauce_labs_backpack(self):
        self.button_remove_item_one.click()

    def remove_sauce_labs_bike_light(self):
        self.button_remove_item_two.click()

    def remove_sauce_labs_bolt_t_shirt(self):
        self.button_remove_item_three.click()

    def cart_to_catalog(self):
        self.go_back_catalog.click()



