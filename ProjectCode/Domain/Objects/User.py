
from ProjectCode.Domain.Objects.Cart import Cart
from abc import ABC, abstractmethod


class User(ABC):

    @abstractmethod
    def get_cart(self):
        # Return the user's shopping cart
        pass

    @abstractmethod
    def add_to_cart(self, storename, productID, product, quantity):
        # Add an item to the user's shopping cart
        pass

    def purchase(self):
        # purchasing process
        pass
