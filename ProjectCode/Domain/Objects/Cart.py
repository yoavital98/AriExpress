import string

from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.Objects.Basket import Basket


class Cart:
    def __init__(self, username):
        self.username = username
        self.baskets = TypedDict(str, Basket)

    def add_basket(self, store, basket):
        self.baskets[store.name] = basket

    def remove_basket(self, store):
        del self.baskets[store.name]

    def get_username(self):
        return self.username

    def set_username(self, username):
        self.username = username

    def get_baskets(self):
        return self.baskets

    def set_baskets(self, baskets):
        self.baskets = baskets
