import string

from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.Objects.Cart import Cart
from abc import ABC, abstractmethod

from ProjectCode.Domain.Objects.User import User
from ProjectCode.Domain.Objects.AccessControl import AccessControl


class Member(User):
    def __init__(self, user_name, password, email):  # TODO need to choose whether registeration requires address and
        self._accesses = TypedDict(str, AccessControl)  # storename to Access
        # TODO birthdate
        self._username = user_name  # username
        self._password = password  # password
        self._email = email  # email
        # self.address = address
        # self.birthDate = birthDate
        self._cart = Cart(user_name)  # userCart
        self._logged_In = False  # login

    def get_cart(self):
        # Return the user's shopping cart
        return self._cart

    def add_to_cart(self, item):
        # Add an item to the user's shopping cart
        pass

    def purchase(self):
        # purchasing process
        pass

    def logInAsMember(self):
        self._logged_In = True

    def logOff(self):
        self._logged_In = False

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
        return self._logged_In

    @property
    def accesses(self):
        return self._accesses
