from ProjectCode.Domain.ExternalServices.MessageController import MessageController
from ProjectCode.Domain.ExternalServices.TransactionHistory import TransactionHistory
from ProjectCode.Domain.Helpers.TypedDict import TypedDict
#-------Data MarketObjects Imports-------#
from ProjectCode.Domain.DataObjects.DataBasket import DataBasket
from ProjectCode.Domain.DataObjects.DataCart import DataCart
from ProjectCode.Domain.DataObjects.DataGuest import DataGuest
from ProjectCode.Domain.DataObjects.DataBid import DataBid
from ProjectCode.Domain.DataObjects.DataLottery import DataLottery
from ProjectCode.Domain.DataObjects.DataProduct import DataProduct
from ProjectCode.Domain.DataObjects.DataStore import DataStore
from ProjectCode.Domain.DataObjects.DataAccess import DataAccess
from ProjectCode.Domain.DataObjects.DataMember import DataMember
from ProjectCode.Domain.DataObjects.DataAdmin import DataAdmin
from ProjectCode.Domain.DataObjects.DataAuction import DataAuction
#-------MarketObjects Imports-------#
from ProjectCode.Domain.MarketObjects.Access import Access
from ProjectCode.Domain.MarketObjects.Bid import Bid
from ProjectCode.Domain.ExternalServices.PasswordService import PasswordValidationService
from ProjectCode.Domain.MarketObjects.Cart import Cart
from ProjectCode.Domain.MarketObjects.Store import Store
from ProjectCode.Domain.MarketObjects.StoreObjects.Auction import Auction
from ProjectCode.Domain.MarketObjects.StoreObjects.Product import Product
from ProjectCode.Domain.MarketObjects.User import User
from ProjectCode.Domain.MarketObjects.UserObjects.Admin import Admin
from ProjectCode.Domain.MarketObjects.UserObjects.Guest import Guest
from ProjectCode.Domain.MarketObjects.UserObjects.Member import Member
import asyncio


class StoreFacade:
    def __init__(self):
        # Store Data
        self.purchase_lock = asyncio.Lock()
        self.admins = TypedDict(str, Admin)  # dict of admins
        self.members = TypedDict(str, Member)    # dict of members
        self.onlineGuests = TypedDict(str, Guest)  # dict of users
        self.stores = TypedDict(str, Store)  # dict of stores
        self.online_members = TypedDict(str, Member) # dict from username to online members
        # Services
        self.message_controller = MessageController()  # Messanger
        # Data
        self.accesses = TypedDict(str, Access)  # optional TODO check key type
        self.nextEntranceID = 0  # guest ID counter
        self.bid_id_counter = 0  # bid counter
        # Admin
        first_admin: Admin = Admin("Ari", "123", "arioshryz@gmail.com")
        first_admin.logInAsAdmin() # added by rubin to prevent deadlock
        self.admins["Ari"] = first_admin
        # load data
        self.loadData()


# ------  System  ------ #
    def loadData(self):  # todo complete
        pass

