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
        self.nextEntranceID = 0
        self.next_store_id = 0
        self.loadData()
        self.passwordValidator = PasswordValidation()

    def loadData(self):  # todo complete
        pass


# ------  users  ------ #

    #  Guests

    def exitTheSystem(self):
        pass

    #  Members
    def register(self, username, password, email):
        if not self.members.keys().__contains__(str(username)):
            password_validator = PasswordValidation()
            if password_validator.ValidatePassword(password):
                new_member = Member(username, password, email) #TODO:why Member is not callable?
                self.members[str(username)] = new_member
                return new_member
        else:
            pass



    def logInAsGuest(self):
        new_guest = Guest(self.nextEntranceID) #TODO: why guest isnt callable?
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
            existing_member:Member = self.members[username]
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
    def getMemberPurchaseHistory(self):
        pass
    def getBasket(self):
        pass

    def getCart(self):
        pass

    def addToBasket(self):
        pass

    def removeFromBasket(self):
        pass

    def editBasketQuantity(self):
        pass

    def purchaseCart(self):
        pass

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
        cur_memeber = self.members.get(username)
        if cur_memeber is None:
            raise Exception("The user is not a member")
        self.next_store_id += 1
        cur_store = Store(store_name)
        # TODO: verify that member have a accesses field and add the access to it
        new_access = Access(cur_memeber, cur_store)
        cur_store.setFounder(cur_memeber.user_name, new_access)
        self.stores[store_name] = cur_store
        return cur_store


    def addNewProductToStore(self, requester_id, store_name, name, quantity, price, categories):
        cur_store: Store = self.stores[store_name]
        #cur_member: Member = self.members[str(requester_id)]
        new_product = cur_store.addProduct(requester_id, name, quantity, price, categories)
        return new_product

    def removeProductFromStore(self):
        pass

    def editProductOfStore(self):
        pass

    def nominateStoreOwner(self):
        pass

    def nominateStoreManager(self):
        pass

    def addPermissionsForManager(self):
        pass

    def editPermissionsForManager(self):
        pass

    def closeStore(self):
        pass

    def getStaffInfo(self):
        pass

    def getStoreManagerPermissions(self):
        pass

