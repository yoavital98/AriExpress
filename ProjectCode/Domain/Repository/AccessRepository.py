from ProjectCode.DAL.AccessModel import AccessModel
from ProjectCode.DAL.AccessStateModel import AccessStateModel
from ProjectCode.DAL.StoreModel import StoreModel
from ProjectCode.Domain.MarketObjects.Access import Access
from ProjectCode.Domain.Repository.Repository import Repository


class AccessRepository(Repository):

    def __init__(self, store_name):
        self.model = AccessModel
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
        from ProjectCode.Domain.MarketObjects.Store import Store
        if pk is None:
            store_entry = StoreModel.get(StoreModel.store_name == self.store_name)
            store_dom = Store(self.store_name)
            access_list = []
            for access in store_entry.accesses:
                access_dom = Access(store_dom, None, access.nominated_by_username)
                access_dom.setAccess(access.role)
                access_list.append(access_dom)
            return access_list
        else:
            store_entry = StoreModel.get(StoreModel.store_name == self.store_name)
            access_entry = store_entry.accesses.select().where(AccessModel.user.username == pk)[0]
            access_dom = Access(self.store_name, None, access_entry.nominated_by_username)
            access_dom.setAccess(access_entry.role)
            return access_dom

    def add(self, access):
        store_entry = StoreModel.get(StoreModel.store_name == self.store_name)
        permissions = access.get_access_state().get_permissions().keys()
        access_state_entry = AccessStateModel.create(permissions=','.join(permissions), state=access.get_role())
        AccessModel.create(store=store_entry, nominated_by_username=access.get_nominated_by_username(), role=access.get_role(), access_state=access_state_entry)
        return access

    def remove(self, pk):
        store_entry = StoreModel.get(StoreModel.store_name == self.store_name)
        #user_entry = UserModel.get(UserModel.username == pk)
        #access_entry = AccessModel.get(AccessModel.store == store_entry, AccessModel.user == user_entry)
        #access_entry.delete_instance()
