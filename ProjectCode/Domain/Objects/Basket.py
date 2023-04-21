

from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.Objects.Store import Store
from ProjectCode.Domain.Objects.StoreObjects.Product import Product


class Basket:
    def __init__(self, cart_id, store):
        self.cart_id = cart_id
        self.store: Store = store
        self.products = TypedDict(int, tuple)  # product id -> (product_name, quantity)

    def add_Product(self, product_ID, product_name, quantity):
        if quantity <= 0:
            raise Exception("quantity cannot be set to 0 or negative number")
        if not self.products.keys().__contains__(product_ID):
            self.products[product_ID] = (product_name, quantity)
        else:
            raise Exception ("product already exists in the basket")

    def edit_Product_Quantity(self, product_ID, quantity):
        if quantity <= 0:
            raise Exception("quantity cannot be set to 0 or negative number")
        product: tuple = self.products[product_ID]
        product[1] = quantity

    def remove_Product(self, product_ID):
        if self.products.keys().__contains__(product_ID):
            self.products.__delitem__(product_ID)
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

    def checkProductExistance(self, product_ID):
        return self.products.keys().__contains__(product_ID)

    def getBasketSize(self):
        return self.products.__sizeof__()

    def getProductsAsTuples(self):
        self.products.values()
