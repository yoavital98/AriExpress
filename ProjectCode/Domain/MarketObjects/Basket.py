from ProjectCode.Domain.Helpers.JsonSerialize import JsonSerialize
from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.MarketObjects.Bid import Bid
from ProjectCode.Domain.MarketObjects.Store import Store


class Basket:
    def __init__(self, username, store):
        self.username = username
        self.store: Store = store
        self.products = TypedDict(int, tuple)  # product id -> (product, quantity, price)
        self.bids = TypedDict(int, Bid)

    def add_Product(self, product_id, product, quantity):
        if quantity <= 0:
            raise Exception("quantity cannot be set to 0 or negative number")
        if not self.products.keys().__contains__(product_id):
            self.products[product_id] = (product, quantity, product.get_price())
        else:
            raise Exception ("product already exists in the basket")

    def edit_Product_Quantity(self, product_id, quantity):
        if quantity <= 0:
            raise Exception("quantity cannot be set to 0 or negative number")
        product: tuple = self.products[product_id]
        self.products[product_id] = (product[0], quantity)

    def remove_Product(self, product_ID):
        if self.products.keys().__contains__(product_ID):
            del self.products[product_ID]
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
        return len(self.products)
    def getBasketBidSize(self):
        return len(self.bids)

    def getProductsAsTuples(self):
        productList = []
        for key, value in self.products.items():
            productList.append((key, value[0], value[1], value[2]))
        return productList

    def addBidToBasket(self, bid: Bid):
        self.bids[bid.bid_id] = bid

    def get_bids(self):
        return self.bids

    def checkAllItemsInBasket(self):
        for key in self.products.keys():
            if not self.store.checkProductAvailability(key, self.products.get(key)[1]):
                return False
        return True

    def checkItemInBasketForBid(self, bid):  # checks if the item is available in the store
        if self.bids.keys().__contains__(bid.bid_id):  # TODO:
            return self.store.checkProductAvailability(bid.get_product(), bid.get_quantity())
        else:
            Exception("product is not in the Basket")

    def purchaseBasket(self):
        return self.store.purchaseBasket(self.products)

    def clearProducts(self):
        self.products.clear()

    def clearBidFromBasket(self, bid_id):
        del self.bids[bid_id]
    # =======================JSON=======================#

    def toJson(self):
        return {
            "username": self.username,
            "store": self.store.get_store_name(),
            "products": JsonSerialize.toJsonAttributes(self.products),
            "bids": JsonSerialize.toJsonAttributes(self.bids)
        }