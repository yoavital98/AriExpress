import asyncio
from datetime import date, datetime
from sqlite3 import Date

from ProjectCode.Domain.ExternalServices.MessageController import MessageController
from ProjectCode.Domain.ExternalServices.MessageObjects.PurchaseReport import PurchaseReport
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

    def add_Product(self,username, store, product_id, product, quantity):
        if not self.baskets.keys().__contains__(store.get_store_name()):
                basket_to_add = Basket(str(username), store)
                self.baskets[store.get_store_name()] = basket_to_add
        basket: Basket = self.get_Basket(store.get_store_name())
        basket.add_Product(product_id, product, quantity)
        return basket

    def removeFromBasket(self, store_name, product_id):
        if self.baskets.keys().__contains__(store_name):
            basket: Basket = self.baskets[store_name]
            answer: bool = basket.remove_Product(product_id) # answer = true if item is successfully removed
            if (basket.getBasketSize() == 0) and (basket.getBasketBidSize() == 0):
                del self.baskets[store_name]
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
        list_of_keys_to_clear: list = list()
        for basketKey in self.baskets.keys():
            basket: Basket = self.baskets[basketKey]
            if basket.getBasketSize() == 0 and basket.getBasketBidSize() == 0:
                list_of_keys_to_clear.append(basketKey)
        for key in list_of_keys_to_clear:
            del self.baskets[key]

    def clearCartFromProducts(self):
        for basketKey in self.baskets.keys():
            basket: Basket = self.baskets[basketKey]
            basket.clearProducts()

    def clearBidFromBasket(self, storename, bid_id):
        if self.baskets.keys().__contains__(storename):
            basket: Basket = self.baskets[storename]
            basket.clearBidFromBasket(bid_id)

    def PurchaseCart(self, card_number, card_user_name, card_holder_id, card_date, cvv, address, is_member):
        payment_service = PaymentService()
        transaction_history = TransactionHistory()
        overall_price = 0  # overall price for the user
        stores_products_dict = TypedDict(str, list)  # store_name to list of tuples (productid,productname,quantity,price4unit)
        answer = self.checkAllItemsInCart()  # answer = True or False, if True then purchasing is available
        # this checks if the credit card is valid!
        try:
            payment_service.validate_credit_card(card_number, card_date, cvv, card_holder_id)
        except Exception as e:
            raise Exception(e)
        if answer is True:  # means everything is ok to go
            purchaseReports = []
            for basket in self.get_baskets().values():  # all the baskets
                products: list = basket.getProductsAsTuples()  # tupleList [(productid,productname,quantity,price4unit)]
                price = basket.purchaseBasket()  # price of a single basket  #TODO:amiel ; needs to have supply approval
                #shipment_date = self.supply_service.checkIfAvailable(basket.store, address,products)  # TODO: Ari, there should be an address probaby
                transaction_history.addNewStoreTransaction(self.username, basket.get_Store().get_store_name(), products, price)  # make a new transaction and add it to the store history and user history
                cur_purchase = PurchaseReport(self.username, basket.get_Store().get_store_name(), products, price)
                MessageController().send_message("AriExpress", basket.get_Store().getFounder(), "Purchase Received", cur_purchase, \
                                                 datetime.now(), False, None)
                purchaseReports.append(cur_purchase)
                stores_products_dict[basket.store.get_store_name()] = products
                overall_price += price
            if is_member:
                transaction_history.addNewUserTransaction(self.username, stores_products_dict, overall_price)
                MessageController().send_message("AriExpress", self.username, "Purchase Received", purchaseReports, \
                                                 datetime.now(), False, None)

            self.clearCartFromProducts()  # clearing all the products from all the baskets
            self.clearCart()  # if there are empty baskets from bids and products - remove them
            return {
            "purchaseReports": purchaseReports,
            "overallPrice": overall_price}
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
