

from ProjectCode.DAL.BasketModel import BasketModel
from ProjectCode.DAL.ProductBasketModel import ProductBasketModel
from ProjectCode.DAL.StoreModel import StoreModel
from ProjectCode.Domain.MarketObjects.StoreObjects.Product import Product
from ProjectCode.Domain.Repository.Repository import Repository


class ProductBasketRepository(Repository):

    def __init__(self, user_name, store_name):
        self.model = ProductBasketModel
        self.user_name = user_name
        self.store_name = store_name


    def __getitem__(self, product_id):
        try:
            return self.get(product_id)
        except Exception as e:
            raise Exception("ProductBasketRepository: __getitem__ failed: " + str(e))

    def __setitem__(self, key, value): #key is meaningless
        try:
            return self.add(value)
        except Exception as e:
            raise Exception("ProductBasketsRepository: __setitem__ failed: " + str(e))

    def __delitem__(self, key):
        try:
            return self.remove(key)
        except Exception as e:
            raise Exception("ProductBasketRepository: __delitem__ failed: " + str(e))

    def __contains__(self, item):
        try:
            return self.contains(item)
        except Exception as e:
            raise Exception("BasketsRepository: __delitem__ failed: " + str(e))

    def get(self, pk=None):
        if pk is None:
            products = []
            query = self.model.select()
            for product_basket_entry in query:
                product_entry = product_basket_entry.product
                product: Product = Product(product_entry.product_id,
                                           product_entry.product_name,
                                           product_entry.quantity,
                                           product_entry.price,
                                           product_entry.categories)
                quantity = product_basket_entry.quantity
                price = product_basket_entry.price
                products.append((product, quantity, price))
            return products
        else:
            product_basket_entry = self.model.get(self.model.product_id == pk)
            product_entry = product_basket_entry.product
            product: Product = Product(product_entry.product_id,
                                       product_entry.product_name,
                                       product_entry.quantity,
                                       product_entry.price,
                                       product_entry.categories)
            quantity = product_basket_entry.quantity
            price = product_basket_entry.price
            to_return = (product, quantity, price)
            return to_return

    def add(self, product_data):
        store_entry = StoreModel.get_by_id(self.store_name)
        basket_query = self.model.get(BasketModel.user_name == self.user_name, BasketModel.store == store_entry)
        product, quantity, price = product_data
        product_query = store_entry.products.get(product_id=product.product_id)
        self.model.create(product_id=product.get_product_id(),
                          quantity=quantity,
                          price=price,
                          basket=basket_query,
                          product=product_query)
        return product_data

    def remove(self, pk):
        cart_entry = self.model.get(product_id=pk)
        cart_entry.delete_instance()
        return True


    def keys(self):
        return [p.product_id for p in ProductBasketModel.select()]

    def values(self):
        return self.get()

    def contains(self, product_id):
        query = self.model.select().where(self.model.product_id == product_id)
        return query.exists()
