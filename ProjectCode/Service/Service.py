import json
import logging

from ProjectCode.Domain.Helpers.JsonSerialize import JsonSerialize
from ProjectCode.Service.Response import Response
from ProjectCode.Domain.StoreFacade import StoreFacade

# TODO check if all functions (new ones) got logging messages
logging.basicConfig(filename='logger.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Service:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.store_facade = StoreFacade()
        return cls._instance

    # ------  logger  ------ # < TODO cuurently without toJson
    def getInfoLogs(self):
        try:
            with open('logger.log', 'r') as f:
                infoLogs = [line.strip() for line in f.readlines() if 'INFO' in line]
                logging.debug("fetched info logs successfully")
                infoLogsJson = json.dumps(infoLogs)
                return Response(infoLogsJson, True)
        except Exception as e:
            logging.error(f"getInfoLogs Error: {str(e)}.")
            return Response(e, False)

    def getDebugLogs(self):
        try:
            with open('logger.log', 'r') as f:
                debugLogs = [line.strip() for line in f.readlines() if 'DEBUG' in line]
                logging.debug("fetched debug logs successfully")
                debugLogsJson = json.dumps(debugLogs)
                return Response(debugLogsJson, True)
        except Exception as e:
            logging.error(f"getDebugLogs Error: {str(e)}.")
            return Response(e, False)

    def getErrorLogs(self):
        try:
            with open('logger.log', 'r') as f:
                errorLogs = [line.strip() for line in f.readlines() if 'ERROR' in line]
                logging.debug("fetched error logs successfully")
                errorLogsJson = json.dumps(errorLogs)
                return Response(errorLogsJson, True)
        except Exception as e:
            logging.error(f"getErrorLogs Error: {str(e)}.")
            return Response(e, False)

    # ------  admin  ------ #
    # def openTheSystem(self, username):
    #     try:
    #         self.store_facade.openSystem(username)
    #         logging.info("AriExpress has opened successfully. Running Admin: " + username + ".")
    #     except Exception as e:
    #         logging.error(f"openTheSystem Error: {str(e)}. By username: '{username}'")
    #         return Response(e, False)

    def addAdmin(self, username, newAdminName, newPassword, newEmail):
        try:
            admin = self.store_facade.addAdmin(username, newAdminName, newPassword, newEmail)
            logging.info(
                "admin has been added successfully. New Admin username: " + newAdminName + ". Added by: " + username + ".")
            return Response(admin.toJson(), True)
        except Exception as e:
            logging.error(f"addAdmin Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def removeMember(self, username, memberName):
        try:
            removedMember = self.store_facade.removeMember(username, memberName)
            logging.info(
                "Member has been removed successfully. By username: " + username + ". Removed username: " + memberName + ".")
            return Response(removedMember.toJson(), True)
        except Exception as e:
            logging.error(f"removeMember Error: {str(e)}. By username: '{username}'")
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

    # def exitTheSystem(self):  # TODO: same as in StoreFacade todo task - need to change
    #     try:
    #         self.store_facade.exitTheSystem()
    #     except ValueError:
    #         pass

    def leaveAsGuest(self, entrance_id):
        try:
            self.store_facade.leaveAsGuest(entrance_id)
            logging.info("Guest left successfully. Guest Entrance ID: " + str(entrance_id))
            data = {'entrance_id': entrance_id}
            return Response(json.dumps(data), True)
        except ValueError as e:
            logging.error(f"leaveAsGuest Error: {str(e)}.")
            return Response(e, False)

    def loginAsGuest(self):
        try:
            entrance_id = self.store_facade.loginAsGuest()
            logging.info("Logged in as guest successfully. Guest Entrance ID: " + str(entrance_id))
            data = {'entrance_id': entrance_id}
            return Response(json.dumps(data), True)
        except Exception as e:
            logging.error(f"logInAsGuest Error: {str(e)}.")
            return Response(e, False)

    #  Members
    def register(self, user_name, password, email):
        try:
            member = self.store_facade.register(user_name, password, email)
            logging.info("Registered successfully. By username: " + user_name + ".")
            return Response(member.toJson(), True)
        except Exception as e:
            logging.error(f"register Error: {str(e)}.")
            return Response(e, False)

    def logIn(self, username, password):
        try:
            member = self.store_facade.logInAsMember(username, password)
            logging.info("Logged in successfully. By username: " + username + ".")
            return Response(member.toJson(), True)
        except Exception as e:
            logging.error(f"logIn Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def logOut(self, username):
        try:
            guest = self.store_facade.logOut(username)
            data = {'username': username, 'entrance_id': guest.getEntranceId()}
            logging.info(f"Logged out successfully. By username: " + username + ". Became a guest with id: " + str(guest.getEntranceId()) + ".")
            return Response(json.dumps(data), True)
        except Exception as e:
            logging.error(f"logOut Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def getMemberPurchaseHistory(self, username):
        try:
            purchase_history = self.store_facade.getMemberPurchaseHistory()
            logging.debug(f"fetching purchase history of member {str(username)}.")
            return Response(purchase_history.toJsonMember(username), True)  # TODO should i json those objects?
        except Exception as e:
            logging.error(f"getMemberPurchaseHistory Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    # ------  stores  ------ #

    def getStoresBasicInfo(self):
        try:
            stores = self.store_facade.getStores()
            logging.debug(f"fetching all stores in the system")
            stores_list = [store.toJsonInfo() for store in stores]
            return Response(json.dumps(stores_list), True)
        except Exception as e:
            logging.error(f"getStoresBasicInfo Error: {str(e)}.")
            return Response(e, False)

    def getStoreProductsInfo(self, storename):
        try:
            store = self.store_facade.getStores()[storename]
            logging.debug(f"fetching store: '{storename}' in the system")
            return Response(store.toJsonProducts(), True)
        except Exception as e:
            logging.error(f"getStoresMoreInfo Error: {str(e)}.")
            return Response(e, False)

    def getStoreAccessesInfo(self, storename):
        try:
            store = self.store_facade.getStores()[storename]
            logging.debug(f"fetching store: '{storename}' in the system")
            return Response(store.toJsonAccesses(), True)
        except Exception as e:
            logging.error(f"getStoresAccessesInfo Error: {str(e)}.")
            return Response(e, False)

    def getStoreAllInfo(self, storename):
        try:
            store = self.store_facade.getStores()[storename]
            logging.debug(f"fetching store: '{storename}' in the system")
            return Response(store.toJsonAll(), True)
        except Exception as e:
            logging.error(f"getStoresMoreInfo Error: {str(e)}.")
            return Response(e, False)

    def getProductsByStore(self, storename, username):
        try:
            products = self.store_facade.getProductsByStore(storename, username)
            logging.debug(f"fetching all products in store '{str(storename)}'. By username: " + username + ".")
            return Response(JsonSerialize.toJsonAttributes(products), True)
        except Exception as e:
            logging.error(f"getProductsByStore Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def getProduct(self, storename, product_id, username):
        try:
            product = self.store_facade.getProduct(storename, product_id, username)
            logging.debug(
                f"fetching product '{str(product_id)}' from store '{str(storename)}'. By username: " + username + ".")
            return Response(product.toJson(), True)
        except Exception as e:
            logging.error(f"getProduct Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def productSearchByName(self, productName, username):  # and keywords
        try:
            results = self.store_facade.productSearchByName(productName, username)
            logging.debug(
                f"fetching all the products with keyname '{str(productName)}'. By username: " + username + ".")
            return Response(JsonSerialize.toJsonAttributes(results), True)
        except Exception as e:
            logging.error(f"productSearchByName Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def productSearchByCategory(self, categoryName,
                                username):  # TODO: probably each store will have its products catagorized
        try:  # TODO: need to create an enum set of categories, shopowners does not create categories.!!!!!!!
            results = self.store_facade.productSearchByCategory(categoryName, username)
            logging.debug(
                f"fetching all the products within the category '{str(categoryName)}'. By username: " + username + ".")
            return Response(JsonSerialize.toJsonAttributes(results), True)
        except Exception as e:
            logging.error(f"productSearchByCategory Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def productFilterByFeatures(self, featuresDict,
                                username):  # TODO (opt) we will assume there's a dict that can say which features will be searched
        try:
            products = self.store_facade.productFilterByFeatures(featuresDict, username)
            logging.debug(
                f"fetching all the products within the features '{str(featuresDict)}'. By username: " + username + ".")
            return Response(JsonSerialize.toJsonAttributes(products), True)
        except Exception as e:
            logging.error(f"productFilterByFeatures Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def getBasket(self, username, storename):
        try:
            basket = self.store_facade.getBasket(username, storename)
            logging.debug(f"fetching the basket of store '{str(storename)}'. By username: " + username + ".")
            return Response(basket.toJson(), True)
        except Exception as e:
            logging.error(f"getBasket Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def getCart(self, username):
        try:
            cart = self.store_facade.getCart(username)
            logging.debug(f"fetching the cart of '{str(username)}'. By username: " + username + ".")
            return Response(cart.toJson(), True)
        except Exception as e:
            logging.error(f"getCart Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def addToBasket(self, username, storename, productID, quantity):
        try:
            basket = self.store_facade.addToBasket(username, storename, productID, quantity)
            logging.debug(
                f"Item has been added to the cart successfully. By username: " + username + ". storename: " + storename + ". productID: " + str(
                    productID) + ". quantity: " + str(quantity) + ".")
            return Response(basket.toJson(), True)
        except Exception as e:
            logging.error(f"addToBasket Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def removeFromBasket(self, username, storename, productID):
        try:
            answer = self.store_facade.removeFromBasket(username, storename, productID)
            logging.debug(
                f"Item has been removed from the cart successfully. By username: " + username + ". storename: " + storename + ". productID: " + str(
                    productID) + ".")
            return Response(answer, True)
        except Exception as e:
            logging.error(f"removeFromBasket Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def editBasketQuantity(self, username, storename, product_id, quantity):
        try:
            basket = self.store_facade.editBasketQuantity(username, storename, product_id, quantity)
            logging.debug(
                f"Item quantity has been edited successfully. By username: " + username + ". storename: " + storename + ". productID: " + str(
                    product_id) + ". quantity: " + str(quantity) + ".")
            return Response(basket.toJson(), True)
        except Exception as e:
            logging.error(f"editBasketQuantity Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def purchaseCart(self, user_name, card_number, card_user_name, card_user_ID, card_date,
                     back_number, address):  # TODO: for now lets assume only credit card(no paypal)
        try:
            self.store_facade.purchaseCart(user_name, card_number, card_user_name, card_user_ID, card_date,
                                                  back_number, address)
            logging.info("Cart was purchased successfully. By username: " + user_name + ".")
            return Response(True, True)
        except Exception as e:
            logging.error(f"purchaseCart Error: {str(e)}.")
            return Response(e, False)

    def placeBid(self, username, storename, offer, productID, quantity):
        try:
            bid = self.store_facade.placeBid(username, storename, offer, productID, quantity)
            logging.info(
                "Bid was placed successfully. By username: " + username + ". storename: " + storename + ". productID: " + str(
                    productID) + ". quantity: " + str(quantity) + ". offer: " + str(offer) + ".")
            return Response(bid.toJson(), True)
        except Exception as e:
            logging.error(f"placeBid Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def getAllBidsFromUser(self, username):
        try:
            bids = self.store_facade.getAllBidsFromUser(username)
            logging.debug(f"fetching all the user's bids. By username: " + username + ".")
            return Response(bids.toJson(), True)
        except Exception as e:
            logging.error(f"getAllBidsFromUser Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def purchaseConfirmedBid(self, username, storename, bid_id, card_number, card_user_name, card_user_ID, card_date,
                             back_number):
        try:
            self.store_facade.purchaseConfirmedBid(username, storename, bid_id, card_number, card_user_name,
                                                   card_user_ID, card_date,
                                                   back_number)
            logging.info(
                "Bid purchase was made successfully. By username: " + username + ". storename: " + storename + ". bid_id: " + str(
                    bid_id) + ".")
            return Response(True, True)
        except Exception as e:
            logging.error(f"purchaseConfirmedBid Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def approveBid(self, username, storename, bid_id):
        try:
            approved_bid = self.store_facade.approveBid(username, storename, bid_id)
            logging.info(
                "Bid was added successfully. By username: " + username + ". storename: " + storename + ". bid_id: " + str(
                    bid_id) + ".")
            return Response(approved_bid.toJson(), True)
        except Exception as e:
            logging.error(f"approveBid Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def rejectBid(self, username, storename, bid_id):
        try:
            rejected_bid = self.store_facade.rejectBid(username, storename, bid_id)
            logging.info(
                "Bid was rejected successfully. By username: " + username + ". storename: " + storename + ". bid_id: " + str(
                    bid_id) + ".")
            return Response(rejected_bid.toJson(), True)
        except Exception as e:
            logging.error(f"rejectBid Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def sendAlternativeOffer(self, username, storename, bid_id, alternate_offer):
        try:
            alt_bid = self.store_facade.sendAlternativeBid(username, storename, bid_id, alternate_offer)
            logging.debug(
                f"Alternative offer was sent successfully. By username: " + username + ". storename: " + storename + ". bid_id: " + str(
                    bid_id) + ". alternate_offer: " + str(alternate_offer) + ".")
            return Response(alt_bid.toJson(), True)
        except Exception as e:
            logging.error(f"sendAlternativeOffer Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def addAuction(self, username, storename, product_id, starting_price, duration):
        try:
            new_auc = self.store_facade.addAuction(username, storename, product_id, starting_price, duration)
            logging.info(
                "Auction has been added successfully. By username: " + username + ". storename: " + storename + ". product_id: " + str(
                    product_id) + ". starting_price: " + str(starting_price) + ". duration: " + str(duration) + ".")
            return Response(new_auc.toJson(), True)
        except Exception as e:
            logging.error(f"addAuction Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def placeOfferInAuction(self, username, storename, auction_id, offer):
        try:
            auc = self.store_facade.addAuction(username, storename, auction_id, offer, None)
            logging.info(
                "Offer has been placed successfully. By username: " + username + ". storename: " + storename + ". auction_id: " + str(
                    auction_id) + ". offer: " + str(offer) + ".")
            return Response(auc.toJson(), True)
        except Exception as e:
            logging.error(f"placeOfferInAuction Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def addLottery(self):
        pass

    def getStorePurchaseHistory(self, username, storename):  # TODO: username is demanded for validation of the request
        try:
            purchase_history = self.store_facade.getMemberPurchaseHistory()
            logging.debug(f"fetching purchase history of member {str(username)}.")
            return Response(purchase_history.toJsonMember(username), True)  # TODO should i json those objects?
        except Exception as e:
            logging.error(f"getMemberPurchaseHistory Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

        try:
            transactions = self.store_facade.getStorePurchaseHistory(storename)
            logging.debug(
                f"fetching all the store's transactions. By username: " + username + ". storename: " + storename + ".")
            return Response(transactions.toJson(), True)
        except Exception as e:
            logging.error(f"getStorePurchaseHistory Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    # ------  Management  ------ #

    def openStore(self, username, store_name):
        try:
            cur_store = self.store_facade.openStore(username, store_name)
            logging.info(
                "Store has been opened successfully. By username: " + username + ". store_name: " + store_name + ".")
            return Response(cur_store.toJson(), True)
        except Exception as e:
            logging.error(f"openStore Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def addNewProductToStore(self, username, storename, productname, categories, quantity, price):
        try:  # TODO check whether this product details are needed
            added_product = self.store_facade.addNewProductToStore(username, storename, productname, quantity, price,
                                                                   categories)
            logging.info(
                "Product has been added successfully. By username: " + username + ". storename: " + storename + ". productname: " + productname + ". categories: " + str(
                    categories) + ". quantity: " + str(quantity) + ". price: " + str(price) + ".")
            return Response(added_product.toJson(), True)
        except Exception as e:
            logging.error(f"addNewProductToStore Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def removeProductFromStore(self, username, storename, product_id):
        try:
            deleted_product_id = self.store_facade.removeProductFromStore(username, storename, product_id)
            logging.info(
                "Product has been removed successfully. By username: " + username + ". storename: " + storename + ". product_id: " + str(
                    product_id) + ".")
            return Response(deleted_product_id.toJson(), True)
        except Exception as e:
            logging.error(f"removeProductFromStore Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def editProductOfStore(self, username, storename,
                           **kwargs):  # TODO (opt) we will assume there's a dict that can say which features will change
        try:
            changed_product = self.store_facade.editProductOfStore(username, storename, **kwargs)
            logging.debug(
                f"Product has been edited successfully. By username: " + username + ". storename: " + storename + ".")
            return Response(changed_product.toJson(), True)
        except Exception as e:
            logging.error(f"editProductOfStore Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def nominateStoreOwner(self, username, nominated_username, store_name):
        try:
            new_access = self.store_facade.nominateStoreOwner(username, nominated_username, store_name)
            logging.info(
                "Store owner has been nominated successfully. By username: " + username + ". nominated_username: " + nominated_username + ". store_name: " + store_name + ".")
            return Response(new_access.toJson(), True)
        except Exception as e:
            logging.error(f"nominateStoreOwner Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def nominateStoreManager(self, username, nominated_username, store_name):  #TODO
        try:
            new_access = self.store_facade.nominateStoreManager(username, nominated_username, store_name)
            logging.info(
                "Store manager has been nominated successfully. By username: " + username + ". nominated_username: " + nominated_username + ". store_name: " + store_name + ".")
            return Response(new_access.toJson(), True)
        except Exception as e:
            logging.error(f"nominateStoreManager Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def addPermission(self, requesterID, nominated_username, permission):
        try:
            self.store_facade.addPermissions()
            logging.info(
                "Permission has been added successfully. By username: " + requesterID + ". nominated_username: " + nominated_username + ". permission: " + permission + ".")
            return Response(True, True)
        except Exception as e:
            logging.error(f"addPermission Error: {str(e)}.")
            return Response(e, False)

    def editPermissions(self, requesterID, nominatedID,
                        permission):  # TODO still don't know the implementation
        try:
            self.store_facade.editPermissions()
            logging.info(
                "Permission has been edited successfully. By username: " + requesterID + ". nominated_username: " + nominatedID + ". permission: " + permission + ".")
            return Response(True, True)
        except Exception as e:
            logging.error(f"editPermissions Error: {str(e)}.")
            return Response(e, False)

    def getPermissions(self, requesterID, nominatedID):  # TODO still don't know the implementation
        try:
            permissions = self.store_facade.getPermissions()
            logging.debug(
                f"fetching all the store's permissions. By username: " + requesterID + ". nominated_username: " + nominatedID + ".")
            return Response(permissions.toJson(), True)
        except Exception as e:
            logging.error(f"getPermissions Error: {str(e)}.")
            return Response(e, False)

    def closeStore(self, username, storename):
        try:
            closed_store_name = self.store_facade.closeStore(username, storename)
            logging.info(
                "Store has been closed successfully. By username: " + username + ". storename: " + storename + ".")
            return Response(closed_store_name.toJson(), True)
        except Exception as e:
            logging.error(f"closeStore Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def getStaffInfo(self, username, storename):
        try:
            store_accesses_dict = self.store_facade.getStaffInfo(username, storename)
            logging.debug(
                f"fetching all the store's staff info. By username: " + username + ". For store: " + storename + ".")
            store_accesses_json = []
            for username, access in store_accesses_dict.items():
                data = {'username': username,
                        'access': access.toJson()}
                store_accesses_json.append(data)
            return Response(json.dumps(data), True)
        except Exception as e:
            logging.error(f"getStaffInfo Error: {str(e)}. By username: '{username}'")
            return Response(e, False)

    def getStoreManagerPermissions(self, requesterID, storeName):
        try:
            self.store_facade.getStoreManagerPermissions()
            logging.debug(
                f"fetching all the store's manager permissions. By username: " + requesterID + ". storename: " + storeName + ".")
            return Response(True, True)
        except Exception as e:
            logging.error(f"getStoreManagerPermissions Error: {str(e)}.")
            return Response(e, False)
