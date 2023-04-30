from ProjectCode.Domain.DataObjects.DataBasket import DataBasket
from ProjectCode.Domain.Objects import Cart, Basket


class DataCart:
    def __init__(self, cart: Cart):
        self.username = cart.get_username()
        self.baskets = self.getBaskets(cart.get_baskets())

    def getBaskets(self, basket_dict):
        baskets = dict()
        for key, value in basket_dict.items():
            baskets[key] = DataBasket(value)
        return baskets




