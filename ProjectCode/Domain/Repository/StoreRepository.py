from ProjectCode.DAL.StoreModel import StoreModel
from ProjectCode.Domain.MarketObjects.Store import Store
from ProjectCode.Domain.Repository.Repository import Repository


class StoreRepository(Repository):

    def __init__(self):
        self.model = StoreModel

    def __getitem__(self, user_name):
        return self.get(user_name)

    def __setitem__(self, key, value): #key is meaningless
        try:
            return self.add(value)
        except Exception as e:
            raise Exception("StoreRepository: __setitem__ failed: " + str(e))

    def __delitem__(self, key):
        try:
            return self.remove(key)
        except Exception as e:
            raise Exception("StoreRepository: __delitem__ failed: " + str(e))

    def __contains__(self, item):
         pass

    def get(self, pk=None):
        try:
            if pk is None:
                store_entry = StoreModel.select()
                store_list = []
                for store in store_entry:
                    store_obj = Store(store.store_name)
                    store_obj.set_counters(store.active, store.closed_by_admin, store.product_id_counter, store.auction_id_counter, store.lottery_id_counter)
                    store_list.append(store_obj)
                return store_list
            else:
                store_entry = StoreModel.get(StoreModel.store_name == pk)
                store_obj = Store(store_entry.store_name)
                store_obj.set_counters(store_entry.active, store_entry.closed_by_admin, store_entry.product_id_counter, store_entry.auction_id_counter,
                                   store_entry.lottery_id_counter)
                return store_obj
        except Exception as e:
            return None


    def add(self, store):
        StoreModel.create(store_name=store.get_store_name(), active=store.active, closed_by_admin=store.closed_by_admin, product_id_counter=store.product_id_counter)
        return store

    def remove(self, pk):
        store_entry = StoreModel.get(StoreModel.store_name == pk)
        for product in store_entry.products:
            product.delete_instance()
        store_entry.delete_instance()

    def keys(self):
        return [store.store_name for store in StoreModel.select()]

    def values(self):
        return self.get()

    def items(self):
        for key, value in zip(self.keys(), self.values()):
            yield key, value
