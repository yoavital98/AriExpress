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
from ProjectCode.Domain.Objects.Basket import *


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
            if ExternalServices.ValidatePassword(password):
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
            if ExternalServices.ConfirmePassword(password, existing_member.get_password()):
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

    def addToBasket(self, username, storename, productID, quantity): # this function should first go to the store and check if we can even add to the basket
        if self.__checkIfUserIsLoggedIn(username):
            existing_member: Member = self.members[username]
            store: Store = self.stores[storename]
            product = store.checkProductAvailability(productID, quantity)  #TODO: amiel needs to implement that method
            if product is not None:
              existing_member.get_cart().add_Product(storename, productID, product, quantity)
            else:
               raise Exception("Product is not available or quantity is higher than the stock")


            existing_member.add_to_cart(storename, 0, 0, quantity)
        else:
            raise Exception("user is not logged in")

    def removeFromBasket(self, username, storename, productID):
        if self.__checkIfUserIsLoggedIn(username):
            existing_member: Member = self.members[username]
            remove_success = existing_member.get_cart().removeFromBasket(storename, productID)
            if remove_success:
                return remove_success
            else:
                raise Exception("there was a problem with removing the item or either the item doesnt exists in the basket")
        else:
            raise Exception("user is not logged in")
    def editBasketQuantity(self, username, storename, productID, quantity):
        if self.__checkIfUserIsLoggedIn(username):
            existing_member: Member = self.members[username]
            answer = existing_member.get_cart().checkProductExistance(storename, productID) #answer is boolean
            if answer:
                store: Store = self.stores[storename]
                product = store.checkProductAvailability(productID, quantity)
                if product is not None:
                    existing_member.get_cart().add_Product(storename, productID, product, quantity)
                else:
                    raise Exception("Product is not available or quantity is higher than the stock")
            else:
                raise Exception("product does not exists in the basket")
        else:
            raise Exception("user is not logged in")


    def purchaseCart(self, username, cardnumber, cardusername, carduserID, carddate, backnumber):
        if self.__checkIfUserIsLoggedIn(username):
            existing_member: Member = self.members[username]
            #TODO:  need to implement a lock system in here, so other users cant purchase at the same time.
            answer = existing_member.get_cart().checkAllItemsInCart()  # answer = set of baskets or none
            if answer is not None:
                for basket in answer:
                    price = basket.store.purchaseBasket(basket.products) # price of a single basket  #TODO:amiel
                    ExternalServices.pay(basket.store, cardnumber, cardusername, carduserID, carddate, backnumber, price) #TODO: Ari
            else:
                raise Exception("There is a problem with the items quantity or existance in the store")
        else:
            raise Exception("user is not logged in")








    # ------  stores  ------ #

    def getStores(self):
        pass

    def getProductsByStore(self):
        pass

    def getProduct(self):
        pass

    def productSearchByName(self):  # and keywords
        pass

    def productSearchByCategory(self):
        pass

    def productFilterByFeatures(self):
        pass



    def placeBid(self):
        pass

    def getStorePurchaseHistory(self):
        pass

    # ------  Management  ------ #


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

