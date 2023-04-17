import string

from ExternalServices import *
from MessageController import *
from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.Objects import User, Store, Access
from ProjectCode.Domain.Objects.ExternalObjects.PasswordValidation import PasswordValidation
from ProjectCode.Domain.Objects.UserObjects import Member, Admin, Guest
from TransactionHistory import *
from ExternalServices import *


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
        self.loadData()
        self.passwordValidator = PasswordValidation()

    def loadData(self):  # todo complete
        pass


# ------  users  ------ #

    #  Guests

    def exitTheSystem(self):
        pass

    #  Members
    def register(self, userName, password, email, birthDate, address):
        new_member = Member(userName, password, email, birthDate, address)

    def logInAsGuest(self):
        new_guest = Guest()

    def logInAsMember(self):
        pass

    def logOut(self):
        pass

    def getMemberPurchaseHistory(self):
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