import logging
from ProjectCode.Service.Response import Response
from ProjectCode.Domain.StoreFacade import StoreFacade

#TODO check if all functions (new ones) got logging messages
logging.basicConfig(filename='logger.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



class Service:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.store_facade = StoreFacade()
        return cls._instance


    # ------  logger  ------ #
    def getInfoLogs(self):
        with open('logger.log', 'r') as f:
            return [line.strip() for line in f.readlines() if 'INFO' in line]

    def getErrorLogs(self):
        with open('logger.log', 'r') as f:
            return [line.strip() for line in f.readlines() if 'ERROR' in line]

    # ------  admin  ------ #
    # def openTheSystem(self, username):
    #     try:
    #         self.store_facade.openSystem(username)
    #         logging.info("AriExpress has opened successfully. Running Admin: " + username + ".")
    #     except Exception as e:
    #         logging.error(f"openTheSystem Error: {str(e)}")
    #         return Response(e, False)

    def addAdmin(self, username, newAdminName, newPassword, newEmail):
        try:
            admin = self.store_facade.addAdmin(username, newAdminName, newPassword, newEmail)
            logging.info("admin has been added successfully. New Admin username: " + newAdminName + ". Added by: " + username + ".")
            return Response(admin, True)
        except Exception as e:
            logging.error(f"addAdmin Error: {str(e)}")
            return Response(e, False)

    def removeMember(self, username, memberName):
        try:
            self.store_facade.removeMember(username, memberName)
            logging.info("Member has been removed successfully. By username: " + username + ". Removed username: " + memberName + ".")
            return Response(True, True)
        except Exception as e:
            logging.error(f"removeMember Error: {str(e)}")
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

    def leaveAsGuest(self, guest):
        try:
            self.store_facade.leaveAsGuest(guest)
            logging.info("Guest left successfully. Guest Entrance ID: " + str(guest.get_username()))
            return Response(True, True)
        except ValueError as e:
            logging.error(f"leaveAsGuest Error: {str(e)}")
            return Response(e, False)

    def loginAsGuest(self):
        try:
            guest = self.store_facade.loginAsGuest()
            logging.info("Logged in as guest successfully. Guest Entrance ID: " + str(guest.get_username()))
            return Response(guest, True)
        except Exception as e:
            logging.error(f"logInAsGuest Error: {str(e)}")
            return Response(e, False)
    #  Members
    def register(self, user_name, password, email):
        try:
            member = self.store_facade.register(user_name, password, email)
            logging.info("Registered successfully. By username: " + user_name + ".")
            return Response(member, True)
        except Exception as e:
            logging.error(f"register Error: {str(e)}")
            return Response(e, False)

    def logIn(self, username, password):  # todo no responses
        try:
            member = self.store_facade.logInAsMember(username, password)
            logging.info("Logged in successfully. By username: " + username + ".")
            return Response(member, True)
        except Exception as e:
            logging.error(f"logIn Error: {str(e)}")
            return Response(e, False)

    # def logIn(self, username, password):  # todo responses from service to gui
    #     try:
    #         member = self.store_facade.logInAsMember(username, password)
    #         logging.info(f"Welcome {str(username)}")
    #         return Response(member.toJson(), True)
    #     except Exception as e:
    #         logging.error(f"logIn Error: {str(e)}")
    #         return Response(e, False)
    # def logIn(self, username, password):  # todo responses from domain to service
    #     memberResponse = self.store_facade.logInAsMember(username, password)
    #     if memberResponse.getStatus():
    #         member = memberResponse.getReturnValue()
    #         logging.info(f"Welcome {str(username)}")
    #         return member.toJson()
    #     else:
    #         e = memberResponse.getReturnValue()
    #         logging.error(f"logIn Error: {str(e)}")
    #         return e

    def logOut(self, username):
        try:
            self.store_facade.logOut(username)
            logging.info(f"Logged out successfully. By username: " + username + ".")
        except Exception as e:
            logging.error(f"logOut Error: {str(e)}")
            return Response(e, False)

    def getMemberPurchaseHistory(self, username):
        try:
            purchase_history = self.store_facade.getMemberPurchaseHistory(username)
            logging.debug(f"fetching purchase history of member {str(username)}.")
            return Response(purchase_history, True)
        except Exception as e:
            logging.error(f"getMemberPurchaseHistory Error: {str(e)}")
            return Response(e, False)

    # ------  stores  ------ #

    def getStores(self):
        try:
            stores = self.store_facade.getStores()
            logging.debug(f"fetching all stores in the system")
            return Response(stores, True)
        except Exception as e:
            logging.error(f"getStores Error: {str(e)}")
            return Response(e, False)

    def getProductsByStore(self, storename, username):
        try:
            products = self.store_facade.getProductsByStore(storename, username)
            logging.debug(f"fetching all products in store '{str(storename)}'. By username: " + username + ".")
            return Response(products, True)
        except Exception as e:
            logging.error(f"getProductsByStore Error: {str(e)}")
            return Response(e, False)

    def getProduct(self, storename, product_id, username):
        try:
            product = self.store_facade.getProduct(storename, product_id, username)
            logging.debug(f"fetching product '{str(product_id)}' from store '{str(storename)}'. By username: " + username + ".")
            return Response(product, True)
        except Exception as e:
            logging.error(f"getProduct Error: {str(e)}")
            return Response(e, False)

    def productSearchByName(self, productName, username):  # and keywords
        try:
            results = self.store_facade.productSearchByName(productName, username)
            logging.debug(f"fetching all the products with keyname '{str(productName)}'. By username: " + username + ".")
            return Response(results, True)
        except Exception as e:
            logging.error(f"productSearchByName Error: {str(e)}")
            return Response(e, False)


    def productSearchByCategory(self, categoryName, username):#TODO: probably each store will have its products catagorized
        try:#TODO: need to create an enum set of categories, shopowners does not create categories.!!!!!!!
            results = self.store_facade.productSearchByCategory(categoryName, username)
            logging.debug(f"fetching all the products within the category '{str(categoryName)}'. By username: " + username + ".")
            return Response(results, True)
        except Exception as e:
            logging.error(f"productSearchByCategory Error: {str(e)}")
            return Response(e, False)


    def productFilterByFeatures(self, featuresDict, username):    #TODO (opt) we will assume there's a dict that can say which features will be searched
        try:
            products = self.store_facade.productFilterByFeatures(featuresDict, username)
            logging.debug(f"fetching all the products within the features '{str(featuresDict)}'. By username: " + username + ".")
            return Response(products, True)
        except Exception as e:
            logging.error(f"productFilterByFeatures Error: {str(e)}")
            return Response(e, False)

    def getBasket(self, username, storename):
        try:
            basket = self.store_facade.getBasket(username, storename)
            logging.debug(f"fetching the basket of store '{str(storename)}'. By username: " + username + ".")
            return Response(basket, True)
        except Exception as e:
            logging.error(f"getBasket Error: {str(e)}")
            return Response(e, False)

    def getCart(self, username):
        try:
            cart = self.store_facade.getCart(username)
            logging.debug(f"fetching the cart of '{str(username)}'. By username: " + username + ".")
            return Response(cart, True)
        except Exception as e:
            logging.error(f"getCart Error: {str(e)}")
            return Response(e, False)

    def addToBasket(self, username, storename, productID, quantity):
        try:
            self.store_facade.addToBasket(username, storename, productID, quantity)
            logging.debug(f"Item has been added to the cart successfully. By username: " + username + ". storename: " + storename + ". productID: " + str(productID) + ". quantity: " + str(quantity) + ".")
        except Exception as e:
            logging.error(f"addToBasket Error: {str(e)}")
            return Response(e, False)

    def removeFromBasket(self, username, storename, productID):
        try:
            answer = self.store_facade.removeFromBasket(username, storename, productID)
            logging.debug(f"Item has been removed from the cart successfully. By username: " + username + ". storename: " + storename + ". productID: " + str(productID) + ".")
            return Response(answer, True)
        except Exception as e:
            logging.error(f"removeFromBasket Error: {str(e)}")
            return Response(e, False)

    def editBasketQuantity(self, username, storename, product_id, quantity):
        try:
            self.store_facade.editBasketQuantity(username, storename, product_id, quantity)
            logging.debug(f"Item quantity has been edited successfully. By username: " + username + ". storename: " + storename + ". productID: " + str(product_id) + ". quantity: " + str(quantity) + ".")
        except Exception as e:
            logging.error(f"editBasketQuantity Error: {str(e)}")
            return Response(e, False)

    def purchaseCart(self, user_name, card_number, card_user_name, card_user_ID, card_date,
                     back_number, address):  # TODO: for now lets assume only credit card(no paypal)
        try:
            flag = self.store_facade.purchaseCart(user_name, card_number, card_user_name, card_user_ID, card_date,
                                                  back_number, address)
            logging.info("Cart was purchased successfully. By username: " + user_name + ".")
            return Response(flag, True)
        except Exception as e:
            logging.error(f"purchaseCart Error: {str(e)}")
            return Response(e, False)

    def placeBid(self, username, storename, offer, productID, quantity):
        try:
            bid = self.store_facade.placeBid(username, storename, offer, productID, quantity)
            logging.info("Bid was placed successfully. By username: " + username + ". storename: " + storename + ". productID: " + str(productID) + ". quantity: " + str(quantity) + ". offer: " + str(offer) + ".")
            return Response(bid, True)
        except Exception as e:
            logging.error(f"placeBid Error: {str(e)}")
            return Response(e, False)

    def getAllBidsFromUser(self, username):
        try:
            bids = self.store_facade.getAllBidsFromUser(username)
            logging.debug(f"fetching all the user's bids. By username: " + username + ".")
            return Response(bids, True)
        except Exception as e:
            logging.error(f"getAllBidsFromUser Error: {str(e)}")
            return Response(e, False)

    def purchaseConfirmedBid(self, username, storename, bid_id, card_number, card_user_name, card_user_ID, card_date,
                             back_number):
        try:
            self.store_facade.purchaseConfirmedBid(username, storename, bid_id, card_number, card_user_name,
                                                   card_user_ID, card_date,
                                                   back_number)
            logging.info("Bid purchase was made successfully. By username: " + username + ". storename: " + storename + ". bid_id: " + str(bid_id) + ".")
        except Exception as e:
            logging.error(f"purchaseConfirmedBid Error: {str(e)}")
            return Response(e, False)

    def approveBid(self, username, storename, bid_id):
        try:
            approved_bid = self.store_facade.approveBid(username, storename, bid_id)
            logging.info("Bid was added successfully. By username: " + username + ". storename: " + storename + ". bid_id: " + str(bid_id) + ".")
            return Response(approved_bid, True)
        except Exception as e:
            logging.error(f"approveBid Error: {str(e)}")
            return Response(e, False)

    def rejectBid(self, username, storename, bid_id):
        try:
            rejected_bid = self.store_facade.rejectBid(username, storename, bid_id)
            logging.info("Bid was rejected successfully. By username: " + username + ". storename: " + storename + ". bid_id: " + str(bid_id) + ".")
            return Response(rejected_bid, True)
        except Exception as e:
            logging.error(f"rejectBid Error: {str(e)}")
            return Response(e, False)

    def sendAlternativeOffer(self, username, storename, bid_id, alternate_offer):
        try:
            alt_bid = self.store_facade.sendAlternativeBid(username, storename, bid_id, alternate_offer)
            logging.debug(f"Alternative offer was sent successfully. By username: " + username + ". storename: " + storename + ". bid_id: " + str(bid_id) + ". alternate_offer: " + str(alternate_offer) + ".")
            return Response(alt_bid, True)
        except Exception as e:
            logging.error(f"sendAlternativeOffer Error: {str(e)}")
            return Response(e, False)

    def addAuction(self, username, storename, product_id, starting_price, duration):
        try:
            new_auc = self.store_facade.addAuction(username, storename, product_id, starting_price, duration)
            logging.info("Auction has been added successfully. By username: " + username + ". storename: " + storename + ". product_id: " + str(product_id) + ". starting_price: " + str(starting_price) + ". duration: " + str(duration) + ".")
            return Response(new_auc, True)
        except Exception as e:
            logging.error(f"addAuction Error: {str(e)}")
            return Response(e, False)

    def placeOfferInAuction(self, username, storename, auction_id, offer):
        try:
            auc = self.store_facade.addAuction(username, storename, auction_id, offer, None)
            logging.info("Offer has been placed successfully. By username: " + username + ". storename: " + storename + ". auction_id: " + str(auction_id) + ". offer: " + str(offer) + ".")
            return Response(auc, True)
        except Exception as e:
            logging.error(f"placeOfferInAuction Error: {str(e)}")
            return Response(e, False)

    def addLottery(self):
        pass

    def getStorePurchaseHistory(self, username, storename):  # TODO: username is demanded for validation of the request
        try:
            transactions = self.store_facade.getStorePurchaseHistory(storename)
            logging.debug(f"fetching all the store's transactions. By username: " + username + ". storename: " + storename + ".")
            return Response(transactions, True)
        except Exception as e:
            logging.error(f"getStorePurchaseHistory Error: {str(e)}")
            return Response(e, False)

    # ------  Management  ------ #

    def openStore(self, username, store_name):
        try:
            cur_store = self.store_facade.openStore(username, store_name)
            logging.info("Store has been opened successfully. By username: " + username + ". store_name: " + store_name + ".")
            return Response(cur_store, True)
        except Exception as e:
            logging.error(f"openStore Error: {str(e)}")
            return Response(e, False)

    def addNewProductToStore(self, username, storename, productname, categories, quantity, price):
        try:  # TODO check whether this product details are needed
            added_product = self.store_facade.addNewProductToStore(username, storename, productname, quantity, price,
                                                                   categories)
            logging.info("Product has been added successfully. By username: " + username + ". storename: " + storename + ". productname: " + productname + ". categories: " + str(categories) + ". quantity: " + str(quantity) + ". price: " + str(price) + ".")
            return Response(added_product, True)
        except Exception as e:
            logging.error(f"addNewProductToStore Error: {str(e)}")
            return Response(e, False)

    def removeProductFromStore(self, username, storename, product_id):
        try:
            deleted_product_id = self.store_facade.removeProductFromStore(username, storename, product_id)
            logging.info("Product has been removed successfully. By username: " + username + ". storename: " + storename + ". product_id: " + str(product_id) + ".")
            return Response(deleted_product_id, True)
        except Exception as e:
            logging.error(f"removeProductFromStore Error: {str(e)}")
            return Response(e, False)

    def editProductOfStore(self, username, storename,
                           **kwargs):  # TODO (opt) we will assume there's a dict that can say which features will change
        try:
            changed_product = self.store_facade.editProductOfStore(username, storename, **kwargs)
            logging.debug(f"Product has been edited successfully. By username: " + username + ". storename: " + storename + ".")
            return Response(changed_product, True)
        except Exception as e:
            logging.error(f"editProductOfStore Error: {str(e)}")
            return Response(e, False)

    def nominateStoreOwner(self, username, nominated_username, store_name):
        try:
            new_access = self.store_facade.nominateStoreOwner(username, nominated_username, store_name)
            logging.info("Store owner has been nominated successfully. By username: " + username + ". nominated_username: " + nominated_username + ". store_name: " + store_name + ".")
            return Response(new_access, True)
        except Exception as e:
            logging.error(f"nominateStoreOwner Error: {str(e)}")
            return Response(e, False)

    def nominateStoreManager(self, username, nominated_username, store_name):
        try:
            new_access = self.store_facade.nominateStoreManager(username, nominated_username, store_name)
            logging.info("Store manager has been nominated successfully. By username: " + username + ". nominated_username: " + nominated_username + ". store_name: " + store_name + ".")
            return Response(new_access, True)
        except Exception as e:
            logging.error(f"nominateStoreManager Error: {str(e)}")
            return Response(e, False)

    def addPermission(self, requesterID, nominated_username, permission):
        try:
            self.store_facade.addPermissions()
            logging.info("Permission has been added successfully. By username: " + requesterID + ". nominated_username: " + nominated_username + ". permission: " + permission + ".")
        except Exception as e:
            logging.error(f"addPermission Error: {str(e)}")
            return Response(e, False)

    def editPermissions(self, requesterID, nominatedID,
                                  permission):  # TODO still don't know the implementation
        try:
            self.store_facade.editPermissions()
            logging.info("Permission has been edited successfully. By username: " + requesterID + ". nominated_username: " + nominatedID + ". permission: " + permission + ".")
            return Response(True, True)
        except Exception as e:
            logging.error(f"editPermissions Error: {str(e)}")
            return Response(e, False)

    def getPermissions(self, requesterID, nominatedID):  # TODO still don't know the implementation
        try:
            permissions = self.store_facade.getPermissions()
            logging.debug(f"fetching all the store's permissions. By username: " + requesterID + ". nominated_username: " + nominatedID + ".")
            return Response(permissions, True)
        except Exception as e:
            logging.error(f"getPermissions Error: {str(e)}")
            return Response(e, False)

    def closeStore(self, username, storename):
        try:
            closed_store_name = self.store_facade.closeStore(username, storename)
            logging.info("Store has been closed successfully. By username: " + username + ". storename: " + storename + ".")
            return Response(closed_store_name, True)
        except Exception as e:
            logging.error(f"closeStore Error: {str(e)}")
            return Response(e, False)

    def getStaffInfo(self, username, storename):
        try:
            store_accesses_dict = self.store_facade.getStaffInfo(username, storename)
            logging.debug(f"fetching all the store's staff info. By username: " + username + ". storename: " + storename + ".")
            return Response(store_accesses_dict, True)
        except Exception as e:
            logging.error(f"getStaffInfo Error: {str(e)}")
            return Response(e, False)

    def getStoreManagerPermissions(self, requesterID, storeName):
        try:
            self.store_facade.getStoreManagerPermissions()
            logging.debug(f"fetching all the store's manager permissions. By username: " + requesterID + ". storename: " + storeName + ".")
        except Exception as e:
            logging.error(f"getStoreManagerPermissions Error: {str(e)}")
            return Response(e, False)
