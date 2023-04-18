from ProjectCode.Domain.Objects.Cart import Cart
from abc import ABC, abstractmethod

from ProjectCode.Domain.Objects.User import User


class Guest(User):
    def __init__(self, entrance_id):
        super().__init__()
        self.entrance_id = entrance_id
        self.cart = Cart(self.entrance_id)

    def get_cart(self):
        # Return the user's shopping cart
        pass

    def add_to_cart(self, item):
        # Add an item to the user's shopping cart
        pass

    def purchase(self):
        # purchasing process
        pass
