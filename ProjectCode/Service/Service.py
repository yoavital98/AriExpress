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
            admins = TypedDict(str, Admin)
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

    def loginAsGuest(self):
        try:
            self.store_facade.loginAsGuest()
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

    def addToBasket(self,requesterID, storename, productname, quantity):
        try:
            self.store_facade.addToBasket()
        except ValueError:
            pass

    def removeFromBasket(self,requesterID, storename, productname):
        try:
            self.store_facade.removeFromBasket()
        except ValueError:
            pass

    def editBasketQuantity(self,requesterID, storename, productname, quantity):
        try:
            self.store_facade.editBasketQuantity()
        except ValueError:
            pass

    def purchaseCart(self, requesterID, cardnumber, cardusername, carduserID, carddate, backnumber):#TODO: for now lets assume only credit card(no paypal)
        try:
            self.store_facade.purchaseCart()
        except ValueError:
            pass

    def placeBid(self,requesterID, storename, productname, bid):
        try:
            self.store_facade.placeBid()
        except ValueError:
            pass

    def getStorePurchaseHistory(self, requesterID, storename):#TODO: username is demanded for validation of the request
        try:
            self.store_facade.getStorePurchaseHistory()
        except ValueError:
            pass

    # ------  Management  ------ #

    def openStore(self, username, store_name):
        try:
            cur_store = self.store_facade.openStore(username, store_name)
            return cur_store
        except Exception as e:
            self.error_log.error(f"Opening a store by {username} has failed.")
            return e

    def addNewProductToStore(self, username, storename , productname, categories, quantity, price):
        try:  # TODO check whether this product details are needed
            added_product = self.store_facade.addNewProductToStore(username, storename, productname, quantity, price, categories)
            return added_product
        except Exception as e:
            self.error_log.error(f"Adding a product by {username} has failed.")
            return e

    def removeProductFromStore(self, username, storename, product_id):
        try:
            deleted_product_id = self.store_facade.removeProductFromStore(username, storename, product_id)
            return deleted_product_id
        except Exception as e:
            self.error_log.error(f"Removing a product by {username} has failed.")
            return e


    def editProductOfStore(self, username, storename, **kwargs):  # TODO (opt) we will assume there's a dict that can say which features will change
        try:
            changed_product = self.store_facade.editProductOfStore(username, storename, **kwargs)
            return changed_product
        except Exception as e:
            self.error_log.error(f"Changing a product by {username} has failed.")
            return e

    def nominateStoreOwner(self, username, nominate_username, store_name):
        try:
            new_access = self.store_facade.nominateStoreOwner(username, nominate_username, store_name)
            return new_access
        except Exception as e:
            self.error_log.error(f"Nominating a store owner by {username} has failed.")
            return e

    def nominateStoreManager(self, username, nominate_username, store_name):
        try:
            new_access = self.store_facade.nominateStoreManager(username, nominate_username, store_name)
            return new_access
        except Exception as e:
            self.error_log.error(f"Nominating a store manager by {username} has failed.")
            return e

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

    def closeStore(self, username, storeName):
        try:
            closed_store_name = self.store_facade.closeStore(username, storeName)
            return closed_store_name
        except Exception as e:
            self.error_log.error(f"Closing a store by {username} has failed.")
            return e

    def getStaffInfo(self, username, storeName):
        try:
            store_accesses_dict = self.store_facade.getStaffInfo(username, storeName)
            return store_accesses_dict
        except Exception as e:
            self.error_log.error(f"Fetching store staff by {username} has failed.")
            return e

    def getStoreManagerPermissions(self, requesterID, storeName):
        try:
            self.store_facade.getStoreManagerPermissions()
        except ValueError:
            pass

