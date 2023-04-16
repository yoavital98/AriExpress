from ProjectCode.Domain.Controllers.StoreFacade import *
import logging


class Service:  # TODO change ValueError to relevant ones
    def __init__(self, logging):
        self.admins = self.loadAdminsFromDB()
        self.store_facade = None # StoreFacade() TODO decide how we want to open teh facade




    # ------  admin  ------ #
    def openTheSystem(self, requesterID):
        try:
            if self.admins.keys().__contains__(requesterID):  # check if admin
                self.store_facade = StoreFacade()  # activates loadData in constructor
            else:
                raise SystemError("open-the-system requester isn't admin")
        except SystemError:
            logging.getLogger().error(SystemError)

    def addAdmin(self, requesterID, newAdminID, newPassword, newEmail):  # TODO we will assume the requesting admin fills himself the new admin details
        try:
            if self.admins.keys().__contains__(requesterID):  # check if admin
                self.admins[newAdminID] = Admin(newAdminID, newPassword, newEmail)
            raise SystemError("add-admin requester isn't admin")
        except SystemError:
            logging.getLogger().error(SystemError)

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
            self.store_facade.register()
        except ValueError:
            pass

    def logIn(self,username, password):
        try:
            self.store_facade.logIn()
        except ValueError:
            pass

    def logOut(self,username):
        try:
            self.store_facade.logOut()
        except ValueError:
            pass

    def getMemberPurchaseHistory(self,username):
        try:
            self.store_facade.getMemberPurchaseHistory()
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

    def productFilterByFeatures(self):#TODO: need to think of a functionality
        try:
            self.store_facade.productFilterByFeatures()
        except ValueError:
            pass

    def getBasket(self,username, storename):
        try:
            self.store_facade.getBasket()
        except ValueError:
            pass

    def getCart(self,username):
        try:
            self.store_facade.getCart()
        except ValueError:
            pass

    def addToBasket(self,username, storename, productname, quantity):
        try:
            self.store_facade.addToBasket()
        except ValueError:
            pass

    def removeFromBasket(self,username, storename, productname):
        try:
            self.store_facade.removeFromBasket()
        except ValueError:
            pass

    def editBasketQuantity(self,username, storename, productname, quantity):
        try:
            self.store_facade.editBasketQuantity()
        except ValueError:
            pass

    def purchaseCart(self, username, cardnumber, cardusername, carduserID, carddate, backnumber):#TODO: for now lets assume only credit card(no paypal)
        try:
            self.store_facade.purchaseCart()
        except ValueError:
            pass

    def placeBid(self,username, storename, productname, bid):
        try:
            self.store_facade.placeBid()
        except ValueError:
            pass

    def getStorePurchaseHistory(self, username, storename):#TODO: username is demanded for validation of the request
        try:
            self.store_facade.getStorePurchaseHistory()
        except ValueError:
            pass

    # ------  Management  ------ #

    def openStore(self,username):
        try:
            self.store_facade.openStore()
        except ValueError:
            pass

    def addNewProductToStore(self,username, storename , productname, productcategory, productquantity, productprice):
        try:
            self.store_facade.addNewProductToStore()
        except ValueError:
            pass

    def removeProductFromStore(self):
        try:
            self.store_facade.removeProductFromStore()
        except ValueError:
            pass

    def editProductOfStore(self):
        try:
            self.store_facade.editProductOfStore()
        except ValueError:
            pass

    def nominateStoreOwner(self):
        try:
            self.store_facade.nominateStoreOwner()
        except ValueError:
            pass

    def nominateStoreManager(self):
        try:
            self.store_facade.nominateStoreManager()
        except ValueError:
            pass

    def addPermissionsForManager(self):
        try:
            self.store_facade.addPermissionsForManager()
        except ValueError:
            pass

    def editPermissionsForManager(self):
        try:
            self.store_facade.editPermissionsForManager()
        except ValueError:
            pass

    def closeStore(self):
        try:
            self.store_facade.closeStore()
        except ValueError:
            pass

    def getStaffInfo(self):
        try:
            self.store_facade.getStaffInfo()
        except ValueError:
            pass

    def getStoreManagerPermissions(self):
        try:
            self.store_facade.getStoreManagerPermissions()
        except ValueError:
            pass

