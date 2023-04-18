import string

from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.Objects.Basket import *


class Cart:
    def __init__(self, cartID, username):
        self.cartID = cartID
        self.username = username
        self.baskets = TypedDict(string, Basket)


    def get_Basket(self,storename):
        if self.baskets.keys().__contains__(storename):
            return self.baskets[storename]
        else:
            raise SystemError("Basket does not exists")

    def add_Product(self, storename, productID, product, quantity):
        basket = self.baskets[storename]
        basket.add_Product(productID, product, quantity)
    def get_username(self):
        return self.username

    def set_username(self, username):
        self.username = username

    def get_baskets(self):
        return self.baskets

    def set_baskets(self, baskets):
        self.baskets = baskets
