import string

import ProjectCode
from ProjectCode.Domain.Controllers.ExternalServices import *
from ProjectCode.Domain.Controllers.MessageController import *
from ProjectCode.Domain.Objects import User, Store, Access
from ProjectCode.Domain.Objects.Bid import *
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

        self.admins = TypedDict(str, Admin)  # dict of admins
        self.members = TypedDict(str, Member)    # dict of members
        self.onlineGuests = TypedDict(str, Guest)  # dict of users
        self.stores = TypedDict(str, Store)  # dict of stores
        self.external_services = ExternalServices()  # external services
        self.message_controller = MessageController()  # Messanger
        self.transaction_history = TransactionHistory()  # Transactions log
        self.accesses = TypedDict(str, Access)  # optional TODO check key type
        self.nextEntranceID = 0  # guest ID counter
        self.cart_ID_Counter = 0  # cart counter
        self.bid_id_counter = 0  # bid counter
        self.loadData()
        self.SystemStatus = False  # True = System on, False = System off
        first_admin: Admin = Admin("Ari", "123", "arioshryz@gmail.com")
        self.admins["Ari"] = first_admin

# ------  System  ------ #
    def loadData(self):  # todo complete
        pass

    def __systemCheck(self):
        if self.SystemStatus:
            pass
        else:
            raise Exception("system is not online")

