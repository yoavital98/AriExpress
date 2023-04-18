from ProjectCode.Domain.Controllers.StoreFacade import *
import logging


class Service:  # TODO change ValueError to relevant ones
    def __init__(self, logging):
        self.admins = self.loadAdminsFromDB()
        self.store_facade = None # StoreFacade() TODO decide how we want to open teh facade
        self.error_log = logging.getLogger()
        self.event_log = logging.getLogger()




    # ------  admin  ------ #
    def openTheSystem(self, requesterID):
        try:
            if self.admins.keys().__contains__(requesterID):  # check if admin
                self.store_facade = StoreFacade()  # activates loadData in constructor
            else:
                raise SystemError("open-the-system requester isn't admin")
        except SystemError:
            pass

    def addAdmin(self, requesterID, newAdminID, newPassword, newEmail):  # TODO we will assume the requesting admin fills himself the new admin details
        try:
            if self.admins.keys().__contains__(requesterID):  # check if admin
                self.admins[newAdminID] = Admin(newAdminID, newPassword, newEmail)
            raise SystemError("add-admin requester isn't admin")
        except SystemError:
            pass

    def loadAdminsFromDB(self):
        try:
            admins = TypedDict(string, Admin)
            ### let's assume we tried to take all the admins from the database
            if len(admins) == 0:#TODO: just for this version so we will have an Admin
                admins["007"] = Admin("JamesBond", "TATAKAE", "yoavital98@gmail.com")
            return admins
        except ValueError:
            pass

    # ------  users  ------ #

    #  Guests

    def exitTheSystem(self):
        try:
            self.store_facade.exitTheSystem()
        except ValueError:
            pass

    #  Members
    def register(self, user_name, password, email):
        try:
            self.store_facade.register(user_name, password, email)
        except ValueError:
            pass

    def logIn(self,username, password):
        try:
            self.store_facade.logIn(username, password)
        except ValueError:
            pass

    def logOut(self,username):
        try:
            self.store_facade.logOut(username)
        except ValueError:
            pass

    def getMemberPurchaseHistory(self, username):
        try:
            self.store_facade.getMemberPurchaseHistory(username)
        except ValueError:
            pass

    # ------  stores  ------ #

    def getStores(self):
        try:
            self.store_facade.getStores()
        except ValueError:
            pass

    def getProductsByStore(self, storename):
        try:
            self.store_facade.getProductsByStore()
        except ValueError:
            pass

    def getProduct(self, storename, productName):
        try:
            self.store_facade.getProduct()
        except ValueError:
            pass

    def productSearchByName(self, productName):  # and keywords
        try:
            self.store_facade.productSearchByName()
        except ValueError:
            pass

    def productSearchByCategory(self, categoryName):#TODO: probably each store will have its products catagorized
        try:#TODO: need to create an enum set of categories, shopowners does not create categories.!!!!!!!
            self.store_facade.productSearchByCategory()
        except ValueError:
            pass

    def productFilterByFeatures(self, featuresDict):# TODO (opt) we will assume there's a dict that can say which features will be searched
        try:
            self.store_facade.productFilterByFeatures()
        except ValueError:
            pass

    def getBasket(self, username, storename):
        try:
            self.store_facade.getBasket()
        except ValueError:
            pass

    def getCart(self, username):
        try:
            self.store_facade.getCart()
        except ValueError:
            pass

    def addToBasket(self, username, storename, productname, quantity):
        try:
            self.store_facade.addToBasket(username, storename, productname, quantity)
        except ValueError:
            pass

    def removeFromBasket(self, username, storename, productname):
        try:
            self.store_facade.removeFromBasket(username, storename, productname)
        except ValueError:
            pass

    def editBasketQuantity(self, username, storename, productname, quantity):
        try:
            self.store_facade.editBasketQuantity(username, storename, productname, quantity)
        except ValueError:
            pass

    def purchaseCart(self, username, cardnumber, cardusername, carduserID, carddate, backnumber):#TODO: for now lets assume only credit card(no paypal)
        try:
            self.store_facade.purchaseCart(username, cardnumber, cardusername, carduserID, carddate, backnumber)
        except ValueError:
            pass

    def placeBid(self, username, storename, productname, bid):
        try:
            self.store_facade.placeBid(username, storename, productname, bid)
        except ValueError:
            pass

    def getStorePurchaseHistory(self, username, storename):#TODO: username is demanded for validation of the request
        try:
            self.store_facade.getStorePurchaseHistory(username, storename)
        except ValueError:
            pass

    # ------  Management  ------ #

    def openStore(self, username):
        try:
            self.store_facade.openStore(username)
        except ValueError:
            pass

    def addNewProductToStore(self, username, storename , productname, productcategory, productquantity, productprice):
        try:  # TODO check whether this product details are needed
            self.store_facade.addNewProductToStore(username, storename, productname, productcategory, productquantity, productprice)
        except ValueError:
            pass

    def removeProductFromStore(self,requesterID, storename , productname):
        try:
            self.store_facade.removeProductFromStore()
        except ValueError:
            pass

    def editProductOfStore(self,requesterID, storename , productname, changesDict):  # TODO (opt) we will assume there's a dict that can say which features will change
        try:
            self.store_facade.editProductOfStore()
        except ValueError:
            pass

    def nominateStoreOwner(self, requesterID, nominatedID):
        try:
            self.store_facade.nominateStoreOwner()
        except ValueError:
            pass

    def nominateStoreManager(self, requesterID, nominatedID):
        try:
            self.store_facade.nominateStoreManager()
        except ValueError:
            pass

    def addPermissionForManager(self, requesterID, nominatedID, permission):
        try:
            self.store_facade.addPermissionsForManager()
        except ValueError:
            pass

    def editPermissionsForManager(self, requesterID, nominatedID, permission):  # TODO still don't know the implementation
        try:
            self.store_facade.editPermissionsForManager()
        except ValueError:
            pass

    def closeStore(self, requesterID, storeName):
        try:
            self.store_facade.closeStore()
        except ValueError:
            pass

    def getStaffInfo(self, requesterID, storeName):
        try:
            self.store_facade.getStaffInfo()
        except ValueError:
            pass

    def getStoreManagerPermissions(self, requesterID, storeName):
        try:
            self.store_facade.getStoreManagerPermissions()
        except ValueError:
            pass

