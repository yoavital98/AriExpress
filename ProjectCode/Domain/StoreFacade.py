import json
from datetime import datetime

import peewee
from peewee import SqliteDatabase, MySQLDatabase, PostgresqlDatabase
#import psycopg2
from ProjectCode.DAL.AccessModel import AccessModel
from ProjectCode.DAL.AccessStateModel import AccessStateModel
from ProjectCode.DAL.AdminModel import AdminModel
from ProjectCode.DAL.BasketModel import BasketModel
from ProjectCode.DAL.BidModel import BidModel
from ProjectCode.DAL.BidsRequestModel import BidsRequestModel
from ProjectCode.DAL.DiscountModel import DiscountModel
from ProjectCode.DAL.GuestModel import GuestModel
from ProjectCode.DAL.MemberModel import MemberModel
from ProjectCode.DAL.MessageModel import MessageModel
from ProjectCode.DAL.NominationAgreementModel import NominationAgreementModel
from ProjectCode.DAL.NotificationModel import NotificationModel
from ProjectCode.DAL.ProductBasketModel import ProductBasketModel
from ProjectCode.DAL.ProductModel import ProductModel
from ProjectCode.DAL.ProductStoreTransactionModel import ProductStoreTransactionModel
from ProjectCode.DAL.ProductUserTransactionModel import ProductUserTransactionModel
from ProjectCode.DAL.PurchasePolicyModel import PurchasePolicyModel
from ProjectCode.DAL.StoreModel import StoreModel
from ProjectCode.DAL.StoreOfUserTransactionModel import StoreOfUserTransactionModel
from ProjectCode.DAL.StoreTransactionModel import StoreTransactionModel
from ProjectCode.DAL.SystemModel import SystemModel
from ProjectCode.DAL.database_conf import DatabaseConf
from ProjectCode.DAL.UserTransactionModel import UserTransactionModel
from ProjectCode.Domain.ExternalServices.MessageController import MessageController
from ProjectCode.Domain.ExternalServices.PaymetService import PaymentService
from ProjectCode.Domain.ExternalServices.SupplyService import SupplyService
from ProjectCode.Domain.ExternalServices.TransactionHistory import TransactionHistory
from ProjectCode.Domain.ExternalServices.TransactionObjects.UserTransaction import UserTransaction
from ProjectCode.Domain.Helpers.TypedDict import TypedDict
# -------MarketObjects Imports-------#
from ProjectCode.Domain.MarketObjects.Access import Access
from ProjectCode.Domain.MarketObjects.Bid import Bid
from ProjectCode.Domain.ExternalServices.PasswordService import PasswordValidationService
from ProjectCode.Domain.MarketObjects.Store import Store
from ProjectCode.Domain.MarketObjects.StoreObjects.Auction import Auction
from ProjectCode.Domain.MarketObjects.StoreObjects.Product import Product
from ProjectCode.Domain.MarketObjects.User import User
from ProjectCode.Domain.MarketObjects.UserObjects.Admin import Admin
from ProjectCode.Domain.MarketObjects.UserObjects.Guest import Guest
from ProjectCode.Domain.MarketObjects.UserObjects.Member import Member
import threading

from ProjectCode.Domain.Repository.AdminRepository import AdminRepository
from ProjectCode.Domain.Repository.GuestRepository import GuestRepository
from ProjectCode.Domain.Repository.MemberRepository import MemberRepository
from ProjectCode.Domain.Repository.StoreRepository import StoreRepository
from ProjectCode.Domain.Repository.StoreTransactionRepository import StoreTransactionRepository
from ProjectCode.Domain.Repository.UserTransactionRepository import UserTransactionRepository


