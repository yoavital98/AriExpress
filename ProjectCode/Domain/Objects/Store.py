from ProjectCode.Domain.Helpers.TypedDict import *
from ProjectCode.Domain.Objects.StoreObjects.Product import *
from ProjectCode.Domain.Objects.Access import *
from ProjectCode.Domain.Objects.Access import Access
from ProjectCode.Domain.Objects.Access import *
from ProjectCode.Domain.Objects.Bid import *
from ProjectCode.Domain.Objects.StoreObjects.Auction import *
import string
import datetime
from typing import List


class Store:

    def __init__(self, store_name):
        self.store_name = store_name
        self.products = TypedDict(int, Product)
        #TODO: policies
        self.active: bool = True
        self.closed_by_admin: bool = False
        self.accesses = TypedDict(str, Access)
        self.product_id_counter = 0
        self.auction_id_counter = 0
        self.bids = TypedDict(int, Bid)
        self.bids_requests = TypedDict(Access, List[Bid])
        self.auctions = TypedDict(int, Auction)

    def setFounder(self, username, access):
        access.setFounder(True)
        self.accesses[username] = access


    def setAccess(self, nominated_access, requester_username, nominated_username, **kwargs):
        self.accesses[nominated_username] = nominated_access
        requester_access = self.accesses[requester_username]
        if requester_access is None:
            raise Exception("The member doesn't have the appropriate permission for that store")
        if requester_access.isOwner or requester_access.isManager or requester_access.isFounder:#TODO: change according to permission policy
            modified_access = self.modify_attributes(nominated_access, **kwargs)
            return modified_access
        else:
            raise Exception("Member doesn't have the permission in this store")

    def addProduct(self, access, name, quantity, price, categories):
        self.hasForProductAccess(access)
        self.product_id_counter += 1
        product_to_add = Product(self.product_id_counter, name, quantity, price, categories)
        self.products.__setitem__(self.product_id_counter, product_to_add)
        return product_to_add

    def deleteProduct(self, access, product_id):
        self.hasForProductAccess(access)
        if self.products.get(product_id) is None:
            raise Exception("Product doesn't exists")
        else:
            self.products.__delitem__(product_id)
            return product_id

    def changeProduct(self, access, product_id, **kwargs):
        self.hasForProductAccess(access)
        cur_product = self.products.get(product_id)
        if cur_product is None:
            raise Exception("Product doesn't exists")
        for k, v in kwargs.items():
            try:
                getattr(cur_product,k)
            except AttributeError:
                raise Exception("No such attribute exists")
            setattr(cur_product, k, v)
        return cur_product


    def hasForProductAccess(self, access):
        #TODO: change according to permission policy
        if access.isOwner or access.isFounder or access.isManager:
            return True
        else:
            raise Exception("The member has no permission for that action")


    #TODO: may cause problem for unknown reasons
    def modify_attributes(self, object_to_modify, **kwargs):
        for k, v in kwargs.items():
            try:
                getattr(object_to_modify, k)
            except AttributeError:
                raise Exception("No such attribute exists")
            setattr(object_to_modify, k, v)
        return object_to_modify


    def closeStore(self, requester_username):
        cur_access = self.accesses[requester_username]
        if cur_access.isFounder:

            return True
        else:
            raise Exception("Member isn't the founder of the store")


    def getStaffInfo(self, username):
        cur_access = self.accesses[username]
        if cur_access is None:
            raise Exception("Member has no access for that store")
        if cur_access.isFounder or cur_access.isOwner or cur_access.isManager:
            return self.accesses
        else:
            raise Exception("Member has no access for that action")

    def checkProductAvailability(self, product_id, quantity):
        answer = True
        cur_product = self.products[int(product_id)]
        if cur_product is None:
            answer = False
        if cur_product.quantity - quantity < 0:
            answer = False
        else:
            answer = True
        return answer
    def searchProductByName(self, keyword):
        product_list = []
        for prod in self.products.values():
            if keyword in prod.name:
                product_list.append(prod)
        return product_list


    def searchProductByCategory(self, category):
        product_list = []
        for prod in self.products.values():
            if category in prod.categories:
                product_list.append(prod)
        return product_list


    def purchaseBasket(self, products_dict): #tup(product,qunaiity)
        overall_price = 0
        for product_id, product_tuple in products_dict.items():
            cur_product = self.products[product_id]
            if cur_product is None:
                raise Exception("No such product exists")
            cur_product.quantity -= product_tuple[1]
            overall_price += cur_product.price * product_tuple[1]
        return overall_price

    def requestBid(self, bid: Bid):
        self.bids[bid.bid_id] = bid
        for access in self.accesses.values():
            if access.isOwner or access.isFounder:
                if self.bids_requests[access] is None:
                    self.bids_requests[access] = []
                self.bids_requests[access].append(bid)
                bid.increment_left_to_approve()



    def approveBid(self, username, bid_id):
        cur_access = self.accesses[username]
        if not (cur_access.isFounder or cur_access.isFounder or cur_access.isManager):
            raise Exception("User doesn't have the permission for rejecting a bid")
        cur_bid: Bid = self.bids[bid_id]
        if cur_bid is None:
            raise Exception("No such bid exists in the store")
        if cur_bid not in self.bids_requests[cur_access]:
            raise Exception("You already approved that bid")
        cur_bid.approve_by_one()
        self.bids_requests[cur_access].remove(cur_bid)
        if cur_bid.get_left_to_approval() == 0:
            cur_bid.set_status(1)
        return cur_bid


    def rejectBid(self, username, bid_id):
        cur_access: Access = self.accesses[username]
        if not (cur_access.isFounder or cur_access.isFounder or cur_access.isManager):
            raise Exception("User doesn't have the permission for rejecting a bid")
        cur_bid: Bid = self.bids[bid_id]
        if cur_bid is None:
            raise Exception("No such bid exists in the store")
        for access, bid_list in self.bids_requests.items():
            if cur_bid in bid_list:
                bid_list.remove(cur_bid)
        cur_bid.set_status(2)
        return cur_bid


    def sendAlternativeBid(self, username, bid_id, alternate_offer):
        cur_access: Access = self.accesses[username]
        if not (cur_access.isFounder or cur_access.isFounder or cur_access.isManager):
            raise Exception("User doesn't have the permission for rejecting a bid")
        cur_bid: Bid = self.bids[bid_id]
        if cur_bid is None:
            raise Exception("No such bid exists in the store")
        cur_bid.set_offer(alternate_offer)
        cur_bid.set_status(3)

    def startAuction(self, username, product_id, starting_price, duration):
        cur_access = self.accesses[username]
        cur_product = self.products[int(product_id)]
        if cur_access is None:
            raise Exception("The user doesnt have access in this store")
        if not (cur_access.isFounder or cur_access.isManager or cur_access.isOwner):
            raise Exception("The user doesnt have the permission for starting an auction")
        if cur_product is None:
            raise Exception("No such product exists")
        self.auction_id_counter += 1
        start_date = datetime.datetime.now()
        expiration_date = start_date + datetime.timedelta(days=int(duration))
        new_auction = Auction(self.auction_id_counter, product_id, starting_price, starting_price, start_date, expiration_date, username)
        self.auctions[self.auction_id_counter] = new_auction
        return new_auction







