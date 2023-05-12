from ProjectCode.Domain.ExternalServices.PaymetService import PaymentService
from ProjectCode.Domain.ExternalServices.TransactionHistory import TransactionHistory
from ProjectCode.Domain.Helpers.JsonSerialize import JsonSerialize
from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.MarketObjects.Basket import Basket
from ProjectCode.Domain.MarketObjects.Bid import Bid
from ProjectCode.Domain.MarketObjects.Store import Store
from ProjectCode.Domain.MarketObjects.StoreObjects.Product import Product


class Cart:

    def __init__(self, username):
        self.username = username
        self.baskets = TypedDict(str, Basket)

    def get_Basket(self, storename):
        if self.baskets.keys().__contains__(storename):
            return self.baskets[storename]
        else:
            raise Exception("Basket does not exists")

    def add_Product(self, username, storename, productID, product, quantity):
        if not self.baskets.keys().__contains__(storename):
            basket = Basket(username, storename)
            self.baskets[storename] = basket
        basket: Basket = self.get_Basket(storename)
        basket.add_Product(productID, product, quantity)
        return basket

    def removeFromBasket(self, storename, productID):
        if self.baskets.keys().__contains__(storename):
            basket = self.baskets[storename]
            answer = basket.remove_Product(productID)  # answer = true if item is successfully removed
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
            basket: Basket = self.get_Basket(storename)
            basket.edit_Product_Quantity(productID, quantity)
            return basket
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
        basket: Basket = self.get_Basket(storename)
        return basket.getProductsAsTuples()

    def addBidToBasket(self, bid: Bid):
        if not self.baskets.keys().__contains__(bid.get_storename()):
            basket = Basket(bid.get_username(), bid.get_storename())
            self.baskets[bid.get_storename()] = basket
        basket_to_place_bid: Basket = self.baskets[bid.get_storename()]
        basket_to_place_bid.addBidToBasket(bid)

    def getAllBids(self):
        output = set()  # set of bids
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

    def clearCart(self):
        for basketKey in self.baskets.keys():
            basket: Basket = self.baskets[basketKey]
            if basket.getBasketSize() == 0 and basket.getBasketBidSize() == 0:
                del self.baskets[basketKey]

    def clearCartFromProducts(self):
        for basketKey in self.baskets.keys():
            basket: Basket = self.baskets[basketKey]
            basket.clearProducts()

    def clearBidFromBasket(self, storename, bid_id):
        if self.baskets.keys().__contains__(storename):
            basket: Basket = self.baskets[storename]
            basket.clearBidFromBasket(bid_id)

    def PurchaseCart(self, card_number, card_user_name, card_user_id, card_date, back_number, address, is_member, lock):
        payment_service = PaymentService()
        transaction_history = TransactionHistory()
        overall_price = 0  # overall price for the user
        stores_to_products = TypedDict(str, list)  # store_name to list of tuples <products,quantities>
        # async with lock:
        answer = self.checkAllItemsInCart()  # answer = True or False, if True then purchasing is available
        if answer is True:  # means everything is ok to go
            for basket in self.get_baskets().values():  # all the baskets
                products: list = basket.getProductsAsTuples()
                price = basket.purchaseBasket()  # price of a single basket  #TODO:amiel ; needs to have supply approval
                # shipment_date = self.supply_service.checkIfAvailable(basket.store, address,products)  # TODO: Ari, there should be an address probaby
                payment_service.pay(basket.store, card_number, card_user_name, card_user_id, card_date, back_number,
                                    price)
                transaction_history.addNewStoreTransaction(self.username, basket.store.store_name, products,
                                                           price)  # make a new transaction and add it to the store history and user history
                stores_to_products[basket.store.store_name] = products  # gets the products for the specific store
                overall_price += price
            if is_member:
                transaction_history.addNewUserTransaction(self.username, stores_to_products, overall_price)
            self.clearCartFromProducts()  # clearing all the products from all the baskets
            self.clearCart()  # if there are empty baskets from bids and products - remove them
        else:
            raise Exception("There is a problem with the items quantity or existance in the store")

    def purchaseConfirmedBid(self, store_name, bid_id, card_number, card_user_name, card_user_id, card_date,
                             back_number, lock):
        payment_service = PaymentService()
        transaction_history = TransactionHistory()
        bid: Bid = self.getBid(store_name, bid_id)
        if bid.get_status() == 1:
            # async with lock:
            answer = self.checkItemInCartForBid(bid)
            if answer:
                basket: Basket = self.baskets.get(store_name)
                store: Store = basket.get_Store()
                product: Product = store.get_products()[bid.get_product()]
                item_name = product.name
                tuple_for_history = (item_name, bid.get_quantity())
                payment_service.pay(bid.get_storename(), card_number, card_user_name, card_user_id, card_date,
                                    back_number, bid.get_offer())
                store.purchaseBid(bid_id)
                transaction_history.addNewStoreTransaction(self.username, bid.get_storename(), tuple_for_history,
                                                           bid.get_offer())

                dict_for_history = TypedDict(str, tuple)
                dict_for_history[store_name] = tuple_for_history
                transaction_history.addNewUserTransaction(self.username, dict_for_history, bid.get_offer())
                self.clearBidFromBasket(store_name, bid_id)
            else:
                raise Exception("there was a problem with the Bid or the quantity in the store")
        else:
            raise Exception("Bid is not confirmed")

    # =======================JSON=======================#

    def toJson(self):
        return {
            "username": self.username,
            "baskets": JsonSerialize.toJsonAttributes(self.baskets)
        }
