from ProjectCode.Domain.Objects.Cart import Cart
from abc import ABC, abstractmethod

from ProjectCode.Domain.Objects.User import User


class Member(User):
    def __init__(self, user_name, password, email):  # TODO need to choose whether registeration requires address and
                                                     # TODO birthdate
        super().__init__()
        self.user_name = user_name
        self.password = password
        self.email = email
        # self.address = address
        # self.birthDate = birthDate
        self.cart = Cart(user_name)

    def get_cart(self):
        # Return the user's shopping cart
        pass

    def add_to_cart(self, item):
        # Add an item to the user's shopping cart
        pass

    def purchase(self):
        # purchasing process
        pass
