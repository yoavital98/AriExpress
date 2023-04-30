from ariExpressDjango.ProjectCode.Domain.Controllers import StoreFacade
import logging


class Service:
    def __init__(self):
        self.store_facade = StoreFacade()
    # ------  admin  ------ #
    def openTheSystem(self, username):
        try:
            self.store_facade.openSystem(username)
            logging.info("AriExpress is now open and running")
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e


    def addAdmin(self, username, newAdminName, newPassword, newEmail):
        try:
            admin =  self.store_facade.addAdmin(username, newAdminName, newPassword, newEmail)
            logging.info("admin has been added successfully")
            return admin
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e


    # def loadAdminsFromDB(self):
    #     try:
    #         admins = TypedDict(str, Admin)
    #         ### let's assume we tried to take all the admins from the database
    #         if len(admins) == 0:#TODO: just for this version so we will have an Admin
    #             admins["007"] = Admin("JamesBond", "TATAKAE", "yoavital98@gmail.com")
    #         return admins
    #     except ValueError:
    #         pass


    # ------  users  ------ #
    #  Guests

    def exitTheSystem(self): #TODO: same as in StoreFacade todo task - need to change
        try:
            self.store_facade.exitTheSystem()
        except ValueError:
            pass

    def leaveAsGuest(self, guest):
        try:
            self.store_facade.leaveAsGuest(guest)
        except ValueError:
            pass

    def loginAsGuest(self):
        try:
            guest = self.store_facade.loginAsGuest()
            logging.info("logged in as guest successfully")
            return guest
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    #  Members
    def register(self, user_name, password, email):
        try:
            member = self.store_facade.register(user_name, password, email)
            logging.info("user has registered successfully")
            return member
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def logIn(self, username, password):  # todo no responses
        try:
            member = self.store_facade.logInAsMember(username, password)
            logging.info(f"Welcome {str(username)}")
            return Smember(member)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    # def logIn(self, username, password):  # todo responses from service to gui
    #     try:
    #         member = self.store_facade.logInAsMember(username, password)
    #         logging.info(f"Welcome {str(username)}")
    #         return Response(member.toJson(), True)
    #     except Exception as e:
    #         logging.error(f"An error occurred: {str(e)}")
    #         return Response(e, False)
    # def logIn(self, username, password):  # todo responses from domain to service
    #     memberResponse = self.store_facade.logInAsMember(username, password)
    #     if memberResponse.getStatus():
    #         member = memberResponse.getReturnValue()
    #         logging.info(f"Welcome {str(username)}")
    #         return member.toJson()
    #     else:
    #         e = memberResponse.getReturnValue()
    #         logging.error(f"An error occurred: {str(e)}")
    #         return e

    def logOut(self, username):
        try:
            self.store_facade.logOut(username)
            logging.info(f"Logged out successfully, goodbye {str(username)}")
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def getMemberPurchaseHistory(self, username):
        try:
            purchase_history = self.store_facade.getMemberPurchaseHistory(username)
            logging.info(f"fetching {str(username)} purchase history")
            return purchase_history
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    # ------  stores  ------ #

    def getStores(self):
        try:
            stores = self.store_facade.getStores()
            logging.info(f"fetching all stores in the system")
            return stores
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def getProductsByStore(self, storename):
        try:
            products = self.store_facade.getProductsByStore(storename)
            logging.info(f"fetching all products in store {str(storename)}")
            return products
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def getProduct(self, storename, product_id):
        try:
            product = self.store_facade.getProduct(storename, product_id)
            logging.info(f"fetching product num {str(product_id)} in store {str(storename)}")
            return product
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def productSearchByName(self, productName):  # and keywords
        try:
            results = self.store_facade.productSearchByName(productName)
            logging.info(f"fetching all the products with keyname {str(productName)}")
            return results
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def productSearchByCategory(self, categoryName):#TODO: probably each store will have its products catagorized
        try:#TODO: need to create an enum set of categories, shopowners does not create categories.!!!!!!!
            results = self.store_facade.productSearchByCategory(categoryName)
            logging.info(f"fetching all the products within the category {str(categoryName)}")
            return results
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def productFilterByFeatures(self, featuresDict):    #TODO (opt) we will assume there's a dict that can say which features will be searched
        try:
            products = self.store_facade.productFilterByFeatures(featuresDict)
            logging.info(f"fetching all the products within the feature {str(featuresDict)}")
            return products
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def getBasket(self, username, storename):
        try:
            basket = self.store_facade.getBasket(username, storename)
            logging.info(f"fetching the basket of store {str(storename)}")
            return basket
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def getCart(self, username):
        try:
            cart = self.store_facade.getCart(username)
            logging.info(f"fetching the cart of {str(username)}")
            return cart
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def addToBasket(self, username, storename, productID, quantity):
        try:
            self.store_facade.addToBasket(username, storename, productID, quantity)
            logging.info(f"Item has been added to the cart successfully")
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def removeFromBasket(self, username, storename, productID):
        try:
            answer = self.store_facade.removeFromBasket(username, storename, productID)
            logging.info(f"Item has been removed from the cart successfully")
            return answer
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def editBasketQuantity(self, username, storename, product_id, quantity):
        try:
            self.store_facade.editBasketQuantity(username, storename, product_id, quantity)
            logging.info(f"Item with id {str(product_id)} has been edited in the basket with {str(quantity)} quantity")
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def purchaseCart(self, user_name, card_number, card_user_name, card_user_ID, card_date, back_number):#TODO: for now lets assume only credit card(no paypal)
        try:
            flag = self.store_facade.purchaseCart(user_name, card_number, card_user_name, card_user_ID, card_date, back_number)
            logging.info("Successful purchase")
            return flag
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def placeBid(self, username, storename, offer, productID, quantity):
        try:
            bid = self.store_facade.placeBid(username, storename, offer, productID, quantity)
            logging.info(f"bid for item number {str(productID)} from the store {str(storename)} has been placed with {str(offer)}")
            return bid
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def getAllBidsFromUser(self, username):
        try:
            bids = self.store_facade.getAllBidsFromUser(username)
            logging.info(f"fetching all the Bids of user {str(username)}")
            return bids
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def purchaseConfirmedBid(self, username, storename, bid_id, card_number, card_user_name, card_user_ID, card_date,
                             back_number):
        try:
            self.store_facade.purchaseConfirmedBid(username, storename, bid_id, card_number, card_user_name, card_user_ID, card_date,
                             back_number)
            logging.info(f"Bid id: {str(bid_id)} has been purchased successfully")
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def approveBid(self, username, storename, bid_id):
        try:
            approved_bid = self.store_facade.approveBid(username, storename, bid_id)
            logging.info(f"Bid id: {str(bid_id)} has been approved successfully")
            return approved_bid
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def rejectBid(self, username, storename, bid_id):
        try:
            rejected_bid = self.store_facade.rejectBid(username, storename, bid_id)
            logging.info(f"Bid id: {str(bid_id)} has been rejected successfully")
            return rejected_bid
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def sendAlternativeOffer(self, username, storename, bid_id, alternate_offer):
        try:
            alt_bid = self.store_facade.sendAlternativeBid(username, storename, bid_id, alternate_offer)
            logging.info(f"Bid id: {str(bid_id)} an alternative offer has been offered")
            return alt_bid
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def addAuction(self, username, storename, product_id, starting_price, duration):
        try:
            new_auc = self.store_facade.addAuction(username, storename, product_id, starting_price, duration)
            logging.info(f"Auction id: {str(new_auc.get_auction_id())} an auction has been created")
            return new_auc
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def placeOfferInAuction(self, username, storename, auction_id, offer):
        try:
            auc = self.store_facade.addAuction(username, storename, auction_id, offer)
            logging.info(f"an offer has been placed on auction id: {str(auc.get_auction_id())}")
            return auc
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def addLottery(self):
        pass

    def getStorePurchaseHistory(self, username, storename):#TODO: username is demanded for validation of the request
        try:
            transactions = self.store_facade.getStorePurchaseHistory(username, storename)
            logging.info(f"transactions of stores has been fetched successfully")
            return transactions
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    # ------  Management  ------ #

    def openStore(self, username, store_name):
        try:
            cur_store = self.store_facade.openStore(username, store_name)
            logging.info(f"store named {str(store_name)} has been created successfully")
            return cur_store
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def addNewProductToStore(self, username, storename , productname, categories, quantity, price):
        try:  # TODO check whether this product details are needed
            added_product = self.store_facade.addNewProductToStore(username, storename, productname, quantity, price, categories)
            logging.info(f"product named {str(productname)} has been added to the store {str(storename)} successfully")
            return added_product
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e


    def removeProductFromStore(self, username, storename, product_id):
        try:
            deleted_product_id = self.store_facade.removeProductFromStore(username, storename, product_id)
            logging.info(f"product id {str(product_id)} has been removed from the store {str(storename)} successfully")
            return deleted_product_id
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e


    def editProductOfStore(self, username, storename, **kwargs):  # TODO (opt) we will assume there's a dict that can say which features will change
        try:
            changed_product = self.store_facade.editProductOfStore(username, storename, **kwargs)
            return changed_product
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def nominateStoreOwner(self, username, nominate_username, store_name):
        try:
            new_access = self.store_facade.nominateStoreOwner(username, nominate_username, store_name)
            logging.info(f"user {str(nominate_username)} has been nominated to owner at store {str(store_name)}")
            return new_access
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def nominateStoreManager(self, username, nominate_username, store_name):
        try:
            new_access = self.store_facade.nominateStoreManager(username, nominate_username, store_name)
            logging.info(f"user {str(nominate_username)} has been nominated to Manager at store {str(store_name)}")
            return new_access
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def addPermissionForManager(self, requesterID, nominatedID, permission):
        try:
            self.store_facade.addPermissionsForManager()
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def editPermissionsForManager(self, requesterID, nominatedID, permission):  # TODO still don't know the implementation
        try:
            self.store_facade.editPermissionsForManager()
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def closeStore(self, username, storename):
        try:
            closed_store_name = self.store_facade.closeStore(username, storename)
            logging.info(f"store {str(storename)} has been closed")
            return closed_store_name
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def getStaffInfo(self, username, storename):
        try:
            store_accesses_dict = self.store_facade.getStaffInfo(username, storename)
            logging.info(f"fetching store {str(storename)} staff info")
            return store_accesses_dict
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e

    def getStoreManagerPermissions(self, requesterID, storeName):
        try:
            self.store_facade.getStoreManagerPermissions()
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return e
        
    def getDjangoTestData(self):
        return {"Flexus", "flextronics@mail.com", True}

