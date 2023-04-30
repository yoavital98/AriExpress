from abc import ABC
from ProjectCode.Domain.DataObjects.DataCart import DataCart

class DataUser(ABC):
    def __init__(self, user):
        self.username = user.get_username()
        self.cart = DataCart(user.get_cart())
