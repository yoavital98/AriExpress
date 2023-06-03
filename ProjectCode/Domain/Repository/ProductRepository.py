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
        return self.add(value)

    def __delitem__(self, key):
        return self.remove(key)

    def __contains__(self, item):
         pass

    def get(self, pk=None):
        if pk is None:
            store = StoreModel.get(StoreModel.store_name == self.store_name)
            product_list = []
            for product in store.products:
                product_list.append(Product(product.product_id, product.name, product.quantity, product.price, product.categories))
            return product_list
        else:
            StoreProduct = StoreModel.products.get_through_model()
            joined = ProductModel.select().join(StoreProduct).join(StoreModel)\
                .where(
                       (StoreProduct.storemodel_id == self.store_name) &
                       (StoreProduct.productmodel_id == pk))
            product = joined[0]
            product_obj = Product(product.product_id, product.name, product.quantity, product.price, product.categories)
            return product_obj

    def add(self, product: Product):
        model = ProductModel.create(product_id=product.get_product_id(), name=product.get_name(), quantity=product.get_quantity(), price=product.get_price(), categories=product.get_categories())
        store = StoreModel.get(StoreModel.store_name == self.store_name)
        store.products.add(model)
        return product

    def remove(self, pk):
        model = ProductModel.get(ProductModel.product_id == pk)
        store = StoreModel.get(StoreModel.store_name == self.store_name)
        store.products.remove(model)
        model.delete_instance()