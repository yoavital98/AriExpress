
from ProjectCode.Domain.Objects.Cart import Cart
from abc import ABC, abstractmethod


class User(ABC):
    @abstractmethod
    def __init__(self, enteranceID):
        self.enterance_ID = enteranceID

    @abstractmethod
    def get_cart(self):
        # Return the user's shopping cart
        pass

    @abstractmethod
    def add_to_cart(self, item):
        # Add an item to the user's shopping cart
        pass

    def purchase(self):
        # purchasing process
        pass
