from playwright.sync_api import Page


class InventoryPage:

    def __init__(self, page: Page):
        self.page = page

        self.open_cart = page.locator('.shopping_cart_link') #переход в корзину

    def catalog_to_cart(self):
        self.open_cart.click()
