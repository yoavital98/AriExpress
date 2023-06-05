

from ProjectCode.DAL.BasketModel import BasketModel
from ProjectCode.DAL.StoreModel import StoreModel
from ProjectCode.Domain.MarketObjects.Basket import Basket
from ProjectCode.Domain.MarketObjects.Store import Store
from ProjectCode.Domain.MarketObjects.StoreObjects.Product import Product
from ProjectCode.Domain.Repository.Repository import Repository


class BasketRepository(Repository):

    def __init__(self):
        self.model = BasketModel

    def __getitem__(self, store_name):
        try:
            return self.get(store_name)
        except Exception as e:
            raise Exception("BasketsRepository: __getitem__ failed: " + str(e))

    def __setitem__(self, key, value): #key is meaningless
        try:
            return self.add(value)
        except Exception as e:
            raise Exception("BasketsRepository: __setitem__ failed: " + str(e))

    def __delitem__(self, key):
        try:
            return self.remove(key)
        except Exception as e:
            raise Exception("BasketsRepository: __delitem__ failed: " + str(e))

    def __contains__(self, item):
        try:
            return self.contains(item)
        except Exception as e:
            raise Exception("BasketsRepository: __delitem__ failed: " + str(e))

    def get(self, pk=None):
        if pk is None:
            basket_list = []
            for basket_entry in self.model.select():
                basket = Basket(basket_entry.user_name, Store(basket_entry.store.store_name))
                for product_basket_entry in basket_entry.products:
                    product_entry = product_basket_entry.product
                    product = Product(
                        product_entry.product_id,
                        product_entry.name,
                        product_basket_entry.quantity,
                        product_entry.price,
                        product_entry.categories
                    )
                    basket.products[product.product_id] = (
                        product,
                        product_basket_entry.quantity,
                        product_entry.price
                    )
                basket_list.append(basket)
            return basket_list
        else:
            basket_entry = self.model.get(store=pk)
            basket = Basket(basket_entry.user_name, basket_entry.store)
            for product_basket_entry in basket_entry.products:
                product_entry = product_basket_entry.product
                product = Product(
                    product_entry.product_id,
                    product_entry.name,
                    product_basket_entry.quantity,
                    product_entry.price,
                    product_entry.categories
                )
                basket.products[product.product_id] = (
                    product,
                    product_basket_entry.quantity,
                    product_entry.price
                )
            return basket

    def add(self, basket: Basket):
        store_entry = StoreModel.get_by_id(basket.store.get_store_name())
        basket_entry = self.model.create(user_name=basket.username, store=store_entry)
        return basket
        # for product_id, product_info in basket.products.items():
        #     product = product_info[0]  # product object
        #     quantity = product_info[1]
        #     price = product_info[2]
        #     product_entry = ProductBasketModel.create(
        #         product_id=product.product_id,
        #         name=product.name,
        #         quantity=quantity,
        #         price=product.price,
        #         categories=product.categories
        #     )
        #    ProductBasketModel.create(quantity=quantity, product=product_entry, basket=basket_entry, price=price)
        return True

    def remove(self, pk):
        cart_entry = self.model.get(user_name=pk)
        cart_entry.delete_instance()
        return True


    def keys(self):
        return [basket.store.get_store_name() for basket in BasketModel.select()]

    def values(self):
        return self.get()

    def contains(self, store_name):
        query = self.model.select().where(self.model.store.store_name == store_name)
        return query.exists()