class StoreFacade:



    def __init__(self, config, send_notification_call=None):
        # Store Data
        # self.lock_for_adding_and_purchasing = threading.Lock()  # lock for purchase
        # self.admins = TypedDict(str, Admin)  # dict of admins
        # self.members = TypedDict(str, Member)  # dict of members
        # self.onlineGuests = TypedDict(str, Guest)  # dict of users
        # self.stores = TypedDict(str, Store)  # dict of stores
        # self.online_members = TypedDict(str, Member)  # dict from username to online members
        # self.banned_members = TypedDict(str,
        #                                 Member)  # dict from username to banned users Todo opt: special home page for banned users
        # # Services
        # self.message_controller = MessageController()  # Assuming get_instance() is the method to get the singleton instance
        # # Data
        # self.accesses = TypedDict(str, Access)  # optional TODO check key type
        # self.nextEntranceID = 0  # guest ID counter
        #
        # self.bid_id_counter = 0  # bid counter
        # # Admin
        # first_admin: Admin = Admin("admin", "12341234", "a@a.com")
        # # first_admin.logInAsAdmin() # added by rubin to prevent deadlock
        # self.admins["admin"] = first_admin
        # # load data
        # self.loadData()

        # Create a database object

        self.db = DatabaseConf.database
        # db = PostgresqlDatabase('postgres', user='postgres', password='01592580',
        #                                host='database-1.ckwkbfc5249a.eu-north-1.rds.amazonaws.com', port=5432)
        if self.db.is_closed():
            self.db.connect()
        # model_list = [SystemModel, ProductModel, StoreModel, AccessModel, AccessStateModel, MemberModel, BasketModel,
        #       ProductBasketModel, DiscountModel, AdminModel, GuestModel, BidModel, BidsRequestModel, PurchasePolicyModel]
        # for m in model_list:
        #    m.delete().execute()

        self.db.drop_tables([SystemModel, ProductModel, StoreModel, AccessModel, AccessStateModel, MemberModel, BasketModel,
                         ProductBasketModel, DiscountModel, AdminModel, GuestModel, BidModel, BidsRequestModel,
                        PurchasePolicyModel,
                        UserTransactionModel, StoreOfUserTransactionModel, ProductUserTransactionModel,
                        StoreTransactionModel,
                        ProductStoreTransactionModel, MessageModel, NotificationModel, NominationAgreementModel])
        self.db.create_tables(
             [SystemModel, ProductModel, StoreModel, AccessModel, AccessStateModel, MemberModel, BasketModel,
              ProductBasketModel, DiscountModel, AdminModel, GuestModel, BidModel, BidsRequestModel, PurchasePolicyModel, UserTransactionModel,
              StoreOfUserTransactionModel, ProductUserTransactionModel, StoreTransactionModel,
              ProductStoreTransactionModel, MessageModel, NotificationModel, NominationAgreementModel])

        self.lock_for_adding_and_purchasing = threading.Lock()  # lock for purchase
        self.admins = AdminRepository() # dict of admins
        self.members = MemberRepository()  # dict of members
        self.members.logInReset()
        self.onlineGuests = GuestRepository()  # dict of users
        self.stores = StoreRepository()  # dict of stores
        self.online_members = MemberRepository(online=True)  # dict from username to online members
        self.banned_members = MemberRepository(banned=True)  # dict from username to banned users Todo opt: special home page for banned users
        # Services
        # Data
        self.accesses = TypedDict(str, Access)  # optional TODO check key type
        self.nextEntranceID = 0  # guest ID counter
        self.bid_id_counter = 0  # bid counter


        # Admin
        self.loadConfigAdmins(config["Admins"])

        # load data
        self.loadData()

        # handshake with supply service and payment service
        self.supply_service = SupplyService(config["SupplyService"])
        self.payment_service = PaymentService(config["PaymentService"])
        # self.supply_service.perform_handshake()
        # self.payment_service.perform_handshake()



        # database config init
        # TODO: connect to db # ------------------- TODO ------------------- #

        self.message_controller = MessageController(send_notification_call)


        # REPOSITORY FIELDS - TO BE REPLACED
        self.members_test = MemberRepository()
        self.stores_test = StoreRepository()
        self.admins_test = AdminRepository()
        self.onlineGuests_test = GuestRepository()
        self.user_transactions_test = UserTransactionRepository()
        self.store_transactions_test = StoreTransactionRepository()


    # ------  System  ------ #
    def loadData(self):  # todo complete
        pass

    def loadConfigAdmins(self, admins : dict):
        for name, pwd in admins.items():
            new_admin: Admin = Admin(name, pwd, "admin@admin.com")
            self.admins[name] = new_admin
            # print(name, pwd)


    # ------  users  ------ #
    #  Guests
    # Login from Guest to Member, this login is not from the main login screen. and from the state of a guest to Member

    def logInFromGuestToMember(self, entrance_id, user_name, password):
        with self.db.atomic():
            password_validator = PasswordValidationService()
            guest: Guest = self.onlineGuests.get(str(entrance_id))
            if guest is None:
                raise Exception("Entrance id not found")
            # guest_cart: Cart = guest.get_cart()
            if self.members.keys().__contains__(user_name):
                existing_member: Member = self.members[user_name]
                if password_validator.ConfirmPassword(password, existing_member.get_password()):
                    existing_member.logInAsMember()
                    existing_member.setEntranceId(str(entrance_id))  # it's the same entrance id
                    #  existing_member.addGuestProductsToMemberCart(guest_cart) # TODO: do I need it?
                    self.online_members[existing_member.get_username()] = existing_member  # keeping track who's online
                    self.leaveAsGuest(entrance_id)  # he isn't a guest anymore
                    return existing_member
                    # return DataMember(existing_member)
                else:
                    raise Exception("username or password does not match")
            else:
                raise Exception("username or password does not match")

    def exitTheSystem(self):  # TODO: @Ari and @Yoav should decide if we need this function
        pass

    # Getting an admin from the admins
    def __getAdmin(self, user_name):
        if self.admins.keys().__contains__(user_name):
            return self.admins[user_name]
        else:
            raise Exception("admin does not exists")

    # regular guest entrance
    def loginAsGuest(self):
        new_guest = Guest(str(self.nextEntranceID))
        self.onlineGuests[str(self.nextEntranceID)] = new_guest
        self.nextEntranceID += 1
        return new_guest.get_entrance_id()

    # will be called when a member wants to log out, and gets a Guest status again.
    def returnToGuest(self, entrance_id):
        guest: Guest = Guest(entrance_id)
        if self.onlineGuests.get(entrance_id) is None:
            self.onlineGuests[entrance_id] = guest
        return guest

    # only guests

    # when a guest leaves the system.
    def leaveAsGuest(self, entrance_id):
        if self.onlineGuests.keys().__contains__(str(entrance_id)):
            self.onlineGuests.__delitem__(str(entrance_id))
        else:
            raise Exception("This entrance id doesn't belong to the online guests list")

    #  Members
    # private method, checks if the member is logged in
    def checkIfMemberExists(self, user_name):
        if not self.members.keys().__contains__(user_name):
            raise Exception("user does not exists")

    def checkIfUserIsLoggedIn(self, user_name):
        return self.online_members.keys().__contains__(user_name)

    # checks if username exists in the system
    def checkIfUsernameExists(self, user_name):
        return self.members.keys().__contains__(str(user_name))

    # user_name could be an entranceID or username, depends on what it is it will return the correct User
    def getUserOrMember(self, user_name):  # TODO: change the if's because checking the keys somehow dosent work
        if self.members.keys().__contains__(str(user_name)):
            # if not self.members.isBanned(user_name):
                if self.online_members.keys().__contains__(str(user_name)):
                    return self.members.get(user_name)
                else:
                    raise Exception("user is not logged in")
            # else:
            #     raise Exception("this member is banned")
        else:
            if self.onlineGuests.keys().__contains__(str(user_name)):
                return self.onlineGuests.get(str(user_name))
            else:
                raise Exception("user is not guest nor a member")

    def checkIfBanned(self, username):
        if self.members.keys().__contains__(str(username)):
            return self.members.isBanned(username)
        else:
            raise Exception("Member doesn't exists.")


    # gets an online member.
    def getOnlineMemberOnly(self, user_name):
        if self.online_members.keys().__contains__(user_name):
            return self.online_members.get(user_name)
        else:
            raise Exception("user is not logged in or is not a member")
        
    def getAllMembers(self):
        return self.members.getAll()

    # Registers a guest, register doesn't mean the user is logged in
    def register(self, user_name, password, email):
        with self.db.atomic():
            password_validator = PasswordValidationService()
            if not (self.members.keys().__contains__(str(user_name)) or user_name == ""):
                if password_validator.ValidatePassword(password):
                    new_member: Member = Member(str(0), user_name, password, email)
                    self.members[str(user_name)] = new_member
                    return new_member
                else:
                    raise Exception("password is too weak")
            else:
                raise Exception("This username is already in the system")

    #  only members

    # Login straight to Member and not as guest from the home logging screen.
    def logInAsMember(self, username, password):
        with self.db.atomic():
            password_validator = PasswordValidationService()
            # check if the user is an admin
            if self.admins.keys().__contains__(username):
                return self.logInAsAdmin(username, password)
            # check if the member is an actual user
            if self.members.keys().__contains__(username):
                #if not self.members.isBanned(username):
                    if not self.online_members.__contains__(username):
                        existing_member: Member = self.members[username]
                        if password_validator.ConfirmPassword(password, existing_member.get_password()):
                            existing_member.logInAsMember()
                            existing_member.setEntranceId(str(self.nextEntranceID))
                            self.nextEntranceID += 1
                            self.online_members[username] = existing_member  # indicates that the user is logged in
                            return existing_member
                            # return DataMember(existing_member)
                        else:
                            raise Exception("username or password does not match")
                    else:
                        raise Exception("user is already logged in")
                # else:
                #     raise Exception("this member is banned")
            else:
                raise Exception("username or password does not match")

    #  only members

    # logout a member
    def logOut(self, username):
        with self.db.atomic():
            if self.admins.keys().__contains__(username):
                self.logOutAsAdmin(username)
                guest: Guest = self.returnToGuest(str(self.nextEntranceID))  # returns as a guest
                self.nextEntranceID += 1
                return guest
            if self.members.keys().__contains__(username):
                existing_member: Member = self.members[username]
                self.online_members.remove(username)  # deletes the user from the online users
                guest: Guest = self.returnToGuest(str(existing_member.get_entrance_id()))  # returns as a guest
                return guest
            else:
                raise Exception("Logout is not an option")

    #  only members
    # getting the user purchase history
    def getMemberPurchaseHistory(self, requesterID, username):
        transaction_history = TransactionHistory()
        if self.admins.keys().__contains__(requesterID) or (
                  requesterID == username and self.checkIfUserIsLoggedIn(requesterID)):
            return transaction_history.get_User_Transactions(username)
        else:
            raise Exception("username isn't logged in")

    # guest and member
    # getting a User's basket
    def getBasket(self, user_name, store_name):
        user = self.getUserOrMember(user_name)
        requested_basket = user.get_Basket(store_name)
        return requested_basket
        # return DataBasket(requested_basket)

    # guest and member
    # getting a Users cart
    def getCart(self, username):
        user: User = self.getUserOrMember(str(username))
        requested_cart = user.get_cart()
        return requested_cart
        # return DataCart(requested_cart)

    # guest and member
    # adding a product to basket, checking with store if the item is available
    def addToBasket(self, username, store_name, product_id, quantity):
        with self.db.atomic():
            user: User = self.getUserOrMember(str(username))
            store: Store = self.stores.get(store_name)
            if store is None:
                raise Exception("Store doesnt exists")
            with self.lock_for_adding_and_purchasing:
                print("id:"+str(product_id)+"  quantity:"+str(quantity))
                product = store.checkProductAvailability(product_id, quantity)
            if product is not None:
                filled_basket = user.add_to_cart(username, store, product_id, product, quantity)
                return filled_basket
            else:
                raise Exception("Product is not available or quantity is higher than the stock")

    # guest and member
    # deleting an item from a basket, if the item exists there
    def removeFromBasket(self, username, store_name, product_id):
        with self.db.atomic():
            user: User = self.getUserOrMember(username)
            remove_success = user.removeFromBasket(store_name, product_id)
            if remove_success:
                return remove_success
            else:
                raise Exception("there was a problem with removing the item or either the item doesnt exists in the basket")

    # guest and member
    # editing aa product quantity from a specific basket
    def editBasketQuantity(self, username, store_name, product_id, quantity):
        with self.db.atomic():
            user: User = self.getUserOrMember(username)

            answer = user.checkProductExistance(store_name, product_id)  # answer is boolean
            if answer:
                store: Store = self.stores[store_name]
                with self.lock_for_adding_and_purchasing:
                    product = store.checkProductAvailability(product_id, quantity)
                if product is not None:
                    return user.edit_Product_Quantity(store_name, product_id, quantity)
                else:
                    raise Exception("Product is not available or quantity is higher than the stock")
            else:
                raise Exception("product does not exists in the basket")

    # guest and member
    # getting all the items in the cart and makes a purchase, adding all the items to the Member history and the store's
    def purchaseCart(self, user_name, card_number, card_date, card_user_full_name, ccv, card_holder_id, address, city, country, zipcode):
        with self.db.atomic():
            user: User = self.getUserOrMember(user_name)
            if self.online_members.__contains__(user_name):
                with self.lock_for_adding_and_purchasing:
                    return user.get_cart().PurchaseCart(user_name, card_number, card_date, card_user_full_name, ccv, card_holder_id, address, city, country, zipcode, True)
            else: # guest user
                with self.lock_for_adding_and_purchasing:
                    return user.get_cart().PurchaseCart(user_name, card_number, card_date, card_user_full_name, ccv, card_holder_id, address, city, country, zipcode, False)


    # Bids! -------------------------------------- Bids are for members only --------------------------------------


    def placeBid(self, username, store_name, offer, product_id, quantity):
        with self.db.atomic():
            existing_member: Member = self.getOnlineMemberOnly(username)
            product_id = int(product_id)
            quantity = int(quantity)
            offer = int(offer)
            store: Store = self.stores.get(store_name)
            if store is None:
                raise Exception("Store doesnt exists")
            with self.lock_for_adding_and_purchasing:
                answer = store.checkProductAvailability(product_id, quantity)
            if answer is not None:
                bid: Bid = Bid(self.bid_id_counter, username, store_name, offer, product_id, quantity)
                self.bid_id_counter += 1
                existing_member.addBidToBasket(bid, store)
                store: Store = self.stores[store_name]
                store.requestBid(bid)
                self.message_controller.send_notification(username, "Bid request was placed", "", datetime.now())
                for staff_member in store.getAllStaffMembersNames():
                    self.message_controller.send_notification(staff_member, "Bid request was placed", "", datetime.now())
                return bid
        # return DataBid(bid)

    def getAllBidsFromUser(self, username):
        existing_member: Member = self.getOnlineMemberOnly(username)
        bids_set = existing_member.getAllBids()  # returns set of bids
        return bids_set
        # data_bids_list = [DataBid(bid) for bid in bids_set]
        # return data_bids_list

    def getAllBidsFromStore(self, storename):
        cur_store: Store = self.stores.get(storename)
        if cur_store is None:
            raise Exception("No such store exists")
        return cur_store.get_bids()

    def purchaseConfirmedBid(self, bid_id, store_name, username, card_number, card_date, card_user_full_name, ccv, card_holder_id
                             , address, city, country, zipcode):
        with self.db.atomic():
            existing_member: Member = self.getOnlineMemberOnly(username)
            with self.lock_for_adding_and_purchasing:
                existing_member.get_cart().purchaseConfirmedBid(bid_id, store_name, username, card_number, card_date, card_user_full_name, ccv, card_holder_id
                                 , address, city, country, zipcode)


    # ------  stores  ------ #

    def getStores(self):
        return self.stores

    def getStoresJson(self):
        return self.stores

    def getProductsByStore(self, store_name, user_name):
        cur_store: Store = self.stores.get(
            store_name)  # TODO: change to "try and expect" instead of "if" because the first line returns exception
        if cur_store is None:
            raise Exception("No such store exists")
        # Generate data dict
        # data_products = dict()
        product_dict = cur_store.getProducts(str(user_name))
        return product_dict
        # for key, value in product_dict:
        #     data_products[key] = DataProduct(value)
        # return data_products

    def getProduct(self, store_name, product_id, user_name):
        cur_store: Store = self.stores.get(store_name)
        if cur_store is None:
            raise Exception("No such store exists")
        cur_product: Product = cur_store.getProductById(product_id, str(user_name))
        # return DataProduct(cur_product)
        return cur_product

    def productSearchByName(self, keywords):  # and keywords
        splitted_keywords = keywords.split(" ")
        search_results = TypedDict(str, list)
        for cur_store in self.stores.values():
            product_list = []
            for keyword in splitted_keywords:
                product_list.extend(cur_store.searchProductByName(keyword))
            if len(product_list) > 0:
                json_product_list = [prod.toJson() for prod in product_list]
                search_results[
                    cur_store.get_store_name()] = json_product_list  # TODO: notice product_list type isnt List[Product] therfore TypedDict returns an error

        return search_results

    def productSearchByCategory(self, category):
        search_results = TypedDict(str, list)
        for cur_store in self.stores.values():
            product_list = cur_store.searchProductByCategory(category)
            if len(product_list) > 0:
                # data_product_list = [DataProduct(prod) for prod in product_list]
                search_results[cur_store.get_store_name()] = product_list
        return search_results

    def productFilterByFeatures(self, featuresDict, username):
        search_results = TypedDict(str, list)
        for cur_store in self.stores.values():
            product_list = cur_store.searchProductByFeatures(featuresDict)
            if len(product_list) > 0:
                json_product_list = [prod.toJson() for prod in product_list]
                search_results[cur_store.get_store_name()] = json_product_list
        return search_results

    def getStorePurchaseHistory(self, requesterID, store_name):
        transaction_history = TransactionHistory()
        if self.admins.keys().__contains__(requesterID):
            return transaction_history.get_Store_Transactions(store_name)
        member: Member = self.getOnlineMemberOnly(requesterID)
        # TODO amiel this long line can be shortened with "checkIfHasAccess"
        if member.accesses.__contains__(store_name):
            return transaction_history.get_Store_Transactions(store_name)
        else:
            raise Exception("no permission for this store")

    # ------  Management  ------ #
    # TODO: add check if user is loggedin to each function

    def createStore(self, username, store_name):
        with self.db.atomic():
            cur_member: Member = self.getOnlineMemberOnly(username)
            if cur_member is None:
                raise Exception("The user is not a member or not logged in")
            if self.stores.keys().__contains__(store_name):
                raise Exception("Store name already taken")

            cur_store = Store(store_name)
            self.stores[store_name] = cur_store
            new_access = Access(cur_store, cur_member, username)
            #cur_member.accesses[store_name] = new_access -- ORM CHANGE
            cur_store.setFounder(cur_member.get_username(), new_access)
            return cur_store
        # return DataStore(cur_store)

    def addNewProductToStore(self, username, store_name, name, quantity, price, categories):
        with self.db.atomic():
            member: Member = self.getUserOrMember(username)
            cur_store: Store = self.stores.get(store_name)
            if cur_store is None:
                raise Exception("No such store exists")

            if member.get_accesses().keys().__contains__(store_name):
                access: Access = member.get_accesses().get(store_name)
            else:
                raise Exception("No access for this member to the store")
            new_product = cur_store.addProduct(access, name, quantity, price,
                                               categories)  # TODO: change first atribute to access
            return new_product
            # return DataProduct(new_product)

    def removeProductFromStore(self, username, store_name, product_id):
        with self.db.atomic():
            if not self.checkIfUserIsLoggedIn(username):
                raise Exception("User is not logged in")
            cur_store: Store = self.stores[store_name]
            if cur_store is None:
                raise Exception("No such store exists")
            cur_access = self.members[username].get_accesses().get(store_name)
            if cur_access is None:
                raise Exception("The member doesn't have a permission for that action")
            deleted_product_id = cur_store.deleteProduct(cur_access, product_id)
            return deleted_product_id

    def editProductOfStore(self, username, store_name, product_id, **kwargs):
        with self.db.atomic():
            if not self.checkIfUserIsLoggedIn(username):
                raise Exception("User is not logged in")
            cur_store: Store = self.stores.get(store_name)
            if cur_store is None:
                raise Exception("No such store exists")
            cur_access = self.members[username].get_accesses().get(store_name)
            if cur_access is None:
                raise Exception("The member doesn't have a permission for that action")

            changed_product = cur_store.changeProduct(cur_access, product_id, **kwargs)
            # return DataProduct(changed_product)
            return changed_product

    def nominateStoreOwner(self, requester_username, nominated_username, store_name):
        with self.db.atomic():
            if not self.checkIfUserIsLoggedIn(requester_username):
                raise Exception("User is not logged in")
            cur_store: Store = self.stores[store_name]
            if cur_store is None:
                raise Exception("No such store exists")
            self.checkIfMemberExists(nominated_username)
            nominated_access = Access(cur_store, self.members[nominated_username], requester_username)
            nominated_modified_access = cur_store.setAccess(nominated_access, requester_username, nominated_username,
                                                            "Owner")

            # return DataAccess(nominated_modified_access)
            return nominated_modified_access

    def approveStoreOwnerNomination(self, requester_username, nominated_username,  store_name):
        with self.db.atomic():
            if not self.checkIfUserIsLoggedIn(requester_username):
                raise Exception("User is not logged in")
            cur_store: Store = self.stores[store_name]
            if cur_store is None:
                raise Exception("No such store exists")
            return cur_store.approveNomination(requester_username, nominated_username)

    def rejectStoreOwnerNomination(self, requester_username, nominated_username, store_name):
        with self.db.atomic():
            if not self.checkIfUserIsLoggedIn(requester_username):
                raise Exception("User is not logged in")
            cur_store: Store = self.stores[store_name]
            if cur_store is None:
                raise Exception("No such store exists")
            return cur_store.rejectNomination(requester_username, nominated_username)

    def nominateStoreManager(self, requester_username, nominated_username, store_name):
        with self.db.atomic():
            cur_store: Store = self.stores[store_name]
            if not self.checkIfUserIsLoggedIn(requester_username):
                raise Exception("User is not logged in")
            if cur_store is None:
                raise Exception("No such store exists")
            nominated_access = Access(cur_store, self.members[nominated_username], requester_username)
            nominated_modified_access = cur_store.setAccess(nominated_access, requester_username, nominated_username,
                                                            "Manager")
            return nominated_modified_access

    def getAllNominationRequests(self, store_name, username):
        with self.db.atomic():
            if not self.checkIfUserIsLoggedIn(username):
                raise Exception("User is not logged in")
            cur_store: Store = self.stores[store_name]
            if cur_store is None:
                raise Exception("No such store exists")
            return cur_store.getAllNominationRequests(username)

    def removeAccess(self, requester_username, to_remove_username, store_name):
        with self.db.atomic():
            cur_store: Store = self.stores[store_name]
            if not self.checkIfUserIsLoggedIn(requester_username):
                raise Exception("User is not logged in")
            if cur_store is None:
                raise Exception("No such store exists")
            removed_username = cur_store.removeAccess(to_remove_username, requester_username)
            MessageController().send_notification(to_remove_username, "Removed Permissions", "Your permissions from store "+ store_name + " have been removed", datetime.now())
            return removed_username

    def addPermissions(self, store_name, requester_username, nominated_username, permission):
        with self.db.atomic():
            cur_store: Store = self.stores[store_name]
            if not self.checkIfUserIsLoggedIn(requester_username):
                raise Exception("User is not logged in")
            if cur_store is None:
                raise Exception("No such store exists")
            modified_access = cur_store.modifyPermission(requester_username, nominated_username, permission, op="ADD")
            return modified_access

    def removePermissions(self, store_name, requester_username, nominated_username, permission):
        with self.db.atomic():
            cur_store: Store = self.stores[store_name]
            if not self.checkIfUserIsLoggedIn(requester_username):
                raise Exception("User is not logged in")
            if cur_store is None:
                raise Exception("No such store exists")
            modified_access = cur_store.modifyPermission(requester_username, nominated_username, permission, op="REMOVE")
            return modified_access

    def getPermissions(self, store_name, requester_username, nominated_username):
        cur_store: Store = self.stores[store_name]
        if not self.checkIfUserIsLoggedIn(requester_username):
            raise Exception("User is not logged in")
        if cur_store is None:
            raise Exception("No such store exists")
        permissions: dict = cur_store.getPermissions(requester_username, nominated_username)
        return permissions

    def getPermissionsAsJson(self, store_name, requester_username):
        cur_store: Store = self.stores[store_name]
        # if not self.checkIfUserIsLoggedIn(requester_username):
        #     raise Exception("User is not logged in")
        if cur_store is None:
            raise Exception("No such store exists")
        permissions: dict = cur_store.getPermissionsAsJson(requester_username)
        return permissions

    def addDiscount(self, storename, username, discount_type, percent=0, level="", level_name="", rule={},
                    discounts={}):
        with self.db.atomic():
            cur_store: Store = self.stores.get(storename)
            if cur_store is None:
                raise Exception("No such store exists")
            if not self.checkIfUserIsLoggedIn(username):
                raise Exception("User isn't logged in")
            new_discount = cur_store.addDiscount(username, discount_type, percent=percent, level=level,
                                                 level_name=level_name,
                                                 rule=rule, discounts=discounts)
            return new_discount

    def removeDiscount(self, storename, username, discount_id):
        with self.db.atomic():
            cur_store: Store = self.stores.get(storename)
            if cur_store is None:
                raise Exception("No such store exists")
            if not self.checkIfUserIsLoggedIn(username):
                raise Exception("User isn't logged in")
            cur_store.removeDiscount(username, discount_id)
            return True

    def getDiscount(self, storename, discount_id):
        cur_store: Store = self.stores.get(storename)
        if cur_store is None:
            raise Exception("No such store exists")
        return cur_store.getDiscount(discount_id)

    def getAllDiscounts(self, storename):
        cur_store: Store = self.stores.get(storename)
        if cur_store is None:
            raise Exception("No such store exists")
        return cur_store.getAllDiscounts()


    def addPurchasePolicy(self, storename, username, purchase_policy, rule, level, level_name):
        with self.db.atomic():
            cur_store: Store = self.stores.get(storename)
            if cur_store is None:
                raise Exception("No such store exists")
            if not self.checkIfUserIsLoggedIn(username):
                raise Exception("User isn't logged in")
            new_policy = cur_store.addPurchasePolicy(username, purchase_policy, rule, level=level, level_name=level_name)
            return new_policy

    def removePurchasePolicy(self, storename, username, policy_id):
        with self.db.atomic():
            cur_store: Store = self.stores.get(storename)
            if cur_store is None:
                raise Exception("No such store exists")
            if not self.checkIfUserIsLoggedIn(username):
                raise Exception("User isn't logged in")
            cur_store.removePurchasePolicy(username, policy_id)
            return True

    def getAllPurchasePolicies(self, storename):
        cur_store: Store = self.stores.get(storename)
        if cur_store is None:
            raise Exception("No such store exists")
        return cur_store.getAllPurchasePolicies()

    def getPurchasePolicy(self, storename, policy_id):
        cur_store: Store = self.stores.get(storename)
        if cur_store is None:
            raise Exception("No such store exists")
        return cur_store.getPolicy(policy_id)

    def approveBid(self, username, storename, bid_id):
        with self.db.atomic():
            member: Member = self.getOnlineMemberOnly(username)
            cur_store: Store = self.stores[storename]
            if cur_store is None:
                raise Exception("No such store exists")
            approved_bid = cur_store.approveBid(username, bid_id)
            return approved_bid
        # return DataBid(approved_bid)

    def rejectBid(self, username, storename, bid_id):
        with self.db.atomic():
            member: Member = self.getOnlineMemberOnly(username)
            cur_store: Store = self.stores[storename]
            if cur_store is None:
                raise Exception("No such store exists")
            rejected_bid = cur_store.rejectBid(username, bid_id)
            return rejected_bid
        # return DataBid(rejected_bid)

    def sendAlternativeBid(self, username, storename, bid_id, alternate_offer):
        with self.db.atomic():
            member: Member = self.getOnlineMemberOnly(username)
            cur_store: Store = self.stores[storename]
            if cur_store is None:
                raise Exception("No such store exists")
            alternative_bid = cur_store.sendAlternativeBid(username, bid_id, alternate_offer)
            return alternative_bid
        # return DataBid(alternative_bid)

    def getStaffPendingForBid(self,store_name, bid_id):
        cur_store: Store = self.stores[store_name]
        if cur_store is None:
            raise Exception("No such store exists")
        return cur_store.getStaffPendingForBid(bid_id)


    def addAuction(self, username, storename, product_id, starting_price, duration):
        if not self.checkIfUserIsLoggedIn(username):
            raise Exception("User is not logged in")
        cur_store: Store = self.stores[storename]
        if cur_store is None:
            raise Exception("No such store exists")
        if self.members[username] is None:
            raise Exception("No such member exists")
        if not self.checkIfUserIsLoggedIn(username):
            raise Exception("User is not logged in")
        new_auction = cur_store.startAuction(username, product_id, starting_price, duration)
        return new_auction
        # return DataAuction(new_auction)


    def openStore(self, username, store_name):
        with self.db.atomic():
            if not self.checkIfUserIsLoggedIn(username):
                raise Exception("User is not logged in")
            cur_store: Store = self.stores.get(store_name)
            if cur_store is None:
                raise Exception("No such store exists")
            cur_store.setStoreStatus(True, username)
            MessageController().send_notification(cur_store.getFounder().get_username(), "Store Re-Opened", "", datetime.now())
            for owner in cur_store.getOwners():
                MessageController().send_notification(owner.get_username(), "Store Re-Opened", "", datetime.now())
            return cur_store

    def closeStore(self, username, store_name):
        with self.db.atomic():
            if not self.checkIfUserIsLoggedIn(username):
                raise Exception("User is not logged in")
            cur_store: Store = self.stores.get(store_name)
            if cur_store is None:
                raise Exception("No such store exists")
            cur_store.setStoreStatus(False, username)
            self.sendNotificationToUser(cur_store.getFounder().get_username(), "Store Closed", "", datetime.now())
            for owner in cur_store.getOwners():
                self.sendNotificationToUser(owner.get_username(), "Store Closed", "", datetime.now())
            return cur_store

    def getStaffInfo(self, username, store_name):
        if not self.checkIfUserIsLoggedIn(username):
            raise Exception("User is not logged in")
        cur_store: Store = self.stores[store_name]
        if cur_store is None:
            raise Exception("No such store exists")
        accesses_dict = cur_store.getStaffInfo(username)
        return accesses_dict
        # Generate accesses data objects
        # data_accesses_dict = dict()
        # for key,value in accesses_dict.items():
        #     data_accesses_dict[key] = DataAccess(value)
        # return data_accesses_dict

    def getStaffInfoForMessage(self, store_name):
        cur_store: Store = self.stores[store_name]
        if cur_store is None:
            raise Exception("No such store exists")
        accesses_dict = cur_store.get_accesses()
        return accesses_dict

    def getStoreManagerPermissions(self):
        pass

    # ------  Admins  ------ #
    def logInAsAdmin(self, username, password):
        with self.db.atomic():
            if self.admins.keys().__contains__(username):
                existing_admin: Admin = self.admins[username]
                if existing_admin.logged_In:
                    raise Exception("admin is already in the system")
                if PasswordValidationService().ConfirmPassword(password, existing_admin.get_password()):
                    existing_admin.logInAsAdmin()
                    self.admins[username] = existing_admin
                    return existing_admin
                else:
                    raise Exception("admin name or password does not match")
            else:
                raise Exception("admin name or password does not match")

    def logOutAsAdmin(self, user_name):
        with self.db.atomic():
            if self.admins.keys().__contains__(user_name):
                existing_admin: Admin = self.admins[user_name]
                if not existing_admin.logged_In:
                    raise Exception("Admin is not logged in")
                existing_admin.logOffAsAdmin()
                self.admins[user_name] = existing_admin

    def messageAsAdmin(self, admin_name, message, receiver_user_name):
        pass  # no messanger this version

    def closeStoreAsAdmin(self, admin_name, store_name):
        with self.db.atomic():
            if self.admins.keys().__contains__(admin_name):
                admin: Admin = self.admins.get(admin_name)
                if admin.logged_In:
                    cur_store: Store = self.stores.get(store_name)
                    if cur_store is None:
                        raise Exception("No such store exists")
                    cur_store.close_store_by_admin()
                else:
                    raise Exception("admin is not logged in")
            else:
                raise Exception("no such admin exists")

    def getAdmin(self, user_name):
        if self.admins.keys().__contains__(user_name):
            return self.admins.get(user_name)
        else:
            raise Exception("no admin was found")

    def addAdmin(self, username, newAdminName, newPassword, newEmail):
        with self.db.atomic():
            password_validator = PasswordValidationService()
            if self.admins.keys().__contains__(username):
                if not self.admins.keys().__contains__(newAdminName):
                    if password_validator.ValidatePassword(newPassword):
                        new_admin = Admin(newAdminName, newPassword, newEmail)
                        self.admins[newAdminName] = new_admin
                        return new_admin
                    else:
                        raise Exception("password is too weak")
                else:
                    raise Exception("Admin with the same name already exists")
            else:
                raise Exception("only an admin can add a new admin.")

    def getAllOnlineMembers(self, user_name):
        if self.admins.__contains__(user_name):
            admin: Admin = self.admins.get(user_name)
            if admin.logged_In:
                member_list = []
                for member in self.online_members.values():
                    member_list.append(member)
                return member_list
            else:
                raise Exception("admin is not logged in")
        else:
            raise Exception("only admin can get the online members list")

    def getAllOfflineMembers(self, user_name):
        if self.admins.__contains__(user_name):
            admin: Admin = self.admins.get(user_name)
            if admin.logged_In:
                member_list = []
                for member in self.members.values():
                    if member not in self.online_members.values():
                        member_list.append(member)
                return member_list
            else:
                raise Exception("admin is not logged in")
        else:
            raise Exception("only admin can get the offline members list")

    def removePermissionFreeMember(self, requesterID, memberName):
        with self.db.atomic():
            if self.admins.keys().__contains__(requesterID):
                if self.members.keys().__contains__(memberName):
                    if not self.accesses.keys().__contains__(memberName):
                        self.logOut(memberName)
                        self.sendNotificationToUser(memberName, "BAN", "You have been banned from the system", datetime.now())  # TOdo : add message to login screen or something
                        self.online_members.remove(memberName)
                        banned_member = self.members.get(memberName)
                        self.banned_members[memberName] = banned_member
                        return banned_member
                    else:
                        raise Exception("Can't remove member with store roles")
                else:
                    raise Exception("no such member exists")
            else:
                raise Exception("only admin can remove a member")

    def returnPermissionFreeMember(self, requesterID, memberName):
        if self.admins.keys().__contains__(requesterID):
            if self.banned_members.keys().__contains__(memberName):
                self.sendNotificationToUser(memberName, "UNBAN", "Your ban has been lifted", datetime.now())
                returned_member = self.banned_members.remove(memberName)
                self.members[memberName] = returned_member
                return returned_member
            else:
                raise Exception("no such member exists")
        else:
            raise Exception("only admin can return a member")

    def django_getAllStaffMembersNames(self, storename):
        return self.stores[storename].getAllStaffMembersNames()

    def getAllStaffMembersNames(self, store_name, username):
        cur_store: Store = self.stores[store_name]
        if cur_store is None:
            raise Exception("No such store exists")
        return cur_store.getAllStaffMembersNames(username)

    def getMemberInfo(self, requesterID, user_name):
        transaction_history = TransactionHistory()
        if not self.admins.keys().__contains__(requesterID):
            raise Exception("only admin can get member info")
        if not self.members.keys().__contains__(user_name):
            raise Exception("no such member exists")
        purchase_history = transaction_history.get_User_Transactions(user_name)
        return self.members[user_name], purchase_history

    def getUserStores(self, username):
        stores_list = list()
        for cur_store in self.stores.values():
            if cur_store.get_accesses().get(username) is not None:
                stores_list.append(cur_store)
        return stores_list

    # ==================  Messages  ==================#

    def sendMessageUsers(self, requesterID, receiverID, subject, content, creation_date, file):
        if not self.checkIfUserIsLoggedIn(requesterID):
            raise Exception("User is not logged in")

        return MessageController().send_message(requesterID, receiverID, subject, content, creation_date, file)

    def sendMessageFromStore(self, store_name, receiverID, subject, content, creation_date, file):
        founder = self.getStoreFounder(store_name)
        return MessageController().send_message(founder, receiverID, subject, content, creation_date, file)


    def sendMessageToStore(self, requesterID, storeID, subject, content, creation_date, file):
        if not self.checkIfUserIsLoggedIn(requesterID):
            raise Exception("User is not logged in")
        founder = self.getStoreFounder(storeID)
        return MessageController().send_message(requesterID, founder, subject, content, creation_date, file)


    def getAllMessagesSent(self, requesterID):
        if not self.checkIfUserIsLoggedIn(requesterID):
            raise Exception("User is not logged in")
        return MessageController().get_messages_sent(requesterID)


    def getAllMessagesReceived(self, requesterID):
        if not self.checkIfUserIsLoggedIn(requesterID):
            raise Exception("User is not logged in")
        return MessageController().get_messages_received(requesterID)

    def getAllNotifications(self, requesterID):
        if not self.checkIfUserIsLoggedIn(requesterID):
            raise Exception("User is not logged in")
        return MessageController().get_notifications(requesterID)


    def readMessage(self, requesterID, messageID):
        if not self.checkIfUserIsLoggedIn(requesterID):
            raise Exception("User is not logged in")
        return MessageController().read_message(requesterID, messageID)

    def deleteMessage(self, requesterID, messageID):
        return MessageController().delete_message(requesterID, messageID)


    # ==================  Notifications  ==================#

    def sendNotificationToUser(self, receiverID, subject, content, creation_date):
        # with purchase form AliExpress to user
        if not self.members.keys().__contains__(receiverID):
            raise Exception("no such member exists")
        return MessageController().send_notification(receiverID, subject, content, creation_date)


    def sendNotificationToStore(self, storeID, subject, content, creation_date):
        # with purchase form AliExpress to store's founder
        if not self.stores.keys().__contains__(storeID):
            raise Exception("no such store exists")
        founder = self.getStoreFounder(storeID)
        return MessageController().send_notification(founder, subject, content, creation_date)


    def getAllNotificationsReceived(self, requesterID):
        if not self.checkIfUserIsLoggedIn(requesterID):
            raise Exception("User is not logged in")
        return MessageController().get_notifications(requesterID)


    def readNotification(self, requesterID, notificationID):
        if not self.checkIfUserIsLoggedIn(requesterID):
            raise Exception("User is not logged in")
        return MessageController().read_notification(requesterID, notificationID)
    
    def deleteNotification(self, requesterID, notificationID):
        return MessageController().delete_notification(requesterID,notificationID)


    # def messageAsAdminToUser(self, admin_name, receiverID, message):
    #     pass
    #
    # def messageAsAdminToStore(self, admin_name, store_Name, message):
    #     pass
    def getStoreFounder(self, store_name):
        if self.stores.keys().__contains__(store_name):
            return self.stores[store_name].getFounder().get_username()
        else:
            raise Exception("no such store exists")
