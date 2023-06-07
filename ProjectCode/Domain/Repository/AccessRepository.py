from ProjectCode.DAL.AccessModel import AccessModel
from ProjectCode.DAL.AccessStateModel import AccessStateModel
from ProjectCode.DAL.MemberModel import MemberModel
from ProjectCode.DAL.StoreModel import StoreModel
from ProjectCode.Domain.MarketObjects.Access import Access
from ProjectCode.Domain.Repository.Repository import Repository




class AccessRepository(Repository):

    def __init__(self, store_name=None, username=None):

        self.model = AccessModel
        self.store_name = store_name
        self.username = username

    def __getitem__(self, item):
        try:
            return self.get(item)
        except Exception as e:
            raise Exception("AccessRepository: __getitem__ failed: " + str(e))

    def __setitem__(self, key, value): #key is meaningless
        try:
            return self.add(value)
        except Exception as e:
            raise Exception("AccessRepository: __setitem__ failed: " + str(e))

    def __delitem__(self, key):
        try:
            return self.remove(key)
        except Exception as e:
            raise Exception("AccessRepository: __delitem__ failed: " + str(e))

    def __contains__(self, item):
        pass


    def get(self, pk=None):
        if self.store_name is None:
            return self.getByUsername(pk=pk)
        else:
            return self.getByStorename(pk=pk)


    def getByStorename(self, pk=None):
        from ProjectCode.Domain.MarketObjects.Store import Store
        from ProjectCode.Domain.MarketObjects.UserObjects.Member import Member

        if pk is None:
            store_entry = StoreModel.get(StoreModel.store_name == self.store_name)
            store_dom = Store(self.store_name)
            access_list = []
            for access in store_entry.accesses:
                user_entry = MemberModel.get(MemberModel.user_name == access.user.user_name)
                user_dom = Member(-1, user_entry.user_name, user_entry.password, user_entry.email)
                access_list.append(self.__createDomainObject(access, store_dom, user_dom))
            return access_list
        else:
            store_entry = StoreModel.get(StoreModel.store_name == self.store_name)
            user_entry = MemberModel.get(MemberModel.user_name == pk)
            access_entry = AccessModel.get(AccessModel.store == store_entry, AccessModel.user == user_entry)
            return self.__createDomainObject(access_entry, Store(self.store_name), Member(-1, user_entry.user_name, user_entry.password, user_entry.email))

    def getByUsername(self, pk=None):
        from ProjectCode.Domain.MarketObjects.Store import Store
        from ProjectCode.Domain.MarketObjects.UserObjects.Member import Member

        if pk is None:
            user_entry = MemberModel.get(MemberModel.user_name == self.username)
            member_dom = Member(-1, user_entry.user_name, user_entry.password, user_entry.email)
            access_list = []
            for access in user_entry.accesses:
                store_dom = Store(access.store.store_name)
                access_list.append(self.__createDomainObject(access, store_dom, member_dom))
            return access_list
        else:
            user_entry = MemberModel.get_or_none(MemberModel.user_name == self.username)
            store_entry = StoreModel.get_or_none(StoreModel.store_name == pk)
            access_entry = AccessModel.get_or_none(AccessModel.store == store_entry, AccessModel.user == user_entry)
            if user_entry is None or store_entry is None or access_entry is None:
                return None
            return self.__createDomainObject(access_entry, Store(pk), Member(-1, user_entry.user_name, user_entry.password, user_entry.email))

    def __createDomainObject(self, access_entry, store_dom, user_dom):
        access_dom = Access(store_dom, user_dom, access_entry.nominated_by_username)
        access_dom.setAccess(access_entry.role)
        access_dom.get_access_state().setPermissions(list(access_entry.access_state.permissions.split(',')))
        return access_dom

    def add(self, access):

        store_entry = StoreModel.get(StoreModel.store_name == self.store_name)
        permissions = access.get_access_state().get_permissions().keys()
        user_entry = MemberModel.get(MemberModel.user_name == access.get_user().get_username())
        access_entry = AccessModel.get_or_none(AccessModel.store == store_entry, AccessModel.user == user_entry)
        access_state_entry = AccessStateModel.create(permissions=','.join(permissions), state=access.get_role())

        if access_entry is not None:
            #update
            access_entry.access_state = access_state_entry
            access_entry.role = access.get_role()
            access_entry.nominated_by_username = access.get_nominated_by_username()
            access_entry.save()
            return access
        AccessModel.create(store=store_entry, user=user_entry, nominated_by_username=access.get_nominated_by_username(), role=access.get_role(), access_state=access_state_entry)
        return access

    def remove(self, pk):
        store_entry = StoreModel.get(StoreModel.store_name == self.store_name)
        user_entry = MemberModel.get(MemberModel.user_name == pk)
        access_entry = AccessModel.get(AccessModel.store == store_entry, AccessModel.user == user_entry)
        access_entry.access_state.delete_instance()
        access_entry.delete_instance()



    def keys(self):
        if self.store_name is None: #-> then return list of storenames
            return [ StoreModel.get_by_id(access.store).store_name for access in MemberModel.get(MemberModel.user_name == self.username).accesses]
        else: #-> then return list of usernames
            store_entry = StoreModel.get(StoreModel.store_name == self.store_name)
            access_query = AccessModel.select().where(AccessModel.store == store_entry)
            return [ MemberModel.get_by_id(access.user).user_name for access in access_query]


    def values(self):
        if self.store_name is None:
            return self.getByUsername()
        else:
            return self.getByStorename()