# ------  users  ------ #
    #  Guests

    def exitTheSystem(self):
        pass

    def __getAdmin(self, user_name):
        if self.admins.keys().__contains__(user_name):
            return self.admins[user_name]
        else:
            raise Exception("admin does not exists")

    #  Members

    def __checkIfUserIsLoggedIn(self, user_name):
            existing_member: Member = self.members[user_name]
            if existing_member.get_logged():
                return True
            else: #should never get here usually
                raise Exception("user is not logged in")

    def __getUserOrMember(self,user_name):
        if self.members.keys().__contains__(user_name):
            if self.__checkIfUserIsLoggedIn(user_name):
                return self.members[user_name]
            else:
                raise Exception("user is not logged in")
        else:
            if self.onlineGuests.keys().__contains__(user_name):
                return self.onlineGuests.get(user_name)
            else:
                raise Exception("user is not guest nor a member")

    def register(self, user_name, password, email):
        self.__systemCheck()
        if not self.members.keys().__contains__(str(user_name)):
            if ExternalServices.ValidatePassword(password):
                new_member = Member(user_name, password, email, self.cart_ID_Counter)
                self.cart_ID_Counter += 1
                self.members[str(user_name)] = new_member

                return new_member
        else:
            raise SystemError("This username is already in the system")

    # only guests
    def logInAsGuest(self):
        self.__systemCheck()
        new_guest = Guest(self.nextEntranceID, self.cart_ID_Counter)
        self.cart_ID_Counter += 1
        self.onlineGuests[str(self.nextEntranceID)] = new_guest
        self.nextEntranceID += 1
        return new_guest

    # only guests

    def leaveAsGuest(self, EntranceID):
        self.__systemCheck()
        if self.onlineGuests.keys().__contains__(str(EntranceID)):
            self.onlineGuests.__delitem__(EntranceID)

    #  only members
    def logInAsMember(self, username , password):
        self.__systemCheck()
        if self.admins.keys().__contains__(username):
            return self.logInAsAdmin(username, password)
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
        self.__systemCheck()
        if self.members.keys().__contains__(username):
            existing_member: Member = self.members[username]
            existing_member.logOut()

    #  only members

    def getMemberPurchaseHistory(self, username):
        self.__systemCheck()
        if self.__checkIfUserIsLoggedIn(username):
            return TransactionHistory.get_User_Transactions(username)

    # guest and member
    def getBasket(self, username, storename):
        self.__systemCheck()
        user = self.__getUserOrMember(username)
        requested_basket = user.get_Basket(storename)
        return requested_basket

    # guest and member
    def getCart(self,username):
        self.__systemCheck()
        user: User = self.__getUserOrMember(username)
        requested_cart = user.get_cart()
        return requested_cart

    # guest and member
    def addToBasket(self, username, storename, productID, quantity): # this function should first go to the store and check if we can even add to the basket
        self.__systemCheck()
        user: User = self.__getUserOrMember(username)
        store: Store = self.stores[storename]
        product = store.checkProductAvailability(productID, quantity)
        if product is not None:
            user.add_to_cart(storename, productID, product, quantity)
        else:
            raise Exception("Product is not available or quantity is higher than the stock")

    # guest and member
    def removeFromBasket(self, username, storename, productID):
        self.__systemCheck()
        user: User = self.__getUserOrMember(username)
        remove_success = user.removeFromBasket(storename, productID)
        if remove_success:
            return remove_success
        else:
            raise Exception("there was a problem with removing the item or either the item doesnt exists in the basket")

    # guest and member
    def editBasketQuantity(self, username, storename, productID, quantity):
        self.__systemCheck()
        user: User = self.__getUserOrMember(username)
        answer = user.checkProductExistance(storename, productID) #answer is boolean
        if answer:
            store: Store = self.stores[storename]
            product = store.checkProductAvailability(productID, quantity)
            if product is not None:
                user.edit_Product_Quantity(storename, productID, quantity)
            else:
                raise Exception("Product is not available or quantity is higher than the stock")
        else:
            raise Exception("product does not exists in the basket")

    # guest and member
    def purchaseCart(self, user_name, card_number, card_user_name, card_user_ID, card_date, back_number):
        self.__systemCheck()
        overall_price = 0  # overall price for the user
        user: User = self.__getUserOrMember(user_name)  # getting the user
        stores_to_products = TypedDict(str, tuple)  # the final dictionary for the UserTransaction
        # TODO: need to implement a lock system in here, so other users cant purchase at the same time.
        answer = user.get_cart().checkAllItemsInCart()  # answer = set of baskets or none
        if answer is not None:
            for basket in answer:
                products: set = basket.getProductsAsTuples()
                price = basket.purchaseBasket()  # price of a single basket  #TODO:amiel
                ExternalServices.pay(basket.store, card_number, card_user_name, card_user_ID, card_date, back_number, price) # TODO: Ari
                TransactionHistory.addNewStoreTransaction(user_name,) #make a new transaction and add it to the store history and user history
                stores_to_products[basket.store.store_name] = products  # gets the
                overall_price += price
            if self.members.keys().__contains__(user_name):
                TransactionHistory.addNewUserTransaction(user_name,stores_to_products, overall_price)
        else:
            raise Exception("There is a problem with the items quantity or existance in the store")

    def placeBid(self,username, storename, offer, productID, quantity):
        existing_member = None
        if self.members.keys().__contains__(username):
            existing_member: Member = self.members[username]
            if not existing_member.get_logged():
                raise Exception("user isnt logged in")
        else:
            raise Exception("user is not valid")
        bid: Bid = Bid(self.bid_id_counter, username, storename, offer, productID, quantity)
        self.bid_id_counter += 1
        existing_member.addBidToBasket(bid)  #TODO:Ari
        store: Store = self.stores[storename]
        store.requestBid(bid)  #TODO:amiel!!



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

    # ------  Admins  ------ #
    def logInAsAdmin(self,username, password):
        if self.admins.keys().__contains__(username):
            existing_admin: Admin = self.admins[username]
            if ExternalServices.ConfirmePassword(password, existing_admin.get_password()):
                existing_admin.logInAsAdmin()
                return existing_admin
            else:
                raise Exception("admin name or password does not match")
        else:
            raise Exception("admin name or password does not match")

    def logInAsAdmin(self, user_name):
        if self.admins.keys().__contains__(user_name):
            existing_admin: Admin = self.members[user_name]
            existing_admin.logOff()

    def openSystem(self, admin_name):
        existing_admin: Admin = self.__getAdmin(admin_name)
        if existing_admin.get_logged():
            self.SystemStatus = True

    def messageAsAdmin(self, admin_name, message, receiver_user_name):
        pass

    def closeStoreAsAdmin(self, admin_name, store_name):
        pass
