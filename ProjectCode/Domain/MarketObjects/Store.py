import datetime
from typing import List

from ProjectCode.DAL.StoreModel import StoreModel
from ProjectCode.Domain.Helpers.JsonSerialize import JsonSerialize
from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.MarketObjects.Access import Access
from ProjectCode.Domain.MarketObjects.Bid import Bid
from ProjectCode.Domain.MarketObjects.StoreObjects.Auction import Auction
from ProjectCode.Domain.MarketObjects.StoreObjects.DiscountPolicy import DiscountPolicy
from ProjectCode.Domain.MarketObjects.StoreObjects.Lottery import Lottery
from ProjectCode.Domain.MarketObjects.StoreObjects.Product import Product
from ProjectCode.Domain.MarketObjects.StoreObjects.PurchasePolicies import PurchasePolicies
import random

# ----- REPOSITORIES ----- #
from ProjectCode.Domain.Repository.ProductRepository import ProductRepository
from ProjectCode.Domain.Repository.AccessRepository import AccessRepository


class Store:


    def __init__(self, store_name, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        # self.__store_name = store_name
        # self.__products = TypedDict(int, Product)
        # # TODO: policies
        # self.active: bool = True
        # self.closed_by_admin: bool = False
        # self.__accesses = TypedDict(str, Access)
        # self.product_id_counter = 0
        # self.auction_id_counter = 0
        # self.lottery_id_counter = 0
        # self.__bids = TypedDict(int, Bid)
        # self.__bids_requests = TypedDict(str, List[Bid])
        # self.__auctions = TypedDict(int, Auction)
        # self.__lotteries = TypedDict(int, Lottery)
        # self.__discount_policy = DiscountPolicy(store_name)
        # self.__purchase_policy = PurchasePolicies()

        super().__init__(*args, **kwargs)
        self.__store_name = store_name
        self.__products = ProductRepository(store_name)
        # TODO: policies
        self.active: bool = True
        self.closed_by_admin: bool = False
        self.__accesses = AccessRepository(store_name=store_name)
        self.product_id_counter = 0
        self.auction_id_counter = 0
        self.lottery_id_counter = 0
        self.__bids = TypedDict(int, Bid)
        self.__bids_requests = TypedDict(str, List[Bid])
        self.__auctions = TypedDict(int, Auction)
        self.__lotteries = TypedDict(int, Lottery)
        self.__discount_policy = DiscountPolicy(store_name)
        self.__purchase_policy = PurchasePolicies()

        #REPOSITORY FIELDS --- TO BE REPLACED
        # self.accesses_test = AccessRepository(store_name=store_name)
        # self.prods = ProductRepository(store_name)


    def __eq__(self, other):
        return self.__store_name == other.get_store_name()

    def setStoreStatus(self, status, requester_username):
        cur_access: Access = self.__accesses[requester_username]
        if cur_access is None:
            raise Exception("No such access exists in the store")
        cur_access.canChangeStatus()
        if status == self.active:
            raise Exception("store is already open or closed")
        self.active = status

    #-------------Permissions----------------#

    def setFounder(self, username, access):
        access.setAccess("Founder")
        self.__accesses[username] = access

    def getFounder(self):
        for access in self.__accesses.values():
            if access.hasRole("Founder"):
                return access.get_user()
        return None

    def getOwners(self):
        owners = []
        for access in self.__accesses.values():
            if access.hasRole("Owner"):
                owners.append(access.get_user())
        return owners

    def setAccess(self, nominated_access, requester_username, nominated_username, role):
        requester_access: Access = self.__accesses[requester_username]
        if requester_access is None:
            raise Exception("The member doesn't have the access for that store")
        if self.__accesses[nominated_username] is not None and self.__accesses[nominated_username].hasRole(role):
            raise Exception("The member already has that role")
        if requester_access.canModifyPermissions() and requester_username == nominated_access.get_nominated_by_username():
            nominated_access.setAccess(role)
            requester_access.addNominatedUsername(nominated_username, nominated_access)
            self.__accesses[nominated_username] = nominated_access
            self.__accesses[requester_username] = requester_access #update
            return nominated_access
        else:
            raise Exception("Member doesn't have the permission in this store")


    def removeAccess(self,to_be_removed_username, requester_username):
        requester_access: Access = self.__accesses[requester_username]
        to_be_removed_access: Access = self.__accesses[to_be_removed_username]
        if requester_access is None or to_be_removed_access is None:
            raise Exception("No such access exists")
        if requester_access.canModifyPermissions() and requester_username == to_be_removed_access.get_nominated_by_username():
            requester_access.get_nominations().pop(to_be_removed_username)
            removed_usernames = self.__removeAllAccesses(to_be_removed_access)
            return removed_usernames
        else:
            raise Exception("User doesn't have the permission to remove this access")


    def __removeAllAccesses(self, to_be_removed_access):
        cur_access: Access = to_be_removed_access
        accesses_to_remove = [to_be_removed_access]
        usernames_to_remove = []
        while len(accesses_to_remove) > 0:
            cur_access = accesses_to_remove[0]
            self.__accesses.remove(cur_access.get_user().get_username())
            usernames_to_remove.extend(cur_access.get_nominations())
            accesses_to_remove.remove(cur_access)
            pulled_accesses = [self.__accesses.get(username) for username in cur_access.get_nominations()]
            accesses_to_remove.extend(pulled_accesses)
        return usernames_to_remove

    def modifyPermission(self, requester_username, nominated_username, permission, op="ADD"):
        requester_access: Access = self.__accesses.get(requester_username)
        nominated_access: Access = self.__accesses.get(nominated_username)
        if requester_access is None or nominated_access is None:
            raise Exception("No such access exists")
        if requester_access.canModifyPermissions() and nominated_access.get_nominated_by_username() == requester_username:
            if op == "ADD":
                nominated_access.get_access_state().addPermission(permission)
            else:
                nominated_access.get_access_state().removePermission(permission)
        return nominated_access

    def getPermissions(self, requester_username, nominated_username):
        requester_access: Access = self.__accesses.get(requester_username)
        nominated_access: Access = self.__accesses.get(nominated_username)
        if requester_access is None or nominated_access is None:
            raise Exception("No such access exists")
        if requester_username == nominated_username or requester_username == nominated_access.get_nominated_by_username():    
            return requester_access.get_access_state().get_permissions()
        else:
            raise Exception("You dont have access to get this user permission")

    # Get personal permissions for a given store
    def getPermissionsAsJson(self, requester_username):
        requester_access: Access = self.__accesses.get(requester_username)
        if requester_access is None:
            return {}
        else:
            return requester_access.get_access_state().get_permissionsAsJson()

    def addProduct(self, access, name, quantity, price, categories):
        access.canChangeProducts()
        if name == "":
            raise Exception("product name cannot be empty")
        self.inc_product_id_counter()
        product_to_add = Product(self.product_id_counter, name, quantity, price, categories)
        self.__products.__setitem__(self.product_id_counter, product_to_add)
        return product_to_add

    def deleteProduct(self, access, product_id):
        product_id = int(product_id)
        access.canChangeProducts()
        if self.__products.get(product_id) is None:
            raise Exception("Product doesn't exists")
        else:
            self.__products.__delitem__(product_id)
            return product_id

    def changeProduct(self, access, product_id, **kwargs):
        access.canChangeProducts()
        cur_product: Product = self.__products.get(product_id)
        if cur_product is None:
            raise Exception("Product doesn't exists")
        for k, v in kwargs.items():
            try:
                getattr(cur_product, k)
            except AttributeError:
                raise Exception("No such attribute exists")
            self.checkValue(v)
            setattr(cur_product, k, v)
        self.__products[product_id] = cur_product
        return cur_product

    # TODO: may cause problem for unknown reasons
    def modify_attributes(self, object_to_modify, **kwargs):
        for k, v in kwargs.items():
            try:
                getattr(object_to_modify, k)
            except AttributeError:
                raise Exception("No such attribute exists")
            setattr(object_to_modify, k, v)
        return object_to_modify

    # def closeStore(self, requester_username):
    #     cur_access = self.__accesses[requester_username]
    #     if cur_access.isFounder:
    #         return True
    #     else:
    #         raise Exception("Member isn't the founder of the store")

    def getProducts(self, username):
        cur_access: Access = self.__accesses.get(username)
        if not self.active:
            if (cur_access is not None) and cur_access.hasRole():
                return self.__products
            else:
                raise Exception("Store is inactive")
        return self.__products

    def getProductById(self, product_id,  username):
        cur_access: Access = self.__accesses.get(username)
        if not self.active:
            if (cur_access is not None) and cur_access.hasRole():
                if self.__products.keys().__contains__(product_id):
                    return self.__products.get(product_id)
                else:
                    raise Exception("Product does not Exist")
            raise Exception("Store is inactive")
        if not self.__products.keys().__contains__(product_id):
            raise Exception("Product does not Exist")
        return self.__products.get(product_id)

    def getStaffInfo(self, username):
        cur_access: Access = self.__accesses[username]
        if cur_access is None:
            raise Exception("Member has no access for that store")
        if not cur_access.canViewStaffInformation():
            raise Exception("You have no permission to view staff information")
        return self.__accesses


    def checkProductAvailability(self, product_id, quantity):
        cur_product : Product = self.__products[int(product_id)]
        if cur_product is None:
            raise Exception("No such product exists")
        if int(cur_product.quantity) - int(quantity) < 0:
            raise Exception("There is not enough stock of the requested product")
        if quantity < 0:
            raise Exception("quantity can't be under zero")
        return cur_product

    def searchProductByName(self, keyword):
        #cur_access: Access = self.__accesses[username]
        if not self.active: #and ( cur_access is None or not cur_access.hasRole()):
            return []

        product_list = []
        for prod in self.__products.values():
            if keyword in prod.name:
                product_list.append(prod)
        return product_list

    def searchProductByCategory(self, category):
        if category == "":
            raise Exception("category cannot be empty")
        #cur_access: Access = self.__accesses[username]
        if not self.active: #and (cur_access is None or not cur_access.hasRole()):
            return {}
        product_list = []
        for prod in self.__products.values():
            if category in prod.categories:
                product_list.append(prod)
        return product_list


    def calculateBasketPrice(self, products_dict): #tup(product,qunaiity)
        #need to add a user arguments so we will be able to check policies
        new_product_dict = TypedDict(int, int) # (id,quantity)
        for product_id, product_tuple in products_dict.items():
            new_product_dict[product_id] = product_tuple[1]
        overall_price = 0
        price_after_discounts = 0
        for product_id, product_quantity in new_product_dict.items():
            cur_product = self.__products[product_id]
            if cur_product is None:
                raise Exception("No such product exists")
            overall_price += cur_product.price * product_quantity

        for product_id, product_quantity in new_product_dict.items():
            cur_product: Product = self.__products[product_id]
            price_after_discounts += product_quantity * self.getProductPriceAfterDiscount(cur_product, new_product_dict,
                                                                                          overall_price)
        return price_after_discounts

    def checkBasketValidity(self, basket, product_to_add, quantity):
        relevant_product_info = dict()
        for product_id, product_tuple in basket.items():
            relevant_product_info[product_id] = product_tuple[1]
        relevant_product_info[product_to_add.get_product_id()] = quantity
        overall_price = self.calculateBasketBasePrice(relevant_product_info)
        #TODO: last argument suppose to be a user, need to figure out how to get it
        return self.__purchase_policy.checkAllPolicies(product_to_add, relevant_product_info, overall_price)

    def calculateProductPriceAfterDiscount(self, product, basket, quantity):
        relevant_product_info = dict()
        for product_id, product_tuple in basket.items():
            relevant_product_info[product_id] = product_tuple[1]
        overall_price = self.calculateBasketBasePrice(relevant_product_info)
        price_after_discount = self.getProductPriceAfterDiscount(product, relevant_product_info, overall_price)
        return (product, quantity, price_after_discount)

    def calculateBasketBasePrice(self, products_dict): #tup(product,qunaiity)
        overall_price = 0
        for product_id, quantity in products_dict.items():
            overall_price += self.__products[product_id].get_price() * quantity
        return overall_price


    def purchaseBasket(self, products_dict): #tup(product,qunaiity)
        #need to add a user arguments so we will be able to check policies
        new_product_dict = TypedDict(int, int) # (id,quantity)
        for product_id, product_tuple in products_dict.items():
            new_product_dict[product_id] = product_tuple[1]

        overall_price = 0
        price_after_discounts = 0
        for product_id, product_quantity in new_product_dict.items():
            cur_product = self.__products[product_id]
            if cur_product is None:
                raise Exception("No such product exists")
            cur_product.quantity -= product_quantity
            overall_price += cur_product.price * product_quantity

        for product_id, product_quantity in new_product_dict.items():
            cur_product: Product = self.__products[product_id]
            price_after_discounts += product_quantity * self.getProductPriceAfterDiscount(cur_product, new_product_dict, overall_price)
        return price_after_discounts


    def getProductPriceAfterDiscount(self, product, product_quantity_dict, overall_price):
        cur_percent = self.__discount_policy.calculateDiscountForProduct(product, product_quantity_dict, overall_price)
        return product.get_price() - product.get_price() * (cur_percent / 100)

    def addDiscount(self, username, discount_type, percent=0, level="", level_name="", rule={}, discounts={}):
        cur_access: Access = self.__accesses.get(username)
        if cur_access is None:
            raise Exception("No such access exists")
        if not self.__products.__contains__(level_name):
            raise Exception("no such product exists")
        cur_access.canManageDiscounts()
        new_discount = self.__discount_policy.addDiscount(discount_type=discount_type, percent=percent, level=level,
                                           level_name=level_name, rule=rule, discounts=discounts)
        return new_discount

    def getDiscount(self, discount_id):
        return self.__discount_policy.getDiscount(discount_id)

    def getAllDiscounts(self):
        return self.__discount_policy.getAllDiscounts()

    def addPurchasePolicy(self,username, purchase_policy, rule, level="", level_name=""):
        cur_access: Access = self.__accesses.get(username)
        if cur_access is None:
            raise Exception("No such access exists")
        cur_access.canManagePolicies()
        new_policy = self.__purchase_policy.addPurchasePolicy(purchase_policy=purchase_policy, rule=rule,
                                                 level=level, level_name=level_name)
        return new_policy

    def getPolicy(self, policy_id):
        return self.__purchase_policy.getPurchasePolicy(policy_id)
    def requestBid(self, bid: Bid):
        self.__bids[bid.bid_id] = bid
        for access in self.__accesses.values():
            if access.canManageBids():
                username = access.get_user().get_username()
                if self.__bids_requests[username] is None:
                    self.__bids_requests[username] = []
                self.__bids_requests[username].append(bid)
                bid.increment_left_to_approve()

    def approveBid(self, username, bid_id):
        cur_access: Access = self.__accesses[username]
        cur_access.canManageBids()

        cur_bid: Bid = self.__bids[bid_id]
        if cur_bid is None:
            raise Exception("No such bid exists in the store")
        if cur_bid not in self.__bids_requests[username]:
            raise Exception("You already approved that bid")
        cur_bid.approve_by_one()
        self.__bids_requests[username].remove(cur_bid)
        if cur_bid.get_left_to_approval() == 0:
            cur_bid.set_status(1)
        return cur_bid

    def rejectBid(self, username, bid_id):
        cur_access: Access = self.__accesses[username]
        cur_access.canManageBids()
        cur_bid: Bid = self.__bids[bid_id]
        if cur_bid is None:
            raise Exception("No such bid exists in the store")
        for access_username, bid_list in self.__bids_requests.items():
            if cur_bid in bid_list:
                bid_list.remove(cur_bid)
        cur_bid.set_status(2)
        return cur_bid

    def sendAlternativeBid(self, username, bid_id, alternate_offer):
        cur_access: Access = self.__accesses[username]
        cur_access.canManageBids()
        cur_bid: Bid = self.__bids[bid_id]
        if cur_bid is None:
            raise Exception("No such bid exists in the store")
        cur_bid.set_offer(alternate_offer)
        cur_bid.set_status(3)

    def purchaseBid(self, bid_id):
        cur_bid: Bid = self.__bids.get(bid_id)
        if cur_bid is None:
            raise Exception("No such bid exists")
        if cur_bid.get_status() != 1 or cur_bid.get_left_to_approval() > 0:
            raise Exception("Bid is not approved by the store owners")
        cur_product: Product = self.__products.get(cur_bid.get_product())
        if cur_product is None:
            raise Exception("Product doesn't exists")
        cur_product.quantity -= cur_bid.get_quantity()
        del self.__bids[cur_bid]

    def startAuction(self, username, product_id, starting_price, duration):
        cur_access: Access = self.__accesses[username]
        cur_product = self.__products[int(product_id)]
        if cur_access is None:
            raise Exception("The user doesnt have access in this store")
        cur_access.canManageAuctions()
        if cur_product is None:
            raise Exception("No such product exists")
        self.auction_id_counter += 1
        start_date = datetime.datetime.now()
        expiration_date = start_date + datetime.timedelta(days=int(duration))
        new_auction = Auction(self.auction_id_counter, product_id, starting_price, starting_price, start_date,
                              expiration_date, username)
        self.__auctions[self.auction_id_counter] = new_auction
        return new_auction

    def purchaseAuctionProduct(self, auction_id):
        cur_auction: Auction = self.__auctions[auction_id]
        if cur_auction.get_expiration_date() < datetime.datetime.now():
            raise Exception("The auction didn't end yet")
        cur_product = self.__products[cur_auction.get_product_id()]
        cur_product.quantity -= 1

    def placeOfferInAuction(self, username, auction_id, offer):
        cur_auction: Auction = self.__auctions.get(auction_id)
        if cur_auction is None:
            raise Exception("No such auction exists")
        if cur_auction.get_expiration_date() < datetime.datetime.now():
            raise Exception("You cannot place an offer in a closed auction")
        if offer > cur_auction.get_current_offer():
            cur_auction.set_current_offer(offer)
            cur_auction.add_participant(username, offer)
            cur_auction.set_highest_offer_username(username)
        return cur_auction

    def startLottery(self, username, product_id):
        cur_product: Product = self.__products.get(product_id)
        if cur_product is None:
            raise Exception("No such product exists")
        cur_access: Access = self.__accesses.get(username)
        if cur_access is None:
            raise Exception("Member doesnt have access for this store")
        cur_access.canManageLottery()
        self.lottery_id_counter += 1
        new_lottery = Lottery(self.lottery_id_counter, product_id, cur_product.price, 0)
        self.__lotteries[self.lottery_id_counter] = new_lottery
        return new_lottery

    def participateInLottery(self, lottery_id, share):
        cur_lottery: Lottery = self.__lotteries.get(lottery_id)
        if cur_lottery is None:
            raise Exception("No such lottery exists")
        cur_lottery.set_accumulated_price(cur_lottery.get_accumulated_price() + share)
        if cur_lottery.get_accumulated_price() == cur_lottery.get_price():
            weights = [participant[1] for participant in cur_lottery.get_participants()]
            participants = [participant[0] for participant in cur_lottery.get_participants()]
            choices = random.choices(participants, weights, k=1)
            chosen = choices[0]
            cur_lottery.set_winner(chosen)
        return cur_lottery

    def checkLotteryParticipationShare(self, lottery_id, share):
        cur_lottery: Lottery = self.__lotteries.get(lottery_id)
        if cur_lottery is None:
            raise Exception("No such lottery exists")
        if cur_lottery.get_price() - cur_lottery.get_accumulated_price() < share:
            raise Exception("The requested share is too high")
        return cur_lottery

    def getAllStaffMembersNames(self):
        return self.get_accesses().keys()

    def inc_product_id_counter(self):
        self.product_id_counter += 1
        store_entry = StoreModel.get_by_id(self.__store_name)
        store_entry.product_id_counter = self.product_id_counter
        store_entry.save()

    def get_store_name(self):
        return self.__store_name

    def set_store_name(self, value):
        self.__store_name = value

    def get_products(self):
        return self.__products

    def set_products(self, value):
        self.__products = value

    def get_accesses(self):
        return self.__accesses

    def set_accesses(self, value):
        self.__accesses = value

    def get_bids(self):
        return self.__bids

    def set_bids(self, value):
        self.__bids = value

    def get_bids_requests(self):
        return self.__bids_requests

    def set_bids_requests(self, value):
        self.__bids_requests = value

    def get_auctions(self):
        return self.__auctions

    def set_auctions(self, value):
        self.__auctions = value

    def get_lottery(self):
        return self.__lotteries

    def get_discount_policy(self):
        return self.__discount_policy

    def set_counters(self, active, closed_by_admin, product_id_counter, auction_id_counter, lottery_id_counter):
        self.active = active
        self.closed_by_admin = closed_by_admin
        self.product_id_counter = product_id_counter
        self.auction_id_counter = auction_id_counter
        self.lottery_id_counter = lottery_id_counter

    # =======================JSON=======================#

    def toJsonInfo(self):
        return {
            'store_name': self.__store_name,
            'active': str(self.active)
        }

    def toJsonProducts(self):
        return {
            'store_name': self.__store_name,
            'products': JsonSerialize.toJsonAttributes(self.__products),
            'active': str(self.active),
            'accesses': JsonSerialize.toJsonAttributes(self.__accesses)
        }

    def toJsonAccesses(self):
        return {
            "store_name": self.__store_name,
            "products": JsonSerialize.toJsonAttributes(self.__products),
            "active": str(self.active),
            # "accesses": JsonSerialize.toJsonAttributes(self.__accesses)
        }

    def toJsonAll(self):
        return {
            "store_name": self.__store_name,
            "products": JsonSerialize.toJsonAttributes(self.__products),
            "active": str(self.active),
            "accesses": JsonSerialize.toJsonAttributes(self.__accesses),
            "bids": JsonSerialize.toJsonAttributes(self.__bids),
            "bids_requests": JsonSerialize.toJsonAttributes(self.__bids_requests),
            "auctions": JsonSerialize.toJsonAttributes(self.__auctions),
            "lotteries": JsonSerialize.toJsonAttributes(self.__lotteries),
            "discounts": self.__discount_policy.toJson()
        }

    def close_store_by_admin(self):
        if self.closed_by_admin:
            raise Exception("Store already closed by admin")
        else:
            if not self.closed_by_admin and not self.active:
                self.active = False
            else:
                self.active = False
                self.closed_by_admin = True


    def close_store_by_admin(self):
        if self.closed_by_admin:
            raise Exception("Store already closed by admin")
        else:
            if not self.closed_by_admin and not self.active:
                self.active = False
            else:
                self.active = False
                self.closed_by_admin = True
    def checkValue(self, value):
        if isinstance(value,int):
            if value <= 0:
                raise Exception("value cannot be 0 or negative number")
        else:
            if isinstance(value,str):
                if value == "":
                    raise Exception("name or category cannot be empty")