# ------  users  ------ #
    #  Guests
    # Login from Guest to Member, this login is not from the main login screen. and from the state of a guest to Member

    def logInFromGuestToMember(self, entrance_id, user_name, password):
        password_validator = PasswordValidationService()
        guest: Guest = self.onlineGuests.get(entrance_id)
        # guest_cart: Cart = guest.get_cart()
        if self.members.keys().__contains__(user_name):
            existing_member: Member = self.members[user_name]
            if password_validator.ConfirmePassword(password, existing_member.get_password()):
                existing_member.logInAsMember()
                existing_member.setEntranceId(guest.entrance_id) # it's the same entrance id
              #  existing_member.addGuestProductsToMemberCart(guest_cart) # TODO: do I need it?
                self.online_members[existing_member.get_username()] = existing_member # keeping track who's online
                self.leaveAsGuest(entrance_id)  # he isn't a guest anymore
                return DataMember(existing_member)
            else:
                raise Exception("username or password does not match")
        else:
            raise Exception("username or password does not match")

    def exitTheSystem(self): #TODO: @Ari and @Yoav should decide if we need this function
        pass

    # Getting an admin from the admins
    def __getAdmin(self, user_name):
        if self.admins.keys().__contains__(user_name):
            return self.admins[user_name]
        else:
            raise Exception("admin does not exists")

    # regular guest entrance
    def loginAsGuest(self):
        new_guest = Guest(self.nextEntranceID)
        self.onlineGuests[str(self.nextEntranceID)] = new_guest
        self.nextEntranceID += 1
        return DataGuest(new_guest)

    # will be called when a member wants to log out, and gets a Guest status again.
    def returnToGuest(self, entrance_id):
        guest: Guest = Guest(entrance_id)
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

    def checkIfUserIsLoggedIn(self, user_name):
        return self.online_members.__contains__(user_name)


    # user_name could be an entranceID or username, depends on what it is it will return the correct User
    def __getUserOrMember(self, user_name):  #TODO: change the if's because checking the keys somehow dosent work
        if self.members.keys().__contains__(str(user_name)):
            if self.online_members.__contains__(str(user_name)):
                return self.members.get(user_name)
            else:
                raise Exception("user is not logged in")
        else:
            if self.onlineGuests.keys().__contains__(str(user_name)):
                return self.onlineGuests.get(user_name)
            else:
                raise Exception("user is not guest nor a member")

    # gets an online member.
    def __getOnlineMemberOnly(self, user_name):
        if self.online_members.keys().__contains__(user_name):
            return self.online_members.get(user_name)
        else:
            raise Exception("user is not logged in")

    # Registers a guest, register doesn't mean the user is logged in
    def register(self, user_name, password, email):
        password_validator = PasswordValidationService()
        if not self.members.keys().__contains__(str(user_name)):
            if password_validator.ValidatePassword(password):
                new_member: Member = Member(str(0), user_name, password, email)
                self.members[str(user_name)] = new_member
                return new_member
        else:
            raise Exception("This username is already in the system")

    #  only members

    # Login straight to Member and not as guest from the home logging screen.
    def logInAsMember(self, username, password):
        password_validator = PasswordValidationService()
        # check if the user is an admin
        if self.admins.keys().__contains__(username):
            return self.logInAsAdmin(username, password)
        # check if the member is an actual user
        if self.members.keys().__contains__(username):
            if not self.online_members.__contains__(username):
                existing_member: Member = self.members[username]
                if password_validator.ConfirmPassword(password, existing_member.get_password()):
                    existing_member.logInAsMember()
                    existing_member.setEntranceId(self.nextEntranceID)
                    self.nextEntranceID += 1
                    self.online_members[username] = existing_member  # indicates that the user is logged in
                    return DataMember(existing_member)
                else:
                    raise Exception("username or password does not match")
            else:
                raise Exception("user is already logged in")
        else:
            raise Exception("username or password does not match")

    #  only members

    # logout a member
    def logOut(self, username):
        if self.members.keys().__contains__(username):
            existing_member: Member = self.members[username]
            del self.online_members[username] # deletes the user from the online users
            guest: Guest = self.returnToGuest(str(existing_member.get_entrance_id()))  # returns as a guest

            return guest
        else:
            raise Exception("Logout is not an option")

    #  only members
    # getting the user purchase history
    def getMemberPurchaseHistory(self, username):
        transaction_history = TransactionHistory()
        if self.checkIfUserIsLoggedIn(username):
            return transaction_history.get_User_Transactions(username)
        else:
            raise Exception("username isn't logged in")

    # guest and member
    # getting a User's basket
    def getBasket(self, user_name, store_name):
        user = self.__getUserOrMember(user_name)
        requested_basket = user.get_Basket(store_name)
        return DataBasket(requested_basket)

    # guest and member
    # getting a Users cart
    def getCart(self, username):
        user: User = self.__getUserOrMember(username)
        requested_cart = user.get_cart()
        return DataCart(requested_cart)

    # guest and member
    # adding a product to basket, checking with store if the item is available
    def addToBasket(self, username, store_name, product_id, quantity):
        user: User = self.__getUserOrMember(username)
        store: Store = self.stores.get(store_name)
        if store is None:
            raise Exception("Store doesnt exists")
        product = store.checkProductAvailability(product_id, quantity)
        if product is not None:
            user.add_to_cart(username, store_name, product_id, product, quantity)
        else:
            raise Exception("Product is not available or quantity is higher than the stock")

    # guest and member
    # deleting an item from a basket, if the item exists there
    def removeFromBasket(self, username, store_name, product_id):
        user: User = self.__getUserOrMember(username)
        remove_success = user.removeFromBasket(store_name, product_id)
        if remove_success:
            return remove_success
        else:
            raise Exception("there was a problem with removing the item or either the item doesnt exists in the basket")

    # guest and member
    # editing aa product quantity from a specific basket
    def editBasketQuantity(self, username, store_name, product_id, quantity):
        user: User = self.__getUserOrMember(username)
        answer = user.checkProductExistance(store_name, product_id) #answer is boolean
        if answer:
            store: Store = self.stores[store_name]
            product = store.checkProductAvailability(product_id, quantity)
            if product is not None:
                user.edit_Product_Quantity(store_name, product_id, quantity)
            else:
                raise Exception("Product is not available or quantity is higher than the stock")
        else:
            raise Exception("product does not exists in the basket")

    # guest and member
    # getting all the items in the cart and makes a purchase, adding all the items to the Member history and the store's
    def purchaseCart(self, user_name, card_number, card_user_name, card_user_id, card_date, back_number, address):
        user: User = self.__getUserOrMember(user_name)
        if self.online_members.__contains__(user_name):
            user.get_cart().PurchaseCart(card_number, card_user_name, card_user_id, card_date, back_number, address, True, self.purchase_lock)
        else:
            user.get_cart().PurchaseCart(card_number, card_user_name, card_user_id, card_date, back_number, address, False, self.purchase_lock)

    # Bids! -------------------------------------- Bids are for members only --------------------------------------
    def placeBid(self, username, store_name, offer, product_id, quantity):
        existing_member: Member = self.__getOnlineMemberOnly(username)
        bid: Bid = Bid(self.bid_id_counter, username, store_name, offer, product_id, quantity)
        self.bid_id_counter += 1
        existing_member.addBidToBasket(bid)
        store: Store = self.stores[store_name]
        store.requestBid(bid)
        return DataBid(bid)

    def getAllBidsFromUser(self, username):
        existing_member: Member = self.__getOnlineMemberOnly(username)
        bids_set = existing_member.getAllBids()  # returns set of bids
        data_bids_list = [DataBid(bid) for bid in bids_set]
        return data_bids_list

    def purchaseConfirmedBid(self, username, store_name, bid_id, card_number, card_user_name, card_user_id, card_date,
                             back_number):
        existing_member: Member = self.__getOnlineMemberOnly(username)
        existing_member.get_cart().purchaseConfirmedBid(store_name, bid_id, card_number, card_user_name, card_user_id,
                                                        card_date, back_number, self.purchase_lock)

    def placeOfferInAuction(self, username, storename, auction_id, offer):
        cur_member: Member = self.__getOnlineMemberOnly(username)
        cur_store: Store = self.stores.get(storename)
        if cur_store is None:
            raise Exception("No such store exists")
        cur_auction: Auction = cur_store.placeOfferInAuction(username, auction_id, offer)
        cur_member.addNewAuction(auction_id, cur_auction)
        return DataAuction(cur_auction)

    def participateInLottery(self, store_name, user_name, lottery_id, share):
        cur_store: Store = self.stores.get(store_name)
        cur_member: Member = self.__getOnlineMemberOnly(user_name)
        if cur_store is None:
            raise Exception("No such store exists")
        cur_lottery = cur_store.checkLotteryParticipationShare(lottery_id, share)
        cur_lottery.add_participant_share(cur_member, share)
        cur_store.participateInLottery(lottery_id, share)
        # TODO: Ari: implement payment for the requested share
        cur_member.addNewLottery(lottery_id, cur_lottery)

    def ClaimAuctionPurchase(self, username, storename, auction_id, card_number, card_user_name, card_user_ID, card_date, back_number):
        cur_member: Member = self.__getOnlineMemberOnly(username)
        cur_store: Store = self.stores.get(storename)
        if cur_store is None:
            raise Exception("No such store exists")
        cur_member.claimAuctionPurchase()
        cur_auction: Auction = cur_member.getAuctionById(auction_id)
        if cur_auction.get_highest_offer_username() == cur_member.get_username():
            product: Product = cur_store.get_products().get(cur_auction.get_product_id())
            item_name = product.name
            tuple_for_history = (item_name, 1) # name of item and quantity for the history of the store
            cur_store.purchaseAuctionProduct(auction_id)
            self.payment_service.pay(storename, card_number, card_user_name, card_user_ID, card_date,
                                       back_number, cur_auction.get_current_offer())
            self.transaction_history.addNewStoreTransaction(username, storename, tuple_for_history,
                                                            cur_auction.get_current_offer())

            dict_for_history = TypedDict(str, tuple)
            dict_for_history[storename] = tuple_for_history
            self.transaction_history.addNewUserTransaction(username, dict_for_history, cur_auction.get_current_offer())
            for member in cur_auction.get_participants():
                member.removeAuctionById(auction_id)



    # ------  stores  ------ #

    def getStores(self):
        return self.stores

    def getProductsByStore(self, store_name, username):
        cur_store: Store = self.stores.get(store_name) #TODO: change to "try and expect" instead of "if" because the first line returns exception
        if cur_store is None:
            raise Exception("No such store exists")
        #Generate data dict
        data_products = dict()
        product_dict = cur_store.getProducts(username)
        for key, value in product_dict:
            data_products[key] = DataProduct(value)
        return data_products

    def getProduct(self, store_name, product_id, username):
        cur_store: Store = self.stores.get(store_name)
        if cur_store is None:
            raise Exception("No such store exists")
        cur_product = cur_store.getProductById(product_id, username)
        return DataProduct(cur_product)

    def productSearchByName(self, keywords, username):  # and keywords
        splitted_keywords = keywords.split(" ")
        search_results = TypedDict(DataStore, list)
        for keyword in splitted_keywords:
            for cur_store in self.stores.values():
                product_list = cur_store.searchProductByName(keyword, username)
                if len(product_list) > 0:
                    data_product_list = [DataProduct(prod) for prod in product_list]
                    search_results[DataStore(cur_store)] = data_product_list #TODO: notice product_list type isnt List[Product] therfore TypedDict returns an error
        return search_results

    def productSearchByCategory(self, category, username):
        search_results = TypedDict(DataStore, list)
        for cur_store in self.stores.values():
            product_list = cur_store.searchProductByCategory(category, username)
            if len(product_list) > 0:
                data_product_list = [DataProduct(prod) for prod in product_list]
                search_results[DataStore(cur_store)] = data_product_list
        return search_results

    def productFilterByFeatures(self, featuresDict, username):
        #TODO: not implemented yet
        return []

    def getStorePurchaseHistory(self, user_name, store_name):
        #TODO: amiel check accesses for the username if he has access to the store
        transaction_history = TransactionHistory()
        return transaction_history.get_Store_Transactions(store_name)

    # ------  Management  ------ #
    #TODO: add check if user is loggedin to each function

    def openStore(self, username, store_name):
        cur_member: Member = self.members.get(username)
        if cur_member is None:
            raise Exception("The user is not a member")
        if not self.checkIfUserIsLoggedIn(username):
            raise Exception("User is not logged in")
        cur_store = Store(store_name)
        new_access = Access(cur_store, cur_member, username)
        cur_member.accesses[store_name] = new_access
        cur_store.setFounder(cur_member.get_username(), new_access)
        self.stores[store_name] = cur_store
        return DataStore(cur_store)

    def addNewProductToStore(self, username, store_name, name, quantity, price, categories):

        if not self.checkIfUserIsLoggedIn(username):
            raise Exception("User is not logged in")
        cur_store: Store = self.stores.get(store_name)
        if cur_store is None:
            raise Exception("No such store exists")
        #cur_member: Member = self.members[str(requester_id)]
        member = self.members[username]
        new_product = cur_store.addProduct(member.get_accesses().get(store_name), name, quantity, price, categories) #TODO: change first atribute to access
        return DataProduct(new_product)

    def removeProductFromStore(self, username, store_name, product_id):
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
        if not self.checkIfUserIsLoggedIn(username):
            raise Exception("User is not logged in")
        cur_store: Store = self.stores[store_name]
        if cur_store is None:
            raise Exception("No such store exists")
        cur_access = self.members[username].get_accesses().get(store_name)
        if cur_access is None:
            raise Exception("The member doesn't have a permission for that action")
        changed_product = cur_store.changeProduct(cur_access, product_id, **kwargs)
        return DataProduct(changed_product)

    def nominateStoreOwner(self, requester_username, nominated_username, store_name):
        if not self.checkIfUserIsLoggedIn(requester_username):
            raise Exception("User is not logged in")
        cur_store: Store = self.stores[store_name]
        if cur_store is None:
            raise Exception("No such store exists")
        nominated_access = self.members[nominated_username].get_accesses().get(store_name)
        if nominated_access is None:
            nominated_access = Access(cur_store,self.members[nominated_username],requester_username)
            self.members[nominated_username].get_accesses()[store_name] = nominated_access
        nominated_modified_access = cur_store.setAccess(nominated_access, requester_username, nominated_username, "Owner")
        return DataAccess(nominated_modified_access)

    def nominateStoreManager(self, requester_username, nominated_username, store_name):
        cur_store: Store = self.stores[store_name]
        if not self.checkIfUserIsLoggedIn(requester_username):
            raise Exception("User is not logged in")
        if cur_store is None:
            raise Exception("No such store exists")
        nominated_access = self.members[nominated_username].get_accesses().get(store_name)
        if nominated_access is None:
            nominated_access = Access(cur_store, self.members[nominated_username], requester_username)
            self.members[nominated_username].get_accesses()[store_name] = nominated_access
        nominated_modified_access = cur_store.setAccess(nominated_access, requester_username, nominated_username,
                                                        "Manager")
        return DataAccess(nominated_modified_access)

    def addPermissionsForManager(self):
        pass

    def editPermissionsForManager(self):
        pass


    def approveBid(self, username, storename, bid_id):
        if not self.checkIfUserIsLoggedIn(username):
            raise Exception("User is not logged in")
        cur_store: Store = self.stores[storename]
        if cur_store is None:
            raise Exception("No such store exists")
        if not self.checkIfUserIsLoggedIn(username):
            raise Exception("User is not logged in")
        if self.members[username] is None:
            raise Exception("No such member exists")
        approved_bid = cur_store.approveBid(username, bid_id)
        return DataBid(approved_bid)

    def rejectBid(self, username, storename, bid_id):
        if not self.checkIfUserIsLoggedIn(username):
            raise Exception("User is not logged in")
        cur_store: Store = self.stores[storename]
        if cur_store is None:
            raise Exception("No such store exists")
        if not self.checkIfUserIsLoggedIn(username):
            raise Exception("User is not logged in")
        if self.members[username] is None:
            raise Exception("No such member exists")
        rejected_bid = cur_store.rejectBid(username,bid_id)
        return DataBid(rejected_bid)

    def sendAlternativeBid(self, username, storename, bid_id, alternate_offer):
        if not self.checkIfUserIsLoggedIn(username):
            raise Exception("User is not logged in")
        cur_store: Store = self.stores[storename]
        if cur_store is None:
            raise Exception("No such store exists")
        if not self.checkIfUserIsLoggedIn(username):
            raise Exception("User is not logged in")
        if self.members[username] is None:
            raise Exception("No such member exists")
        alternative_bid = cur_store.sendAlternativeBid(username, bid_id, alternate_offer)
        return DataBid(alternative_bid)


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
        new_auction = cur_store.startAuction(username,product_id,starting_price,duration)
        return DataAuction(new_auction)






    def addLottery(self, username, storename, product_id):
        if not self.checkIfUserIsLoggedIn(username):
            raise Exception("User is not logged in")
        cur_store: Store = self.stores.get(storename)
        if cur_store is None:
            raise Exception("No such store exists")
        if self.members.get(username) is None:
            raise Exception("No such member exists")
        if not self.checkIfUserIsLoggedIn(username):
            raise Exception("User is not logged in")
        new_lottery = cur_store.startLottery(username, product_id)
        return DataLottery(new_lottery)



    def closeStore(self, username, store_name):
        if not self.checkIfUserIsLoggedIn(username):
            raise Exception("User is not logged in")
        cur_store: Store = self.stores.get(store_name)
        if cur_store is None:
            raise Exception("No such store exists")
        cur_store.setStoreStatus(False, username)
        # if is_founder:
        #     #deletes all accesses for that store
        #     for mem in self.members.values():
        #         store_exists = mem.get_accesses().get(store_name)
        #         if store_exists is not None:
        #             del mem.get_accesses()[store_name]
        #
        #     del self.stores[store_name]
        return DataStore(cur_store)

    def getStaffInfo(self, username, store_name):
        if not self.checkIfUserIsLoggedIn(username):
            raise Exception("User is not logged in")
        cur_store: Store = self.stores[store_name]
        if cur_store is None:
            raise Exception("No such store exists")
        accesses_dict = cur_store.getStaffInfo(username)
        #Generate accesses data objects
        data_accesses_dict = dict()
        for key,value in accesses_dict.items():
            data_accesses_dict[key] = DataAccess(value)
        return data_accesses_dict

    def getStoreManagerPermissions(self):
        pass

    # ------  Admins  ------ #
    def logInAsAdmin(self,username, password):
        if self.admins.keys().__contains__(username):
            existing_admin: Admin = self.admins[username]
            if self.password_validator.ConfirmePassword(password, existing_admin.get_password()):
                existing_admin.logInAsAdmin()
                return DataAdmin(existing_admin)
            else:
                raise Exception("admin name or password does not match")
        else:
            raise Exception("admin name or password does not match")

    def logOutAsAdmin(self, user_name):
        if self.admins.keys().__contains__(user_name):
            existing_admin: Admin = self.members[user_name]
            existing_admin.logOffAsAdmin()


    def messageAsAdmin(self, admin_name, message, receiver_user_name):
        pass # no messanger this version

    def closeStoreAsAdmin(self, admin_name, store_name):
        if self.admins.keys().__contains__(admin_name):
            pass #  TODO: logic of closing a store as an admin amiel!

    def addAdmin(self, username, newAdminName, newPassword, newEmail):
        if self.admins.keys().__contains__(username):
            if self.password_validator.ValidatePassword(newPassword):
                new_admin = Admin(newAdminName, newPassword, newEmail)
                self.admins[newAdminName] = new_admin
                return DataAdmin(new_admin)
            else:
                raise Exception("password is too weak")

    def getAllOnlineMembers(self, user_name):
        if self.admins.__contains__(user_name):
            member_list = []
            for member in self.online_members.values():
                member_list.insert(DataMember(member))
            return member_list
        else:
            raise Exception("only admin can get the online members list")



