from abc import ABC
from ProjectCode.Domain.DataObjects.DataCart import DataCart

class DataUser(ABC):
    def __init__(self, user):
        self.entrance_id = user.get_entrance_id()
        self.cart = DataCart(user.get_cart())
