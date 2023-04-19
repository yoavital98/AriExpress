import string

import ProjectCode
from ProjectCode.Domain.Controllers.ExternalServices import *
from ProjectCode.Domain.Controllers.MessageController import *
from ProjectCode.Domain.Objects import User, Store, Access
from ProjectCode.Domain.Objects.ExternalObjects.PasswordValidation import PasswordValidation
from ProjectCode.Domain.Objects.UserObjects import Member, Admin, Guest
from ProjectCode.Domain.Controllers.TransactionHistory import *
from ProjectCode.Domain.Objects.Store import *
from ProjectCode.Domain.Objects.UserObjects.Guest import *
from ProjectCode.Domain.Objects.UserObjects.Member import *
from ProjectCode.Domain.Objects.Cart import *
from typing import List

class StoreFacade:
    def __init__(self):
        self.members = TypedDict(string, Member)    # dict of
        self.stores = TypedDict(string, Store)  # by id
        self.onlineGuests = TypedDict(string, Guest)
        # self.onlineUsers = TypedDict(string, Guest) --optional instead of onlineGuests--
        self.external_services = ExternalServices()
        self.message_controller = MessageController()
        self.transaction_history = TransactionHistory()
        self.accesses = TypedDict(string, Access)  # optional TODO check key type
        self.nextEntranceID = 0  # guest ID counter
        self.cart_ID_Counter = 0  # cart counter
        self.loadData()
        self.passwordValidator = PasswordValidation()

    def loadData(self):  # todo complete
        pass


