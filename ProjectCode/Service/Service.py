from ProjectCode.Domain.StoreFacade import StoreFacade
import logging
import threading
from ProjectCode.Service.Response import Response
from ProjectCode.Domain.Controllers.StoreFacade import StoreFacade
from ProjectCode.Domain.Objects.UserObjects.Admin import *


logging.basicConfig(filename='logger.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                    
def Singleton(cls):
    _instance_lock = threading.Lock()
    _instance = {}

    def _singleton(*args, **kwargs):
        if cls not in _instance:
            with _instance_lock:
                if cls not in _instance:
                    _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]
    return _singleton




@Singleton
class Service:
    def __init__(self):
        self.store_facade = StoreFacade()

    # ------  logger  ------ #
    def getInfoLogs(self):
        with open('logger.log', 'r') as f:
            return [line.strip() for line in f.readlines() if 'INFO' in line]

    def getErrorLogs(self):
        with open('logger.log', 'r') as f:
            return [line.strip() for line in f.readlines() if 'ERROR' in line]

    # ------  admin  ------ #
    def getAllOnlineOnline(self, user_name):
        try:
            online_members_dict = self.store_facade.getAllOnlineMembers(user_name)
            return Response(online_members_dict,True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def addAdmin(self, username, newAdminName, newPassword, newEmail):
        try:
            admin = self.store_facade.addAdmin(username, newAdminName, newPassword, newEmail)
            logging.info("admin has been added successfully")
            return Response(admin, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
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
            logging.info("logged in as guest successfully")
            return Response(guest, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    #  Members
    def register(self, user_name, password, email):
        try:
            member = self.store_facade.register(user_name, password, email)
            logging.info("user has registered successfully")
            return Response(member, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def logIn(self, username, password):  # todo no responses
        try:
            member = self.store_facade.logInAsMember(username, password)
            logging.info(f"Welcome {str(username)}")
            return Response(member, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

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
            return Response(e, False)

    def getMemberPurchaseHistory(self, username):
        try:
            purchase_history = self.store_facade.getMemberPurchaseHistory(username)
            logging.info(f"fetching {str(username)} purchase history")
            return Response(purchase_history, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    # ------  stores  ------ #

    def getStores(self):
        try:
            stores = self.store_facade.getStores()
            logging.info(f"fetching all stores in the system")
            return Response(stores, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def getProductsByStore(self, storename, username):
        try:
            products = self.store_facade.getProductsByStore(storename, username)
            logging.info(f"fetching all products in store {str(storename)}")
            return Response(products, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def getProduct(self, storename, product_id, username):
        try:
            product = self.store_facade.getProduct(storename, product_id, username)
            logging.info(f"fetching product num {str(product_id)} in store {str(storename)}")
            return Response(product, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def productSearchByName(self, productName, username):  # and keywords
        try:
            results = self.store_facade.productSearchByName(productName, username)
            logging.info(f"fetching all the products with keyname {str(productName)}")
            return Response(results, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)


    def productSearchByCategory(self, categoryName, username):#TODO: probably each store will have its products catagorized
        try:#TODO: need to create an enum set of categories, shopowners does not create categories.!!!!!!!
            results = self.store_facade.productSearchByCategory(categoryName, username)
            logging.info(f"fetching all the products within the category {str(categoryName)}")
            return Response(results, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)


    def productFilterByFeatures(self, featuresDict, username):    #TODO (opt) we will assume there's a dict that can say which features will be searched
        try:
            products = self.store_facade.productFilterByFeatures(featuresDict, username)
            logging.info(f"fetching all the products within the feature {str(featuresDict)}")
            return Response(products, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def getBasket(self, username, storename):
        try:
            basket = self.store_facade.getBasket(username, storename)
            logging.info(f"fetching the basket of store {str(storename)}")
            return Response(basket, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def getCart(self, username):
        try:
            cart = self.store_facade.getCart(username)
            logging.info(f"fetching the cart of {str(username)}")
            return Response(cart, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def addToBasket(self, username, storename, productID, quantity):
        try:
            self.store_facade.addToBasket(username, storename, productID, quantity)
            logging.info(f"Item has been added to the cart successfully")
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def removeFromBasket(self, username, storename, productID):
        try:
            answer = self.store_facade.removeFromBasket(username, storename, productID)
            logging.info(f"Item has been removed from the cart successfully")
            return Response(answer, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def editBasketQuantity(self, username, storename, product_id, quantity):
        try:
            self.store_facade.editBasketQuantity(username, storename, product_id, quantity)
            logging.info(f"Item with id {str(product_id)} has been edited in the basket with {str(quantity)} quantity")
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def purchaseCart(self, user_name, card_number, card_user_name, card_user_ID, card_date,
                     back_number):  # TODO: for now lets assume only credit card(no paypal)
        try:
            flag = self.store_facade.purchaseCart(user_name, card_number, card_user_name, card_user_ID, card_date,
                                                  back_number)
            logging.info("Successful purchase")
            return Response(flag, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def placeBid(self, username, storename, offer, productID, quantity):
        try:
            bid = self.store_facade.placeBid(username, storename, offer, productID, quantity)
            logging.info(
                f"bid for item number {str(productID)} from the store {str(storename)} has been placed with {str(offer)}")
            return Response(bid, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def getAllBidsFromUser(self, username):
        try:
            bids = self.store_facade.getAllBidsFromUser(username)
            logging.info(f"fetching all the Bids of user {str(username)}")
            return Response(bids, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def purchaseConfirmedBid(self, username, storename, bid_id, card_number, card_user_name, card_user_ID, card_date,
                             back_number):
        try:
            self.store_facade.purchaseConfirmedBid(username, storename, bid_id, card_number, card_user_name,
                                                   card_user_ID, card_date,
                                                   back_number)
            logging.info(f"Bid id: {str(bid_id)} has been purchased successfully")
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def approveBid(self, username, storename, bid_id):
        try:
            approved_bid = self.store_facade.approveBid(username, storename, bid_id)
            logging.info(f"Bid id: {str(bid_id)} has been approved successfully")
            return Response(approved_bid, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def rejectBid(self, username, storename, bid_id):
        try:
            rejected_bid = self.store_facade.rejectBid(username, storename, bid_id)
            logging.info(f"Bid id: {str(bid_id)} has been rejected successfully")
            return Response(rejected_bid, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def sendAlternativeOffer(self, username, storename, bid_id, alternate_offer):
        try:
            alt_bid = self.store_facade.sendAlternativeBid(username, storename, bid_id, alternate_offer)
            logging.info(f"Bid id: {str(bid_id)} an alternative offer has been offered")
            return Response(alt_bid, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def addAuction(self, username, storename, product_id, starting_price, duration):
        try:
            new_auc = self.store_facade.addAuction(username, storename, product_id, starting_price, duration)
            logging.info(f"Auction id: {str(new_auc.get_auction_id())} an auction has been created")
            return Response(new_auc, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def placeOfferInAuction(self, username, storename, auction_id, offer):
        try:
            auc = self.store_facade.addAuction(username, storename, auction_id, offer)
            logging.info(f"an offer has been placed on auction id: {str(auc.get_auction_id())}")
            return Response(auc, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def addLottery(self):
        pass

    def getStorePurchaseHistory(self, username, storename):  # TODO: username is demanded for validation of the request
        try:
            transactions = self.store_facade.getStorePurchaseHistory(username, storename)
            logging.info(f"transactions of stores has been fetched successfully")
            return Response(transactions, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    # ------  Management  ------ #

    def openStore(self, username, store_name):
        try:
            cur_store = self.store_facade.openStore(username, store_name)
            logging.info(f"store named {str(store_name)} has been created successfully")
            return Response(cur_store, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def addNewProductToStore(self, username, storename, productname, categories, quantity, price):
        try:  # TODO check whether this product details are needed
            added_product = self.store_facade.addNewProductToStore(username, storename, productname, quantity, price,
                                                                   categories)
            logging.info(f"product named {str(productname)} has been added to the store {str(storename)} successfully")
            return Response(added_product, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def removeProductFromStore(self, username, storename, product_id):
        try:
            deleted_product_id = self.store_facade.removeProductFromStore(username, storename, product_id)
            logging.info(f"product id {str(product_id)} has been removed from the store {str(storename)} successfully")
            return Response(deleted_product_id, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def editProductOfStore(self, username, storename,
                           **kwargs):  # TODO (opt) we will assume there's a dict that can say which features will change
        try:
            changed_product = self.store_facade.editProductOfStore(username, storename, **kwargs)
            return Response(changed_product, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def nominateStoreOwner(self, username, nominate_username, store_name):
        try:
            new_access = self.store_facade.nominateStoreOwner(username, nominate_username, store_name)
            logging.info(f"user {str(nominate_username)} has been nominated to owner at store {str(store_name)}")
            return Response(new_access, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def nominateStoreManager(self, username, nominate_username, store_name):
        try:
            new_access = self.store_facade.nominateStoreManager(username, nominate_username, store_name)
            logging.info(f"user {str(nominate_username)} has been nominated to Manager at store {str(store_name)}")
            return Response(new_access, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def addPermissionForManager(self, requesterID, nominatedID, permission):
        try:
            self.store_facade.addPermissionsForManager()
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def editPermissionsForManager(self, requesterID, nominatedID,
                                  permission):  # TODO still don't know the implementation
        try:
            self.store_facade.editPermissionsForManager()
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def closeStore(self, username, storename):
        try:
            closed_store_name = self.store_facade.closeStore(username, storename)
            logging.info(f"store {str(storename)} has been closed")
            return Response(closed_store_name, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def getStaffInfo(self, username, storename):
        try:
            store_accesses_dict = self.store_facade.getStaffInfo(username, storename)
            logging.info(f"fetching store {str(storename)} staff info")
            return Response(store_accesses_dict, True)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)

    def getStoreManagerPermissions(self, requesterID, storeName):
        try:
            self.store_facade.getStoreManagerPermissions()
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return Response(e, False)
