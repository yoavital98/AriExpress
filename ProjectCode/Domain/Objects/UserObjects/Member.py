from ariExpressDjango.ProjectCode.Domain.Helpers import TypedDict
from ariExpressDjango.ProjectCode import Access
from ariExpressDjango.ProjectCode.Domain.Objects.StoreObjects import Auction
from ariExpressDjango.ProjectCode import User


class Member(User):
    def __init__(self, username, password, email):
        super().__init__(username)
        self.accesses = TypedDict(str, Access)  # Accesses
        self.password = password  # password
        self.email = email  # email
        self.logged_In = False  # login
        self.auctions = TypedDict(int, Auction)  # auction id to auction

    # -------------------------Methods from User--------------------------------
    def get_cart(self):
        return super().get_cart()

    def add_to_cart(self, username, storename, productID, product, quantity):
        super().add_to_cart(username, storename, productID, product, quantity)

    def get_Basket(self, storename):
        return super().get_Basket(storename)

    def removeFromBasket(self, storename, productID):
        super().removeFromBasket(storename, productID)

    def edit_Product_Quantity(self, storename, productID, quantity):
        super().edit_Product_Quantity(storename, productID, quantity)

    # -------------------------------------------------------------------------------

    def logInAsMember(self):
        self.logged_In = True

    def logOut(self):  # TODO need to turn the member to guest
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