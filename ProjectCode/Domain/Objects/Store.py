from ProjectCode.Domain.Helpers.TypedDict import *
from ProjectCode.Domain.Objects.StoreObjects.Product import *
from ProjectCode.Domain.Objects.Access import *
import string


class Store:

    def __init__(self, store_name):
        self.store_name = store_name
        self.products = TypedDict(int, Product)
        #TODO: policies
        self.active: bool = True
        self.accesses = TypedDict(str, Access)
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
        self.products.__setitem__(self.product_id_counter, product_to_add)
        return product_to_add

    def deleteProduct(self, access, product_id):
        self.hasForProductAccess(access)
        if self.products.get(product_id) is None:
            raise Exception("Product doesn't exists")
        else:
            self.products.__delitem__(product_id)
            return product_id

    def changeProduct(self, access, product_id, **kwargs):
        self.hasForProductAccess(access)
        cur_product = self.products.get(product_id)
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


    def checkProductAvailability(self, product_id, quantity):
        cur_product = self.products[int(product_id)]
        if cur_product is None:
            raise Exception("No such product exists")
        if cur_product.quantity - quantity >= 0:
            return cur_product
        else:
            raise Exception("There isn't enough quantity")
    def searchProductByName(self, keyword):
        product_list = []
        for prod in self.products.values():
            if keyword in prod.name:
                product_list.append(prod)
        return product_list


    def searchProductByCategory(self, category):
        product_list = []
        for prod in self.products.values():
            if category in prod.categories:
                product_list.append(prod)
        return product_list


    def purchaseBasket(self, products_dict): #tup(product,qunaiity)
        overall_price = 0
        for product_id, product_tuple in products_dict.items():
            cur_product = self.products[product_id]
            if cur_product is None:
                raise Exception("No such product exists")
            cur_product.quantity -= product_tuple[1]
            overall_price += cur_product.price * product_tuple[1]
        return overall_price

    def bidRequest(self, product_id, offer):
        pass