# ------  users  ------ #

    #  Guests

    def exitTheSystem(self):
        pass

    #  Members
    def __checkIfUserIsLoggedIn(self, username):
        if self.members.keys().__contains__(username):
            existing_member: Member = self.members[username]
            return existing_member.get_logged()
        else: #should never get here usually
            raise Exception("user is not logged in")

    def register(self, username, password, email):
        if not self.members.keys().__contains__(str(username)):
            password_validator = PasswordValidation()
            if password_validator.ValidatePassword(password):
                new_member = Member(username, password, email)
                self.members[str(username)] = new_member
                return new_member
        else:
            pass



    def logInAsGuest(self):
        new_guest = Guest(self.nextEntranceID)
        self.onlineGuests[str(self.nextEntranceID)] = new_guest
        self.nextEntranceID += 1
        return new_guest

    def leaveAsGuest(self, EntranceID):
        if self.onlineGuests.keys().__contains__(str(EntranceID)):
            self.onlineGuests.__delitem__(EntranceID)
        else:
            pass


    def logInAsMember(self, username , password):
        if self.members.keys().__contains__(username):
            existing_member: Member = self.members[username]
            password_validator = PasswordValidation()
            if password_validator.ConfirmePassword(password, existing_member.get_password()):
                existing_member.logInAsMember()
                return existing_member
            else:
                raise Exception("username or password does not match")
        else:
            raise Exception("username or password does not match")


    def logOut(self,username):
        if self.members.keys().__contains__(username):
            existing_member: Member = self.members[username]
            existing_member.logOff()
        else:
            pass
    def getMemberPurchaseHistory(self, username):
        if self.__checkIfUserIsLoggedIn(username):
            return TransactionHistory.get_User_Transactions(username)


    def getBasket(self,username, storename):
        if self.__checkIfUserIsLoggedIn(username):
            existing_member: Member = self.members[username]
            requested_basket = existing_member.get_cart().get_Basket(storename)
            return requested_basket
        else:
            raise Exception("user is not logged in")

    def getCart(self,username):
        if self.__checkIfUserIsLoggedIn(username):
            existing_member: Member = self.members[username]
            requested_cart = existing_member.get_cart()
            return requested_cart
        else:
            raise Exception("user is not logged in")

    def addToBasket(self,username, storename, productname, quantity): # this function should first go to the store and check if we can even add to the basket
        if self.__checkIfUserIsLoggedIn(username):
            existing_member: Member = self.members[username]
            # TODO: amiel this is where you use your logic to give me the item ID and the product!!!
            existing_member.add_to_cart(storename, 0, 0, quantity) #TODO: chage the 0, 0 to the productID and to the product itself
        else:
            raise Exception("user is not logged in")

    def removeFromBasket(self):
        pass

    def editBasketQuantity(self):
        pass

    def purchaseCart(self):
        pass

    # ------  stores  ------ #

    def getStores(self):
        return self.stores

    def getProductsByStore(self, store_name):
        cur_store: Store = self.stores[store_name]
        if cur_store is None:
            raise Exception("No such store exists")
        return cur_store.products

    def getProduct(self, store_name, product_id):
        cur_store: Store = self.stores[store_name]
        if cur_store is None:
            raise Exception("No such store exists")
        cur_product = cur_store.products[product_id]
        return cur_product

    def productSearchByName(self, keywords):  # and keywords
        splitted_keywords = keywords.split(" ")
        search_results = TypedDict(Store, List[Product])
        for keyword in splitted_keywords:
            for cur_store in self.stores.values():
                product_list = cur_store.searchProductByName(keyword)
                if len(product_list) > 0:
                    search_results[cur_store] = product_list
        return search_results

    def productSearchByCategory(self, category):
        search_results = TypedDict(Store, List[Product])
        for cur_store in self.stores.values():
            product_list = cur_store.searchProductByCategory(category)
            if len(product_list) > 0:
                search_results[cur_store] = product_list
        return search_results

    def productFilterByFeatures(self):
        pass



    def placeBid(self):
        pass

    def getStorePurchaseHistory(self):
        pass

    # ------  Management  ------ #
    #TODO: add check if user is loggedin to each function

    def openStore(self, username, store_name):
        cur_member: Member = self.members.get(username)
        if cur_member is None:
            raise Exception("The user is not a member")
        cur_store = Store(store_name)
        new_access = Access(cur_member, cur_store)
        cur_member.accesses[store_name] = new_access
        cur_store.setFounder(cur_member.user_name, new_access)
        self.stores[store_name] = cur_store
        return cur_store


    def addNewProductToStore(self, username, store_name, name, quantity, price, categories):
        cur_store: Store = self.stores[store_name]
        if cur_store is None:
            raise Exception("No such store exists")
        #cur_member: Member = self.members[str(requester_id)]
        new_product = cur_store.addProduct(username, name, quantity, price, categories)
        return new_product


    def removeProductFromStore(self, username, store_name, product_id):
        cur_store: Store = self.stores[store_name]
        if cur_store is None:
            raise Exception("No such store exists")
        cur_access = self.members[username].accesses[store_name]
        if cur_access is None:
            raise Exception("The member doesn't have a permission for that action")
        deleted_product_id = cur_store.deleteProduct(cur_access, product_id)
        return deleted_product_id

    def editProductOfStore(self, username, store_name, product_id, **kwargs):
        cur_store: Store = self.stores[store_name]
        if cur_store is None:
            raise Exception("No such store exists")
        cur_access = self.members[username].accesses[store_name]
        if cur_access is None:
            raise Exception("The member doesn't have a permission for that action")
        changed_product = cur_store.changeProduct(cur_access, product_id, **kwargs)
        return changed_product

    def nominateStoreOwner(self, requester_username, nominated_username, store_name):
        cur_store: Store = self.stores[store_name]
        if cur_store is None:
            raise Exception("No such store exists")
        nominated_access = self.members[nominated_username].accesses[store_name]
        if nominated_access is None:
            nominated_access = Access(cur_store,self.members[nominated_username])
            self.members[nominated_access].accesses[store_name] = nominated_access
        nominated_modified_access = cur_store.setAccess(nominated_access, requester_username, nominated_username, isOwner=True)
        return nominated_modified_access

    def nominateStoreManager(self, requester_username, nominated_username, store_name):
        cur_store: Store = self.stores[store_name]
        if cur_store is None:
            raise Exception("No such store exists")
        nominated_access = self.members[nominated_username].accesses[store_name]
        if nominated_access is None:
            nominated_access = Access(cur_store, self.members[nominated_username])
            self.members[nominated_access].accesses[store_name] = nominated_access
        nominated_modified_access = cur_store.setAccess(nominated_access, requester_username, nominated_username,
                                                        isManager=True)
        return nominated_modified_access

    def addPermissionsForManager(self):
        pass

    def editPermissionsForManager(self):
        pass

    def closeStore(self, username, store_name):
        cur_store: Store = self.stores[store_name]
        if cur_store is None:
            raise Exception("No such store exists")
        is_founder = cur_store.closeStore(username)
        #TODO: may need to delete other delegations that relates to Store
        if is_founder:
            #deletes all accesses for that store
            for mem in self.members.values():
                store_exists = mem.accesses[store_name]
                if store_exists is not None:
                    del mem.accesses[store_name]

            del self.stores[store_name]
        return store_name


    def getStaffInfo(self, username, store_name):
        cur_store: Store = self.stores[store_name]
        if cur_store is None:
            raise Exception("No such store exists")
        accesses_dict = cur_store.getStaffInfo(username)
        return accesses_dict

    def getStoreManagerPermissions(self):
        pass

