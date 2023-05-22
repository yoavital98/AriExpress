from ProjectCode.DAL.Repository import Repository
from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.MarketObjects.StoreObjects.Product import Product


class ProductRepository(Repository):

    def __init__(self):
        self.cache = TypedDict(int, Product)

    def get(self, pk=None):
        if pk is None:
            return self.cache
        else:
            if self.cache.get(pk) is None:
                raise Exception("No such product exists")
            return self.cache[pk]

    def add(self, pk, product):
        if self.cache.get(pk) is None:
            raise Exception("No such product exists")
        self.cache[pk] = product

    def remove(self, pk):
        if self.cache.get(pk) is None:
            raise Exception("No such product exists")
        del self.cache[pk]