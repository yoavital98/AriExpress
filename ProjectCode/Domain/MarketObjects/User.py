from abc import ABC

from ProjectCode.Domain.MarketObjects.Cart import Cart


class User(ABC):
    def __init__(self, username):
        self.username = username
        self.cart = Cart(username)

    def get_cart(self):
        return self.cart

    def add_to_cart(self,username, storename, productID, product, quantity):
        self.cart.add_Product(username, storename, productID, product, quantity)


    def get_Basket(self, storename):
        return self.cart.get_Basket(storename)

    def removeFromBasket(self, storename, productID):
        self.cart.removeFromBasket(storename, productID)

    def checkProductExistance(self, storename, productID):
        return self.cart.checkProductExistance(storename, productID)

    def edit_Product_Quantity(self, storename, productID, quantity):
        self.cart.edit_Product_Quantity(storename, productID, quantity)

    def get_username(self):
        return self.username
