

from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.Objects.Bid import Bid
from ProjectCode.Domain.Objects.Store import Store
from ProjectCode.Domain.Objects.StoreObjects.Product import Product


class Basket:
    def __init__(self, username, store):
        self.username = username
        self.store: Store = store
        self.products = TypedDict(int, tuple)  # product id -> (product_name, quantity)
        self.bids = TypedDict(int, Bid)

    def add_Product(self, product_ID, product_name, quantity):
        if quantity <= 0:
            raise Exception("quantity cannot be set to 0 or negative number")
        if not self.products.keys().__contains__(product_ID):
            self.products[product_ID] = (product_name, quantity)
        else:
            raise Exception ("product already exists in the basket")

    def edit_Product_Quantity(self, product_ID, quantity):
        if quantity <= 0:
            raise Exception("quantity cannot be set to 0 or negative number")
        product: tuple = self.products[product_ID]
        product[1] = quantity

    def remove_Product(self, product_ID):
        if self.products.keys().__contains__(product_ID):
            self.products.__delitem__(product_ID)
            return True
        else:
            return False

    def get_Store(self):
        return self.store

    def set_Store(self, store):
        self.store = store

    def get_Products(self):
        return self.products

    def checkProductExistance(self, product_ID):
        return self.products.keys().__contains__(product_ID)

    def getBasketSize(self):
        return self.products.__sizeof__()
    def getBasketBidSize(self):
        return self.bids.__sizeof__()

    def getProductsAsTuples(self):
        return self.products.values()

    def addBidToBasket(self, bid: Bid):
        self.bids[bid.get_bid_id()] = bid

    def get_bids(self):
        return self.bids

    def checkAllItemsInBasket(self):
        answer = True
        for key in self.products.keys():
            if not self.store.checkProductAvailability(key, self.products[key]):
                answer = False
                return answer
        return answer

    def checkItemInBasket(self, product_id):  # checks if the item is available in the store
        if self.products.keys().__contains__(product_id):
            return self.store.checkProductAvailability(product_id, self.products[product_id])
        else:
            Exception("product is not in the Basket")

    def purchaseBasket(self):
        return self.store.purchaseBasket(self.products)

    def clearProducts(self):
        self.products.clear()

    def clearBidFromBasket(self, bid_id):
        del self.bids[bid_id]