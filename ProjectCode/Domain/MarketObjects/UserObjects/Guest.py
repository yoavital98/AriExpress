from ProjectCode.Domain.MarketObjects.Cart import Cart
from ProjectCode.Domain.MarketObjects.User import User


class Guest(User):
    def __init__(self, entrance_id):
        super().__init__(entrance_id)

    def get_cart(self):
        return super().get_cart()

    def add_to_cart(self,username, storename, productID, product, quantity):
        return super().add_to_cart(username, storename, productID, product, quantity)

    def get_Basket(self, storename):
        return super().get_Basket(storename)

    def removeFromBasket(self, storename, productID):
        super().removeFromBasket(storename, productID)

    def get_entrance_id(self):
        return super().get_entrance_id()

    def setCart(self, cart: Cart):
        super().setCart(cart)

