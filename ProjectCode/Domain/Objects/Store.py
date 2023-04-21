from ProjectCode.Domain.Helpers.TypedDict import *
from ProjectCode.Domain.Objects.StoreObjects.Product import *
from ProjectCode.Domain.Objects.AccessControl import *
import string


class Store:

    def __init__(self, store_name):
        self.store_name = store_name
        self.product = TypedDict(int, Product)
        #TODO: policies
        self.active: bool = True
        self.accesses = TypedDict(str, AccessControl)
        self.product_id_counter = 0

    def setFounder(self, username, access):
        access.setFounder(True)
        self.accesses[username] = access


    def setAccess(self, nominated_access, requester_username, nominated_username, **kwargs):
        self.accesses[nominated_username] = nominated_access
        requester_access = self.accesses[requester_username]
        if requester_access is None:
            raise Exception("The member doesn't have the appropriate permission for that store")
        if requester_access.isOwner or requester_access.isManager or requester_access.isFounder:#TODO: change according to permission policy
            modified_access = self.modify_attributes(nominated_access, **kwargs)
            return modified_access
        else:
            raise Exception("Member doesn't have the permission in this store")

    def addProduct(self, access, name, quantity, price, categories):
        self.hasForProductAccess(access)
        self.product_id_counter += 1
        product_to_add = Product(self.product_id_counter, name, quantity, price, categories)
        self.product.__setitem__(self.product_id_counter,product_to_add)
        return product_to_add

    def deleteProduct(self, access, product_id):
        self.hasForProductAccess(access)
        if self.product.get(product_id) is None:
            raise Exception("Product doesn't exists")
        else:
            self.product.__delitem__(product_id)
            return product_id

    def changeProduct(self, access, product_id, **kwargs):
        self.hasForProductAccess(access)
        cur_product = self.product.get(product_id)
        if cur_product is None:
            raise Exception("Product doesn't exists")
        for k, v in kwargs.items():
            try:
                getattr(cur_product,k)
            except AttributeError:
                raise Exception("No such attribute exists")
            setattr(cur_product, k, v)
        return cur_product


    def hasForProductAccess(self, access):
        #TODO: change according to permission policy
        if access.isOwner or access.isFounder or access.isManager:
            return True
        else:
            raise Exception("The member has no permission for that action")


    #TODO: may cause problem for unknown reasons
    def modify_attributes(self, object_to_modify, **kwargs):
        for k, v in kwargs.items():
            try:
                getattr(object_to_modify, k)
            except AttributeError:
                raise Exception("No such attribute exists")
            setattr(object_to_modify, k, v)
        return object_to_modify


    def closeStore(self, requester_username):
        cur_access = self.accesses[requester_username]
        if cur_access.isFounder:

            return True
        else:
            raise Exception("Member isn't the founder of the store")


    def getStaffInfo(self, username):
        cur_access = self.accesses[username]
        if cur_access is None:
            raise Exception("Member has no access for that store")
        if cur_access.isFounder or cur_access.isOwner or cur_access.isManager:
            return self.accesses
        else:
            raise Exception("Member has no access for that action")

