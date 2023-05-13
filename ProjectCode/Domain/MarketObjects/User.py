from abc import ABC

from ProjectCode.Domain.MarketObjects.Cart import Cart


class User(ABC):
    def __init__(self, entrance_id):
        self.entrance_id = entrance_id
        self.cart = Cart(entrance_id)

    def get_cart(self):
        return self.cart


    def add_to_cart(self, username, store, productID, product, quantity):
        return self.cart.add_Product(username, store, productID, product, quantity)

    def get_Basket(self, storename):
        return self.cart.get_Basket(storename)

    def removeFromBasket(self, storename, productID):
        answer: bool = self.cart.removeFromBasket(storename, productID)
        return answer

    def checkProductExistance(self, storename, productID):
        return self.cart.checkProductExistance(storename, productID)

    def edit_Product_Quantity(self, storename, productID, quantity):
        return self.cart.edit_Product_Quantity(storename, productID, quantity)

    def get_entrance_id(self):
        return self.entrance_id
