
from ProjectCode.Domain.Objects.Cart import Cart
from abc import ABC, abstractmethod


class User(ABC):
    def __init__(self, username, cart_id):
        self.username = username
        self.cart = Cart(cart_id, username)

    def get_cart(self):
        return self.cart
        pass

    def add_to_cart(self, storename, productID, product, quantity):
        self.cart.add_Product(storename, productID, product, quantity)
        pass

    def purchase(self):
        # purchasing process
        pass

    def get_Basket(self, storename):
        return self.cart.get_Basket(storename)

    def removeFromBasket(self, storename, productID):
        self.cart.removeFromBasket(storename, productID)

    def checkProductExistance(self, storename, productID):
        return self.cart.checkProductExistance(storename, productID)

    def edit_Product_Quantity(self, storename, productID, quantity):
        self.cart.edit_Product_Quantity(storename, productID, quantity)
