import string

import ProjectCode
from ProjectCode.Domain.Controllers.ExternalServices import *
from ProjectCode.Domain.Controllers.MessageController import *
from ProjectCode.Domain.Objects import User, Store, Access
from ProjectCode.Domain.Objects.UserObjects import Member, Admin, Guest
from ProjectCode.Domain.Controllers.TransactionHistory import *
from ProjectCode.Domain.Objects.Store import *
from ProjectCode.Domain.Objects.UserObjects.Guest import *
from ProjectCode.Domain.Objects.UserObjects.Member import *
from ProjectCode.Domain.Objects.Cart import *
from ProjectCode.Domain.Objects.Basket import *
from ProjectCode.Domain.Objects.UserObjects.Admin import *
from typing import List


class StoreFacade:
    def __init__(self):
        self.admins = TypedDict(string, Admin)  # dict of admins
        self.members = TypedDict(string, Member)    # dict of members
        self.onlineGuests = TypedDict(string, Guest)  # dict of users
        self.stores = TypedDict(string, Store)  # dict of stores
        self.external_services = ExternalServices()  # external services
        self.message_controller = MessageController()  # Messanger
        self.transaction_history = TransactionHistory()  # Transactions log
        self.accesses = TypedDict(string, Access)  # optional TODO check key type
        self.nextEntranceID = 0  # guest ID counter
        self.cart_ID_Counter = 0  # cart counter
        self.loadData()
        self.SystemStatus = False  # True = System on, False = System off
        first_admin: Admin = Admin("Ari", "123", "arioshryz@gmail.com")
        self.admins["Ari"] = first_admin

    def loadData(self):  # todo complete
        pass


# ------  users  ------ #

    #  Guests

    def exitTheSystem(self):
        pass

    #  Members
    def __checkIfUserIsLoggedIn(self, username):
            existing_member: Member = self.members[username]
            if existing_member.get_logged():
                return True
            else: #should never get here usually
                raise Exception("user is not logged in")
    def __getUserOrMember(self,username):
        if self.members.keys().__contains__(username):
            if self.__checkIfUserIsLoggedIn(username):
                return self.members[username]
            else:
                raise Exception("user is not logged in")
        else:
            if self.onlineGuests.keys().__contains__(username):
                return self.onlineGuests.get(username)
            else:
                raise Exception("user is not guest nor a member")

    def register(self, username, password, email):
        if not self.members.keys().__contains__(str(username)):
            if ExternalServices.ValidatePassword(password):
                new_member = Member(username, password, email, self.cart_ID_Counter)
                self.cart_ID_Counter += 1
                self.members[str(username)] = new_member
                return new_member
        else:
            pass

    # only guests
    def logInAsGuest(self):
        new_guest = Guest(self.nextEntranceID, self.cart_ID_Counter)
        self.cart_ID_Counter += 1
        self.onlineGuests[str(self.nextEntranceID)] = new_guest
        self.nextEntranceID += 1
        return new_guest

    # only guests

    def leaveAsGuest(self, EntranceID):
        if self.onlineGuests.keys().__contains__(str(EntranceID)):
            self.onlineGuests.__delitem__(EntranceID)

    #  only members
    def logInAsMember(self, username , password):
        if self.members.keys().__contains__(username):
            existing_member: Member = self.members[username]
            if ExternalServices.ConfirmePassword(password, existing_member.get_password()):
                existing_member.logInAsMember()
                return existing_member
            else:
                raise Exception("username or password does not match")
        else:
            raise Exception("username or password does not match")

    #  only members
    def logOut(self, username):
        if self.members.keys().__contains__(username):
            existing_member: Member = self.members[username]
            existing_member.logOff()

    #  only members

    def getMemberPurchaseHistory(self, username):
        if self.__checkIfUserIsLoggedIn(username):
            return TransactionHistory.get_User_Transactions(username)

    # guest and member
    def getBasket(self, username, storename):
        user = self.__getUserOrMember(username)
        requested_basket = user.get_Basket(storename)
        return requested_basket

    # guest and member
    def getCart(self,username):
        user: User = self.__getUserOrMember(username)
        requested_cart = user.get_cart()
        return requested_cart

    # guest and member
    def addToBasket(self, username, storename, productID, quantity): # this function should first go to the store and check if we can even add to the basket
        user: User = self.__getUserOrMember(username)
        store: Store = self.stores[storename]
        product = store.checkProductAvailability(productID, quantity)  #TODO: amiel needs to implement that method
        if product is not None:
            user.add_to_cart(storename, productID, product, quantity)
        else:
            raise Exception("Product is not available or quantity is higher than the stock")

    # guest and member
    def removeFromBasket(self, username, storename, productID):
        user: User = self.__getUserOrMember(username)
        remove_success = user.removeFromBasket(storename, productID)
        if remove_success:
            return remove_success
        else:
            raise Exception("there was a problem with removing the item or either the item doesnt exists in the basket")

    # guest and member
    def editBasketQuantity(self, username, storename, productID, quantity):
            user: User = self.__getUserOrMember(username)
            answer = user.checkProductExistance(storename, productID) #answer is boolean
            if answer:
                store: Store = self.stores[storename]
                product = store.checkProductAvailability(productID, quantity)  # TODO:Amiel
                if product is not None:
                    user.edit_Product_Quantity(storename, productID, quantity)
                else:
                    raise Exception("Product is not available or quantity is higher than the stock")
            else:
                raise Exception("product does not exists in the basket")


    # guest and member
    def purchaseCart(self, username, cardnumber, cardusername, carduserID, carddate, backnumber):
        if self.__checkIfUserIsLoggedIn(username):
            existing_member: Member = self.members[username]
            # TODO: need to implement a lock system in here, so other users cant purchase at the same time.
            answer = existing_member.get_cart().checkAllItemsInCart()  # answer = set of baskets or none
            if answer is not None:
                for basket in answer:
                    price = basket.store.purchaseBasket(basket.products) # price of a single basket  #TODO:amiel
                    ExternalServices.pay(basket.store, cardnumber, cardusername, carduserID, carddate, backnumber, price) # TODO: Ari
            else:
                raise Exception("There is a problem with the items quantity or existance in the store")
        else:
            raise Exception("user is not logged in")








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



    def placeBid(self, username, store_name, offer):
        cur_member = self.members[username]
        self.__checkIfUserIsLoggedIn(username)



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

