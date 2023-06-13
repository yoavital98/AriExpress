from peewee import *

from ProjectCode.DAL.ProductModel import ProductModel
from ProjectCode.DAL.StoreModel import StoreModel
from ProjectCode.Domain.MarketObjects.StoreObjects.Product import Product
from ProjectCode.Domain.Repository.Repository import Repository


class ProductRepository(Repository):

    def __init__(self, store_name):
        self.model = ProductModel
        self.store_name = store_name

    def __getitem__(self, item):
        return self.get(item)


    def __setitem__(self, key, value): #key is meaningless
        try:
            return self.add(value)
        except Exception as e:
            raise Exception("ProductRepository: __setitem__ failed: " + str(e))

    def __delitem__(self, key):
        try:
            return self.remove(key)
        except Exception as e:
            raise Exception("ProductRepository: __delitem__ failed: " + str(e))
    def __contains__(self, item):
        try:
            return self.contains(item)
        except Exception as e:
            raise Exception("ProductRepository: __contains__ failed: " + str(e))

    def get(self, pk=None):
        try:
            if pk is None:
                store = StoreModel.get(StoreModel.store_name == self.store_name)
                product_list = []
                for product in store.products:
                    product_list.append(Product(product.product_id, product.name, product.quantity, product.price, product.categories))
                return product_list
            else:
                store_entry = StoreModel.get(StoreModel.store_name == self.store_name)
                product_entry = ProductModel.get(ProductModel.product_id == pk, ProductModel.store == store_entry)
                product = Product(product_entry.product_id, product_entry.name, product_entry.quantity, product_entry.price, product_entry.categories)
                return product
        except Exception as e:
            return None


    def add(self, product: Product):
        store_entry = StoreModel.get(StoreModel.store_name == self.store_name)
        product_entry = ProductModel.get_or_none(ProductModel.product_id == product.get_product_id(), ProductModel.store == store_entry)
        if product_entry is None:
            product_entry = ProductModel.create(product_id=product.get_product_id(), store=store_entry, name=product.get_name(), quantity=product.get_quantity(), price=product.get_price(), categories=product.get_categories())
        else:
            product_entry.name = product.get_name()
            product_entry.quantity = product.get_quantity()
            product_entry.price = product.get_price()
            product_entry.categories = product.get_categories()
            product_entry.save()
        return product

    def remove(self, pk):
        model = ProductModel.get(ProductModel.product_id == pk)
        model.delete_instance()

    def keys(self):
        try:
            return [product.product_id for product in StoreModel.get(StoreModel.store_name == self.store_name).products]
        except Exception as e:
            return []

    def contains(self, item):
        return item in self.keys()

    def values(self):
        return self.get()


