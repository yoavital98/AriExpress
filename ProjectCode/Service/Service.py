from ProjectCode.Domain.Controllers.StoreFacade import *


class Service:
    def __init__(self):
        self.store_facade = StoreFacade()  # activates loadData in constructor

    # ------  users  ------ #

    #  Guests
    def enterTheSystem(self):
        pass

    def exitTheSystem(self):
        pass

    #  Members
    def register(self):
        pass

    def logIn(self):
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



