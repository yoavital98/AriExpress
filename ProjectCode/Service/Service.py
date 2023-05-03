from ProjectCode.Domain.StoreFacade import StoreFacade
import logging

from ProjectCode.Service.MemoryHandler import MemoryHandler
from ProjectCode.Service.Response import Response


class Service:
    def __init__(self):
        self.store_facade = StoreFacade()
        self.logger = logging.getLogger(__name__)
        self.modifyLogger()

    # ------  logger  ------ #
    def modifyLogger(self):
        # create custom handler with a higher log level for success messages
        success_handler = MemoryHandler(logging.INFO)
        # create custom handler with a higher log level for error messages
        error_handler = MemoryHandler(logging.ERROR)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        success_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)
        # add the handlers to the logger
        self.logger.addHandler(success_handler)
        self.logger.addHandler(error_handler)

    def getInfoLogger(self):
        # get all log records with level INFO
        info_handler: MemoryHandler = self.logger.handlers[0]
        return info_handler.get_messages()

    def getErrorLogger(self):
        # get all log records with level ERROR
        error_handler: MemoryHandler = self.logger.handlers[1]
        return error_handler.get_messages()

    # ------  admin  ------ #
    def openTheSystem(self, username):
        try:
            self.store_facade.openSystem(username)
            self.logger.info("AriExpress is now open and running")
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def addAdmin(self, username, newAdminName, newPassword, newEmail):
        try:
            admin = self.store_facade.addAdmin(username, newAdminName, newPassword, newEmail)
            self.logger.info("admin has been added successfully")
            return Response(admin, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

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

    def exitTheSystem(self):  # TODO: same as in StoreFacade todo task - need to change
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
            self.logger.info("logged in as guest successfully")
            return Response(guest, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    #  Members
    def register(self, user_name, password, email):
        try:
            member = self.store_facade.register(user_name, password, email)
            self.logger.info("user has registered successfully")
            return Response(member, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def logIn(self, username, password):  # todo no responses
        try:
            member = self.store_facade.logInAsMember(username, password)
            self.logger.info(f"Welcome {str(username)}")
            return Response(member, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    # def logIn(self, username, password):  # todo responses from service to gui
    #     try:
    #         member = self.store_facade.logInAsMember(username, password)
    #         self.logger.info(f"Welcome {str(username)}")
    #         return Response(member.toJson(), True)
    #     except Exception as e:
    #         self.logger.error(f"An error occurred: {str(e)}")
    #         return Response(e, False)
    # def logIn(self, username, password):  # todo responses from domain to service
    #     memberResponse = self.store_facade.logInAsMember(username, password)
    #     if memberResponse.getStatus():
    #         member = memberResponse.getReturnValue()
    #         self.logger.info(f"Welcome {str(username)}")
    #         return member.toJson()
    #     else:
    #         e = memberResponse.getReturnValue()
    #         self.logger.error(f"An error occurred: {str(e)}")
    #         return e

    def logOut(self, username):
        try:
            self.store_facade.logOut(username)
            self.logger.info(f"Logged out successfully, goodbye {str(username)}")
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def getMemberPurchaseHistory(self, username):
        try:
            purchase_history = self.store_facade.getMemberPurchaseHistory(username)
            self.logger.info(f"fetching {str(username)} purchase history")
            return Response(purchase_history, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    # ------  stores  ------ #

    def getStores(self):
        try:
            stores = self.store_facade.getStores()
            self.logger.info(f"fetching all stores in the system")
            return Response(stores, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def getProductsByStore(self, storename):
        try:
            products = self.store_facade.getProductsByStore(storename)
            self.logger.info(f"fetching all products in store {str(storename)}")
            return Response(products, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def getProduct(self, storename, product_id):
        try:
            product = self.store_facade.getProduct(storename, product_id)
            self.logger.info(f"fetching product num {str(product_id)} in store {str(storename)}")
            return Response(product, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def productSearchByName(self, productName):  # and keywords
        try:
            results = self.store_facade.productSearchByName(productName)
            self.logger.info(f"fetching all the products with keyname {str(productName)}")
            return Response(results, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def productSearchByCategory(self, categoryName):  # TODO: probably each store will have its products catagorized
        try:  # TODO: need to create an enum set of categories, shopowners does not create categories.!!!!!!!
            results = self.store_facade.productSearchByCategory(categoryName)
            self.logger.info(f"fetching all the products within the category {str(categoryName)}")
            return Response(results, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def productFilterByFeatures(self,
                                featuresDict):  # TODO (opt) we will assume there's a dict that can say which features will be searched
        try:
            products = self.store_facade.productFilterByFeatures(featuresDict)
            self.logger.info(f"fetching all the products within the feature {str(featuresDict)}")
            return Response(products, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def getBasket(self, username, storename):
        try:
            basket = self.store_facade.getBasket(username, storename)
            self.logger.info(f"fetching the basket of store {str(storename)}")
            return Response(basket, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def getCart(self, username):
        try:
            cart = self.store_facade.getCart(username)
            self.logger.info(f"fetching the cart of {str(username)}")
            return Response(cart, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def addToBasket(self, username, storename, productID, quantity):
        try:
            self.store_facade.addToBasket(username, storename, productID, quantity)
            self.logger.info(f"Item has been added to the cart successfully")
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def removeFromBasket(self, username, storename, productID):
        try:
            answer = self.store_facade.removeFromBasket(username, storename, productID)
            self.logger.info(f"Item has been removed from the cart successfully")
            return Response(answer, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def editBasketQuantity(self, username, storename, product_id, quantity):
        try:
            self.store_facade.editBasketQuantity(username, storename, product_id, quantity)
            self.logger.info(f"Item with id {str(product_id)} has been edited in the basket with {str(quantity)} quantity")
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def purchaseCart(self, user_name, card_number, card_user_name, card_user_ID, card_date,
                     back_number):  # TODO: for now lets assume only credit card(no paypal)
        try:
            flag = self.store_facade.purchaseCart(user_name, card_number, card_user_name, card_user_ID, card_date,
                                                  back_number)
            self.logger.info("Successful purchase")
            return Response(flag, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def placeBid(self, username, storename, offer, productID, quantity):
        try:
            bid = self.store_facade.placeBid(username, storename, offer, productID, quantity)
            self.logger.info(
                f"bid for item number {str(productID)} from the store {str(storename)} has been placed with {str(offer)}")
            return Response(bid, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def getAllBidsFromUser(self, username):
        try:
            bids = self.store_facade.getAllBidsFromUser(username)
            self.logger.info(f"fetching all the Bids of user {str(username)}")
            return Response(bids, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def purchaseConfirmedBid(self, username, storename, bid_id, card_number, card_user_name, card_user_ID, card_date,
                             back_number):
        try:
            self.store_facade.purchaseConfirmedBid(username, storename, bid_id, card_number, card_user_name,
                                                   card_user_ID, card_date,
                                                   back_number)
            self.logger.info(f"Bid id: {str(bid_id)} has been purchased successfully")
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def approveBid(self, username, storename, bid_id):
        try:
            approved_bid = self.store_facade.approveBid(username, storename, bid_id)
            self.logger.info(f"Bid id: {str(bid_id)} has been approved successfully")
            return Response(approved_bid, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def rejectBid(self, username, storename, bid_id):
        try:
            rejected_bid = self.store_facade.rejectBid(username, storename, bid_id)
            self.logger.info(f"Bid id: {str(bid_id)} has been rejected successfully")
            return Response(rejected_bid, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def sendAlternativeOffer(self, username, storename, bid_id, alternate_offer):
        try:
            alt_bid = self.store_facade.sendAlternativeBid(username, storename, bid_id, alternate_offer)
            self.logger.info(f"Bid id: {str(bid_id)} an alternative offer has been offered")
            return Response(alt_bid, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def addAuction(self, username, storename, product_id, starting_price, duration):
        try:
            new_auc = self.store_facade.addAuction(username, storename, product_id, starting_price, duration)
            self.logger.info(f"Auction id: {str(new_auc.get_auction_id())} an auction has been created")
            return Response(new_auc, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def placeOfferInAuction(self, username, storename, auction_id, offer):
        try:
            auc = self.store_facade.addAuction(username, storename, auction_id, offer)
            self.logger.info(f"an offer has been placed on auction id: {str(auc.get_auction_id())}")
            return Response(auc, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def addLottery(self):
        pass

    def getStorePurchaseHistory(self, username, storename):  # TODO: username is demanded for validation of the request
        try:
            transactions = self.store_facade.getStorePurchaseHistory(username, storename)
            self.logger.info(f"transactions of stores has been fetched successfully")
            return Response(transactions, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    # ------  Management  ------ #

    def openStore(self, username, store_name):
        try:
            cur_store = self.store_facade.openStore(username, store_name)
            self.logger.info(f"store named {str(store_name)} has been created successfully")
            return Response(cur_store, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def addNewProductToStore(self, username, storename, productname, categories, quantity, price):
        try:  # TODO check whether this product details are needed
            added_product = self.store_facade.addNewProductToStore(username, storename, productname, quantity, price,
                                                                   categories)
            self.logger.info(f"product named {str(productname)} has been added to the store {str(storename)} successfully")
            return Response(added_product, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def removeProductFromStore(self, username, storename, product_id):
        try:
            deleted_product_id = self.store_facade.removeProductFromStore(username, storename, product_id)
            self.logger.info(f"product id {str(product_id)} has been removed from the store {str(storename)} successfully")
            return Response(deleted_product_id, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def editProductOfStore(self, username, storename,
                           **kwargs):  # TODO (opt) we will assume there's a dict that can say which features will change
        try:
            changed_product = self.store_facade.editProductOfStore(username, storename, **kwargs)
            return Response(changed_product, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def nominateStoreOwner(self, username, nominate_username, store_name):
        try:
            new_access = self.store_facade.nominateStoreOwner(username, nominate_username, store_name)
            self.logger.info(f"user {str(nominate_username)} has been nominated to owner at store {str(store_name)}")
            return Response(new_access, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def nominateStoreManager(self, username, nominate_username, store_name):
        try:
            new_access = self.store_facade.nominateStoreManager(username, nominate_username, store_name)
            self.logger.info(f"user {str(nominate_username)} has been nominated to Manager at store {str(store_name)}")
            return Response(new_access, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def addPermissionForManager(self, requesterID, nominatedID, permission):
        try:
            self.store_facade.addPermissionsForManager()
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def editPermissionsForManager(self, requesterID, nominatedID,
                                  permission):  # TODO still don't know the implementation
        try:
            self.store_facade.editPermissionsForManager()
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def closeStore(self, username, storename):
        try:
            closed_store_name = self.store_facade.closeStore(username, storename)
            self.logger.info(f"store {str(storename)} has been closed")
            return Response(closed_store_name, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def getStaffInfo(self, username, storename):
        try:
            store_accesses_dict = self.store_facade.getStaffInfo(username, storename)
            self.logger.info(f"fetching store {str(storename)} staff info")
            return Response(store_accesses_dict, True)
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def getStoreManagerPermissions(self, requesterID, storeName):
        try:
            self.store_facade.getStoreManagerPermissions()
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return Response(e, False)
