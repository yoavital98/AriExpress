from ProjectCode.Domain.Helpers.TypedDict import *
from ProjectCode.Domain.Objects.StoreObjects.Product import *
from ProjectCode.Domain.Objects.AccessControl import *
from ProjectCode.Domain.Objects.Access import Access
from ProjectCode.Domain.Objects.Access import *
from ProjectCode.Domain.Objects.Bid import *
from ProjectCode.Domain.Objects.StoreObjects.Auction import *
import string
import datetime
from typing import List


class Store:

    def __init__(self, store_name):
        self.__store_name = store_name
        self.__products = TypedDict(int, Product)
        #TODO: policies
        self.active: bool = True
        self.closed_by_admin: bool = False
        self.__accesses = TypedDict(str, Access)
        self.product_id_counter = 0
        self.auction_id_counter = 0
        self.__bids = TypedDict(int, Bid)
        self.__bids_requests = TypedDict(Access, List[Bid])
        self.__auctions = TypedDict(int, Auction)





    def setFounder(self, username, access):
        access.setFounder(True)
        self.__accesses[username] = access


    def setAccess(self, nominated_access, requester_username, nominated_username, **kwargs):
#<<<<<<< tmp_f
#        self.accesses[nominated_username] = nominated_access
#        requester_access = self.accesses.get(requester_username)
#=======
        self.__accesses[nominated_username] = nominated_access
        requester_access = self.__accesses[requester_username]
#>>>>>>> final_fix
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
        self.__products.__setitem__(self.product_id_counter, product_to_add)
        return product_to_add

    def deleteProduct(self, access, product_id):
        self.hasForProductAccess(access)
        if self.__products.get(product_id) is None:
            raise Exception("Product doesn't exists")
        else:
            self.__products.__delitem__(product_id)
            return product_id

    def changeProduct(self, access, product_id, **kwargs):
        self.hasForProductAccess(access)
        cur_product = self.__products.get(product_id)
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
        cur_access = self.__accesses[requester_username]
        if cur_access.isFounder:

            return True
        else:
            raise Exception("Member isn't the founder of the store")


    def getStaffInfo(self, username):
#<<<<<<< tmp_f
#        cur_access = self.accesses.get(username)
#=======
        cur_access = self.__accesses[username]
#>>>>>>> final_fix
        if cur_access is None:
            raise Exception("Member has no access for that store")
        if cur_access.isFounder or cur_access.isOwner or cur_access.isManager:
            return self.__accesses
        else:
            raise Exception("Member has no access for that action")

    def checkProductAvailability(self, product_id, quantity):
        answer = True
        cur_product = self.__products[int(product_id)]
        if cur_product is None:
            answer = False
        if cur_product.quantity - quantity < 0:
            answer = False
        else:
            answer = True
        return answer
    def searchProductByName(self, keyword):
#<<<<<<< tmp_f
#        product_list = list()
#        for prod in self.products.values():
#=======
        product_list = []
        for prod in self.__products.values():
#>>>>>>> final_fix
            if keyword in prod.name:
                product_list.append(prod)
        return product_list


    def searchProductByCategory(self, category):
#<<<<<<< tmp_f
#        product_list = list()
#        for prod in self.products.values():
#=======
        product_list = []
        for prod in self.__products.values():
#>>>>>>> final_fix
            if category in prod.categories:
                product_list.append(prod)
        return product_list


    def purchaseBasket(self, products_dict): #tup(product,qunaiity)
        overall_price = 0
        for product_id, product_tuple in products_dict.items():
            cur_product = self.__products[product_id]
            if cur_product is None:
                raise Exception("No such product exists")
            cur_product.quantity -= product_tuple[1]
            overall_price += cur_product.price * product_tuple[1]
        return overall_price

    def requestBid(self, bid: Bid):
        self.__bids[bid.bid_id] = bid
        for access in self.__accesses.values():
            if access.isOwner or access.isFounder:
                if self.__bids_requests[access] is None:
                    self.__bids_requests[access] = []
                self.__bids_requests[access].append(bid)
                bid.increment_left_to_approve()



    def approveBid(self, username, bid_id):
        cur_access = self.__accesses[username]
        if not (cur_access.isFounder or cur_access.isFounder or cur_access.isManager):
            raise Exception("User doesn't have the permission for rejecting a bid")
        cur_bid: Bid = self.__bids[bid_id]
        if cur_bid is None:
            raise Exception("No such bid exists in the store")
        if cur_bid not in self.__bids_requests[cur_access]:
            raise Exception("You already approved that bid")
        cur_bid.approve_by_one()
        self.__bids_requests[cur_access].remove(cur_bid)
        if cur_bid.get_left_to_approval() == 0:
            cur_bid.set_status(1)
        return cur_bid


    def rejectBid(self, username, bid_id):
        cur_access: Access = self.__accesses[username]
        if not (cur_access.isFounder or cur_access.isFounder or cur_access.isManager):
            raise Exception("User doesn't have the permission for rejecting a bid")
        cur_bid: Bid = self.__bids[bid_id]
        if cur_bid is None:
            raise Exception("No such bid exists in the store")
        for access, bid_list in self.__bids_requests.items():
            if cur_bid in bid_list:
                bid_list.remove(cur_bid)
        cur_bid.set_status(2)
        return cur_bid


    def sendAlternativeBid(self, username, bid_id, alternate_offer):
        cur_access: Access = self.__accesses[username]
        if not (cur_access.isFounder or cur_access.isFounder or cur_access.isManager):
            raise Exception("User doesn't have the permission for rejecting a bid")
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
        cur_access = self.__accesses[username]
        cur_product = self.__products[int(product_id)]
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
        self.__auctions[self.auction_id_counter] = new_auction
        return new_auction

    def placeOfferInAuction(self, username, auction_id, offer):
        cur_auction: Auction = self.__auctions.get(auction_id)
        if cur_auction is None:
            raise Exception("No such auction exists")
        if cur_auction.get_expiration_date() < datetime.datetime.now():
            raise Exception("You cannot place an offer in a closed auction")
        if offer > cur_auction.get_current_offer():
            cur_auction.set_current_offer(offer)
            cur_auction.set_highest_offer_username(username)
        return cur_auction

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






