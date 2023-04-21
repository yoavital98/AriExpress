import string

from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.Objects.Basket import *


class Cart:
    def __init__(self, cartID, username):  # TODO: remove cartID from the system
        self.cartID = cartID
        self.username = username
        self.baskets = TypedDict(string, Basket)

    def get_Baskets(self, storename):
        if self.baskets.keys().__contains__(storename):
            return self.baskets[storename]
        else:
            raise SystemError("Basket does not exists")

    def add_Product(self, storename, productID, product, quantity):
        basket: Basket= self.get_Baskets(storename)
        basket.add_Product(productID, product, quantity)

    def removeFromBasket(self, storename, productID):
        basket = self.baskets[storename]
        answer = basket.remove_Product(productID) # answer = true if item is successfully removed
        if basket.getBasketSize() == 0:
            self.baskets.__delitem__(storename)
        return answer

    def checkProductExistance(self, storename, productID):
        basket = self.baskets[storename]
        return basket.checkProductExistance(productID)

    def edit_Product_Quantity(self, storename, productID, quantity):
        basket: Basket = self.get_Baskets(storename)
        basket.edit_Product_Quantity(productID, quantity)

    def get_username(self):
        return self.username

    def set_username(self, username):
        self.username = username

    def get_baskets(self):
        return self.baskets

    def set_baskets(self, baskets):
        self.baskets = baskets

    def getProductsAsTuples(self, storename):
        basket: Basket = self.get_Baskets(storename)
        return basket.getProductsAsTuples()
