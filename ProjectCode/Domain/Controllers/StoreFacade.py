import string

import ProjectCode
from ProjectCode.Domain.Controllers.ExternalServices import *
from ProjectCode.Domain.Controllers.MessageController import *
from ProjectCode.Domain.Objects.UserObjects.Admin import *
from ProjectCode.Domain.Objects.ExternalObjects.PasswordValidation import PasswordValidation
from ProjectCode.Domain.Objects.UserObjects import Member, Admin, Guest
from ProjectCode.Domain.Controllers.TransactionHistory import *
from ProjectCode.Domain.Objects.Store import *
from ProjectCode.Domain.Objects.UserObjects.Guest import *
from ProjectCode.Domain.Objects.UserObjects.Member import *
from ProjectCode.Domain.Objects.AccessControl import *


class StoreFacade:
    def __init__(self):
        self.members = TypedDict(str, Member)    # dict of
        self.stores = TypedDict(str, Store)  # by id
        self.onlineGuests = TypedDict(str, Guest)
        # self.onlineUsers = TypedDict(str, Guest) --optional instead of onlineGuests--
        self.external_services = ExternalServices()
        self.message_controller = MessageController()
        self.transaction_history = TransactionHistory()
        self.accesses = TypedDict(str, AccessControl)  # optional TODO check key type
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
    def checkIfUserIsLoggedIn(self, username):  # public for testing
        if self.members.keys().__contains__(username):
            existing_member: Member = self.members[username]
            return existing_member.get_logged()
        else: #should never get here usually
            raise SystemError("user does not exists")

    def register(self, username, password, email):
        if not self.members.keys().__contains__(str(username)):
            password_validator = PasswordValidation()
            if password_validator.ValidatePassword(password):
                new_member = Member(username, password, email)
                self.members[str(username)] = new_member
                return new_member
        else:
            raise SystemError("This username is already in the system")



    def logInAsGuest(self):
        new_guest = Guest(self.nextEntranceID)
        self.onlineGuests[str(self.nextEntranceID)] = new_guest
        self.nextEntranceID += 1
        return new_guest

    def leaveAsGuest(self, EntranceID):
        if self.onlineGuests.keys().__contains__(str(EntranceID)):
            self.onlineGuests.__delitem__(str(EntranceID))
        else:
            raise SystemError("This entrance id doesn't belong to the online guests list")


    def logInAsMember(self, username , password):
        if self.members.keys().__contains__(username):
            existing_member: Member = self.members[username]
            password_validator = PasswordValidation()
            if password_validator.ConfirmePassword(password, existing_member.get_password()):
                existing_member.logInAsMember()
                return existing_member
            else:
                raise SystemError("username or password does not match")
        else:
            raise SystemError("username or password does not match")


    def logOut(self,username):
        if self.members.keys().__contains__(username):
            existing_member: Member = self.members[username]
            existing_member.logOff()
        else:
            pass
    def getMemberPurchaseHistory(self, username):
        if self.__checkIfUserIsLoggedIn(username):
            return TransactionHistory.get_User_Transactions(username)
        else:
            raise SystemError("username isn't logged in")


    def getBasket(self,username, storename):
        existing_member: Member = self.members[username]
        return existing_member.get_cart(username).get_baskets()[storename]

    def getCart(self,username):
        if self.__checkIfUserIsLoggedIn(username):
            existing_member: Member = self.members[username]
            return existing_member.get_cart()
        else:
            raise SystemError("username isn't logged in")

# guest and member
    def addToBasket(self, username, storename, productID, quantity): # this function should first go to the store and check if we can even add to the basket
        self.__systemCheck()
        user: User = self.__getUserOrMember(username)
        store: Store = self.stores[storename]
        product = store.checkProductAvailability(productID, quantity)
        if product is not None:
            user.add_to_cart(username, storename, productID, product, quantity)
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
        if not cur_member:
            raise Exception("The user is not a member")
        cur_store = Store(store_name)
        new_access = AccessControl(cur_member, cur_store)
        cur_member.accesses[store_name] = new_access
        cur_store.setFounder(cur_member.get_username(), new_access)
        self.stores[store_name] = cur_store
        return cur_store


    def addNewProductToStore(self, username, store_name, name, quantity, price, categories):
        cur_store: Store = self.stores[store_name]
        if cur_store is None:
            raise Exception("No such store exists")
        #cur_member: Member = self.members[str(requester_id)]
        access = None # todo what
        new_product = cur_store.addProduct(access, name, quantity, price, categories)
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
            nominated_access = AccessControl(cur_store,self.members[nominated_username])
            self.members[nominated_access].accesses[store_name] = nominated_access
        nominated_modified_access = cur_store.setAccess(nominated_access, requester_username, nominated_username, isOwner=True)
        return nominated_modified_access

    def nominateStoreManager(self, requester_username, nominated_username, store_name):
        cur_store: Store = self.stores[store_name]
        if cur_store is None:
            raise Exception("No such store exists")
        nominated_access = self.members[nominated_username].accesses[store_name]
        if nominated_access is None:
            nominated_access = AccessControl(cur_store, self.members[nominated_username])
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

