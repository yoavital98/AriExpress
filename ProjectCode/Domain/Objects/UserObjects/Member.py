import string

from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.Objects.Cart import Cart
from abc import ABC, abstractmethod

from ProjectCode.Domain.Objects.StoreObjects.Auction import Auction
from ProjectCode.Domain.Objects.User import User
from ProjectCode.Domain.Objects.Access import *


class Member(User):
    def __init__(self, username, password, email):
        super().__init__(username)
        self.accesses = TypedDict(str, Access)  #Accesses
        self.password = password  # password
        self.email = email  # email
        self.logged_In = False  # login
        self.auctions = TypedDict(int, Auction) # auction id to auction

    # -------------------------Methods from User--------------------------------
    def get_cart(self):
        super().get_cart()

    def add_to_cart(self, username, storename, productID, product, quantity):
        super().add_to_cart(username, storename, productID, product, quantity)

    def get_Basket(self, storename):
        super().get_Basket(storename)

    def removeFromBasket(self, storename, productID):
        super().removeFromBasket(storename, productID)

    def edit_Product_Quantity(self, storename, productID, quantity):
        super().edit_Product_Quantity(storename, productID, quantity)

# -------------------------------------------------------------------------------


    def logInAsMember(self):
        self._logged_In = True


    def logOut(self):
        self.logged_In = False

    def get_username(self):
        return self.username

    def set_username(self, username):
        self.username = username

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_logged(self):
        return self.logged_In

    def addBidToBasket(self, bid):
        self.cart.addBidToBasket(bid)

    def getAllBids(self):
        return self.cart.getAllBids()

    def addNewAuction(self, auction_id, cur_auction):
        if not self.auctions.keys().__contains__(auction_id):
            self.auctions[auction_id] = cur_auction

    def getAuctionById(self,auction_id):
        if self.auctions.keys().__contains__(auction_id):
            return self.auctions[auction_id]
        else:
            raise Exception("Member is not participating in the auction")

    def removeAuctionById(self, auction_id):
        if self.auctions.keys().__contains__(auction_id):
            del self.auctions[auction_id]
        else:
            raise Exception("Member is not participating in the auction")
