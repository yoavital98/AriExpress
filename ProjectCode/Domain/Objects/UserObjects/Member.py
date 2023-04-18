import string

from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.Objects.Cart import Cart
from abc import ABC, abstractmethod

from ProjectCode.Domain.Objects.User import User
from ProjectCode.Domain.Objects import Access

class Member(User):
    def __init__(self, user_name, password, email):  # TODO need to choose whether registeration requires address and
        self.accesses = TypedDict(string, Access)   # storename to Access                                          # TODO birthdate
        self.user_name = user_name #username
        self.password = password #password
        self.email = email #email
        # self.address = address
        # self.birthDate = birthDate
        self.cart = Cart(user_name) #userCart
        self.logged_In = False #login

    def get_cart(self):
        # Return the user's shopping cart
        pass

    def add_to_cart(self, item):
        # Add an item to the user's shopping cart
        pass

    def purchase(self):
        # purchasing process
        pass
    def logInAsMember(self):
        self.logged_In = True

    def logOff(self):
        self.logged_In = False

    def get_username(self):
        return self._username

    def set_username(self, username):
        self._username = username

    def get_password(self):
        return self._password

    def set_password(self, password):
        self._password = password

    def get_email(self):
        return self._email

    def set_email(self, email):
        self._email = email
    def get_logged(self):
        return self.logged_In