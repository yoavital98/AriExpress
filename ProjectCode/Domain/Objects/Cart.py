import string

from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.Objects.Basket import *


class Cart:

    def __init__(self, username):
        self.username = username
        self.baskets = TypedDict(str, Basket)

    def get_Baskets(self, storename):
        if self.baskets.keys().__contains__(storename):
            return self.baskets[storename]
        else:
            raise Exception("Basket does not exists")

    def add_Product(self,username, storename, productID, product, quantity):
        if not self.baskets.keys().__contains__(storename):
                basket = Basket(username, storename)
                self.baskets[storename] = basket
        basket: Basket = self.get_Baskets(storename)
        basket.add_Product(productID, product, quantity)

    def removeFromBasket(self, storename, productID):
        if self.baskets.keys().__contains__(storename):
            basket = self.baskets[storename]
            answer = basket.remove_Product(productID) # answer = true if item is successfully removed
            if basket.getBasketSize() == 0:
                self.baskets.__delitem__(storename)
            return answer
        else:
            raise Exception("Basket was not found")

    def checkProductExistance(self, storename, productID):
        if self.baskets.keys().__contains__(storename):
            basket = self.baskets[storename]
            return basket.checkProductExistance(productID)
        else:
            raise Exception("Basket was not found")

    def edit_Product_Quantity(self, storename, productID, quantity):
        if self.baskets.keys().__contains__(storename):
            basket: Basket = self.get_Baskets(storename)
            basket.edit_Product_Quantity(productID, quantity)
        else:
            raise Exception("Basket was not found")

    def get_username(self):
        return self.username

    def set_username(self, username):
        self.username = username

    def get_baskets(self):
        return self.baskets

    def set_baskets(self, baskets):
        self.baskets = baskets

    def getProductsAsTuples(self, storename):
        basket: Basket = self.get_Baskets(storename)
        return basket.getProductsAsTuples()

    def addBidToBasket(self, bid: Bid):
        if not self.baskets.keys().__contains__(bid.get_storename()):
            basket = Basket(bid.get_username(), bid.get_storename())
            self.baskets[bid.get_storename()] = basket
        basket_to_place_bid: Basket = self.baskets[bid.get_storename()]
        basket_to_place_bid.addBidToBasket(bid)

    def getAllBids(self):
        output = set() #set of bids
        for basket in self.baskets.values():
            bids: TypedDict[int, Bid] = basket.get_bids()
            for bid in bids:
                output.add(bid)
        return output

    def getBid(self, storename, bid_id):
        if not self.baskets.keys().__contains__(storename):
            raise Exception("Basket does not exists")
        basket: Basket = self.baskets[storename]
        return basket.get_bids()[bid_id]  # TODO: check if the bid even exists

    def checkAllItemsInCart(self):
        answer = None
        for basket in self.baskets.values():
            answer = basket.checkAllItemsInBasket()
            if not answer:
                return answer
        return answer

    def checkItemInCartForBid(self, bid):
        if self.baskets.keys().__contains__(bid.set_storename()):
            basket = self.baskets[bid.get_storename()]
            return basket.checkItemInBasketForBid(bid)
        else:
            raise Exception("Basket was not found")
