

from ProjectCode.DAL.BasketModel import BasketModel
from ProjectCode.DAL.StoreModel import StoreModel
from ProjectCode.Domain.MarketObjects.Basket import Basket
from ProjectCode.Domain.MarketObjects.Store import Store
from ProjectCode.Domain.MarketObjects.StoreObjects.Product import Product
from ProjectCode.Domain.Repository.Repository import Repository


class BasketRepository(Repository):

    def __init__(self, user_name):
        self.model = BasketModel
        self.user_name = user_name

    def __getitem__(self, store_name):
        return self.get(store_name)


    def __setitem__(self, key, value): #key is meaningless
        try:
            return self.add(key, value)
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
        try:
            if pk is None:
                basket_list = []
                for basket_entry in self.model.select():
                    basket = self.__createDomainObject(basket_entry)
                    basket_list.append(basket)
                return basket_list
            else:
                basket_entry = self.model.get(BasketModel.store==pk, BasketModel.user_name==self.user_name)
                basket = self.__createDomainObject(basket_entry)
                return basket
        except Exception as e:
            return None

    def __createDomainObject(self, basket_entry):
        basket = Basket(basket_entry.user_name, Store(basket_entry.store.store_name))
        for product_basket_entry in basket_entry.products:
            product_entry = product_basket_entry.product_model
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

    def add(self, key, basket: Basket):
        store_entry = StoreModel.get(StoreModel.store_name == key)
        basket_entry = self.model.get_or_none(BasketModel.store == key, BasketModel.user_name == self.user_name)
        if basket_entry is None:
            #create
            self.model.create(user_name=basket.username, store=store_entry)
        else:
            #update
            pass
        return basket

    def remove(self, pk):
        basket_entry = self.model.get(BasketModel.store == pk, BasketModel.user_name == self.user_name)
        for product_basket_entry in basket_entry.products:
            product_basket_entry.delete_instance()
        basket_entry.delete_instance()
        return True


    def keys(self):
        return [basket.store.store_name for basket in BasketModel.select()]

    def values(self):
        return self.get()

    def items(self):
        for key, value in zip(self.keys(), self.values()):
            yield key, value

    def contains(self, store_name):
        query = self.model.select().where(self.model.store.store_name == store_name)
        return query.exists()
