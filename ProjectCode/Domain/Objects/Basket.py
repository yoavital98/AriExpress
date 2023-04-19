

from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.Objects.Store import Store
from ProjectCode.Domain.Objects.StoreObjects.Product import Product


class Basket:
    def __init__(self, cart_id, store):
        self.cart_id = cart_id
        self.store: Store = store
        self.products = TypedDict(int, tuple)#  (product, quantity)

    def add_Product(self,productID, product, quantity):
        if not self.products.keys().__contains__(productID):
            self.products[productID] = (product, quantity)
        else:
            raise Exception ("product already exists in the basket")

    def remove_Product(self, productID):
        if self.products.keys().__contains__(productID):
            self.products.__delitem__(productID)
            return True
        else:
            return False

    def get_Cart_Id(self):
        return self.cart_id

    def set_Cart_Id(self, cart_id):
        self.cart_id = cart_id

    def get_Store(self):
        return self.store

    def set_Store(self, store):
        self.store = store

    def get_Products(self):
        return self.products
    def checkProductExistance(self, productID):
        return self.products.keys().__contains__(productID)

    def getBasketSize(self):
        return self.products.__sizeof__()
