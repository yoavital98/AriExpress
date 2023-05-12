import json

from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.MarketObjects.Access import Access
from ProjectCode.Domain.MarketObjects.Cart import Cart
from ProjectCode.Domain.MarketObjects.StoreObjects.Auction import Auction
from ProjectCode.Domain.MarketObjects.StoreObjects.Lottery import Lottery
from ProjectCode.Domain.MarketObjects.User import User


class Member(User):
    def __init__(self, entrance_id, user_name, password, email):
        super().__init__(entrance_id)
        self.cart = Cart(user_name) # TODO: cart will be pulled from database and guest cart will be added to it
        self.accesses = TypedDict(str, Access)  # Accesses
        self.auctions = TypedDict(int, Auction)  # auction id to auction
        self.lotteries = TypedDict(int, Lottery) # Lottery id to lottery
        self.user_name = user_name  # username
        self.password = password  # password
        self.email = email  # email

    # -------------------------Methods from User--------------------------------
    def get_cart(self):
        return super().get_cart()

    def add_to_cart(self, username, store_name, product_id, product, quantity):
        super().add_to_cart(username, store_name, product_id, product, quantity)

    def get_Basket(self, store_name):
        return super().get_Basket(store_name)

    def removeFromBasket(self, store_name, product_id):
        super().removeFromBasket(store_name, product_id)

    def edit_Product_Quantity(self, storename, product_id, quantity):
        super().edit_Product_Quantity(storename, product_id, quantity)

    # -------------------------------------------------------------------------------

    def logInAsMember(self):
        self.logged_In = True

    def logOut(self):
        self.logged_In = False

    def get_username(self):
        return self.user_name

    def set_username(self, user_name):
        self.user_name = user_name

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def addBidToBasket(self, bid):
        self.cart.addBidToBasket(bid)

    def getAllBids(self):
        return self.cart.getAllBids()

    def addNewAuction(self, auction_id, cur_auction):
        if not self.auctions.keys().__contains__(auction_id):
            self.auctions[auction_id] = cur_auction

    def getAuctionById(self, auction_id):
        if self.auctions.keys().__contains__(auction_id):
            return self.auctions[auction_id]
        else:
            raise Exception("Member is not participating in the auction")

    def removeAuctionById(self, auction_id):
        if self.auctions.keys().__contains__(auction_id):
            del self.auctions[auction_id]
        else:
            raise Exception("Member is not participating in the auction")

    def get_accesses(self):
        return self.accesses

    # def toJson(self):
    #     data = {
    #         "username": self.username
    #     }
    #     return json.dumps(data)
    #
    # def toJsonAccesses(self):
    #     data = {
    #         "username": self.username,
    #         "accesses": self.accesses,
    #         "password": self.password,
    #         "email": self.email,
    #         "logged_In": self.logged_In,
    #         "auctions": list(self.auctions.values())
    #     }
    #     return json.dumps(data)
    def setEntranceId(self, new_entrance_id):
        self.entrance_id = new_entrance_id

    def toJson(self):
        data = {
            "entrance_id": self.entrance_id,
            "username": self.user_name,
            "email": self.email
        }
        return json.dumps(data)

    def addNewLottery(self, lottery_id, cur_lottery):
        if not self.lotteries.keys().__contains__(lottery_id):
            self.auctions[lottery_id] = cur_lottery

    def claimAuctionPurchase(self,storename, auction_id, card_number, card_user_name, card_user_ID, card_date, back_number):
        pass
        #  function will be here
