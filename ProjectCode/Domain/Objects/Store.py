from ProjectCode.Domain.Helpers.TypedDict import *
from StoreObjects.Product import *
from Access import *


class Store:

    def __init__(self, store_id: int, founder: Access):
        self.store_id: int = store_id
        self.product = TypedDict(int, Product)
        #TODO: policies
        self.active: bool = True
        self.founder: Access = founder
        self.managers = TypedDict(int, Access)
        self.product_id_counter = 0

    def addProduct(self, name, quantity, price, categories):
        self.product_id_counter += 1
        product_to_add = Product(self.product_id_counter, name, quantity, price, categories)
        self.product.__setitem__(self.product_id_counter,product_to_add)
        return product_to_add

    def deleteProduct(self, product_id):
        if self.product.get(product_id) is None:
            raise Exception("Product doesn't exists")
        else:
            self.product.__delitem__(product_id)
            return product_id

    def changeProduct(self, product_id, **kwargs):
        cur_product = self.product.get(product_id)
        if cur_product is None:
            raise Exception("Product doesn't exists")
        for k, v in kwargs.items():
            try:
                getattr(cur_product,k)
            except AttributeError:
                raise Exception("No such attribute exists")
            setattr(cur_product, k, v)
        return cur_product
