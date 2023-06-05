from ProjectCode.DAL.StoreModel import StoreModel
from ProjectCode.Domain.MarketObjects.Store import Store
from ProjectCode.Domain.Repository.Repository import Repository


class StoreRepository(Repository):

    def __init__(self):
        self.model = StoreModel

    def __getitem__(self, user_name):
        try:
            return self.get(user_name)
        except Exception as e:
            raise Exception("StoreRepository: __getitem__ failed: " + str(e))

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
        if pk is None:
            store_entry = StoreModel.select()
            store_list = []
            for store in store_entry:
                store_list.append(Store(store.store_name))
            return store_list
        else:
            store_entry = StoreModel.get(StoreModel.store_name == pk)
            return Store(store_entry.store_name)

    def add(self, store):
        StoreModel.create(store_name=store.get_store_name())
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
