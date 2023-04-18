import string

from ExternalServices import *
from MessageController import *
from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.Objects import User, Store, Access
from ProjectCode.Domain.Objects.Cart import Cart
from ProjectCode.Domain.Objects.ExternalObjects.PasswordValidation import PasswordValidation
from ProjectCode.Domain.Objects.UserObjects import Member, Admin, Guest
from TransactionHistory import *
from ExternalServices import *
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
            raise SystemError("user is not logged in")

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


    def getBasket(self,username, storename):
        if self.__checkIfUserIsLoggedIn(username):
            existing_member: Member = self.members[username]
            existing_member.get_cart()

    def getCart(self,username):
        pass

    def addToBasket(self): # this function should first go to the store and check if we can even add to the basket
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

    def openStore(self):
        pass

    def addNewProductToStore(self):
        pass

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

