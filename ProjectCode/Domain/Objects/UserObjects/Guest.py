from ProjectCode.Domain.Objects.Cart import Cart
from abc import ABC, abstractmethod

from ProjectCode.Domain.Objects.User import User


class Guest(User):
    def __init__(self, entrance_id):
        self.entrance_id = entrance_id
        self.cart = Cart(self.entrance_id)

    def get_cart(self):
        # Return the user's shopping cart
        return self.cart

    def add_to_cart(self, storename, item):

        pass

    def purchase(self):
        # purchasing process
        pass
