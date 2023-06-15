import asyncio
from datetime import date, datetime
from sqlite3 import Date

from ProjectCode.Domain.ExternalServices.MessageController import MessageController
from ProjectCode.Domain.ExternalServices.MessageObjects.PurchaseReport import PurchaseReport
from ProjectCode.Domain.ExternalServices.PaymetService import PaymentService
from ProjectCode.Domain.ExternalServices.SupplyService import SupplyService
from ProjectCode.Domain.ExternalServices.TransactionHistory import TransactionHistory
from ProjectCode.Domain.Helpers.JsonSerialize import JsonSerialize
from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.MarketObjects.Basket import Basket
from ProjectCode.Domain.MarketObjects.Bid import Bid
from ProjectCode.Domain.MarketObjects.Store import Store
from ProjectCode.Domain.MarketObjects.StoreObjects.Product import Product
from ProjectCode.Domain.Repository.BasketRepository import BasketRepository


class Cart:

    def __init__(self, username):
        self.username = username
        self.baskets = TypedDict(str, Basket)

        # REPOSITORY FIELD --- TO BE REPLACED
        self.basket_test = BasketRepository(username)

    def get_Basket(self, storename):
        if self.baskets.keys().__contains__(storename):
            return self.baskets[storename]
        else:
            raise Exception("Basket does not exists")

    def add_Product(self, username, store, product_id, product, quantity):
        if not self.baskets.keys().__contains__(store.get_store_name()):
            basket_to_add = Basket(str(username), store)
            self.baskets[store.get_store_name()] = basket_to_add
        basket: Basket = self.get_Basket(store.get_store_name())
        basket.add_Product(product_id, product, quantity)
        return basket

    def removeFromBasket(self, store_name, product_id):
        if self.baskets.keys().__contains__(store_name):
            basket: Basket = self.baskets[store_name]
            answer: bool = basket.remove_Product(product_id)  # answer = true if item is successfully removed
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

    def addBidToBasket(self, bid: Bid, store: Store):
        if not self.baskets.keys().__contains__(bid.get_storename()):
            basket = Basket(bid.get_username(), store)
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
        if self.baskets.keys().__contains__(bid.get_storename()):
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

    def PurchaseCart(self, user_name, card_number, card_date, card_user_full_name, ccv, card_holder_id, address, city,
                     country, zipcode, is_member):
        payment_service = PaymentService("https://php-server-try.000webhostapp.com/")
        supply_service = SupplyService("https://php-server-try.000webhostapp.com/")
        transaction_history = TransactionHistory()
        message_controller = MessageController()
        overall_price = 0  # overall price for the user
        stores_products_dict = TypedDict(str,
                                         list)  # store_name to list of tuples (productid,productname,quantity,price4unit)
        answer = self.checkAllItemsInCart()  # answer = True or False, if True then purchasing is available
        try:
            payment_service.perform_handshake()
            supply_service.perform_handshake()
        except Exception as e:
            raise Exception(e)
        if answer:  # means everything is ok to go
            purchaseReports = {}
            founders_usernames = []
            exp_month, exp_year = card_date.split("/")
            for basket in self.get_baskets().values():  # all the baskets
                products: list = basket.getProductsAsTuples()  # tupleList [(productid,productname,quantity,price4unit)]
                price = basket.calculateBasketPrice()  # price of a single basket
                founders_usernames.append(basket.get_Store().getFounder().get_username())
                cur_purchase = PurchaseReport(self.username, basket.get_Store().get_store_name(), products, price)
                purchaseReports[basket.get_Store().get_store_name()] = cur_purchase
                stores_products_dict[basket.get_Store().get_store_name()] = products
                overall_price += price
            try:
                transaction_id = payment_service.pay(card_number, exp_month, exp_year, card_user_full_name, ccv,
                                                     card_holder_id)
            except Exception as e:
                raise Exception(e)
            try:
                supply_id = supply_service.dispatch_supply(card_user_full_name, address, city, country, zipcode)
            except Exception as e:
                raise Exception(e)
            message_header = "Regular Purchase Received. Transaction_ID: " + str(transaction_id) + " Supply_ID: " + str(supply_id)
            buyer_message_header = "Regular Purchase Completed. Transaction_ID: " + str(transaction_id) + " Supply_ID: " + str(supply_id)
            for basket in self.get_baskets().values():  # purchase all the baskets
                basket.purchaseBasket()
           
            purchase_reports_json = []
            index = 0
            for purchase in purchaseReports.values():  # all the baskets
                transaction_history.addNewStoreTransaction(transaction_id, supply_id, user_name,
                                                           purchase.getStorename(), purchase.getProducts(),
                                                           purchase.getTotalBasketPayment())
                MessageController().send_notification(founders_usernames[index], message_header, purchase.toJson(), datetime.now())
                index += 1
                purchase_reports_json.append(purchase.toJson())

            if is_member:
                transaction_history.addNewUserTransaction(transaction_id, supply_id, self.username,
                                                            stores_products_dict, overall_price)
                message = "Thank you for buying in AriExpress! Your transaction id is: " + str(transaction_id) + " and your supply id is: " + str(supply_id)+ "\n" + "Your purchase reports are: \n"
                purchaseReportsString = '\n'.join([str(rep) for rep in purchase_reports_json])
                MessageController().send_message("AriExpress", self.username, buyer_message_header,message+purchaseReportsString, datetime.now())
            self.clearCartFromProducts()  # clearing all the products from all the baskets
            self.clearCart()  # if there are empty baskets from bids and products - remove them
            return {
                "message": "Regular Purchase was successful",
                "transaction_id": transaction_id,
                "supply_id": supply_id,
                "purchaseReports": purchase_reports_json,
                "overallPrice": overall_price
            }
        else:
            raise Exception("There is a problem with the items quantity or existence in the store")

    def purchaseConfirmedBid(self, bid_id, store_name, user_name, card_number, card_date, card_user_full_name, ccv,
                             card_holder_id
                             , address, city, country, zipcode):
        payment_service = PaymentService("https://php-server-try.000webhostapp.com/")
        supply_service = SupplyService("https://php-server-try.000webhostapp.com/")
        transaction_history = TransactionHistory()
        message_controller = MessageController()
        bid: Bid = self.getBid(store_name, bid_id)
        if bid.get_status() == 1 or bid.get_status() == 3:
            # async with lock:
            answer = self.checkItemInCartForBid(bid)
            try:
                payment_service.perform_handshake()
                supply_service.perform_handshake()
            except Exception as e:
                raise Exception(e)
            if answer:
                exp_month, exp_year = card_date.split("/")
                basket: Basket = self.baskets.get(store_name)
                store: Store = basket.get_Store()
                product: Product = store.getProductById(bid.get_product_id(), "")
                single_product_dict = {store_name: product}
                transaction_id = payment_service.pay(card_number, exp_month, exp_year, card_user_full_name, ccv,
                                                     card_holder_id)
                supply_id = supply_service.dispatch_supply(card_user_full_name, address, city, country, zipcode)
                store.purchaseBid(bid_id)
                message_header = "Bid Purchase Received. Transaction_ID: " + str(transaction_id) + " Supply_ID: " + str(
                    supply_id)
                transaction_history.addNewUserTransaction(transaction_id, supply_id, user_name, single_product_dict,
                                                          bid.get_offer())
                transaction_history.addNewStoreTransaction(transaction_id, supply_id, user_name, store_name,
                                                           single_product_dict, bid.get_offer())
                message_controller.send_notification(user_name, message_header, single_product_dict,
                                                          datetime.now())

                message_controller.send_notification(store.getFounder().get_username(), message_header, single_product_dict,
                                                           datetime.now())
                self.clearBidFromBasket(store_name, bid_id)
                return {
                    "message": "Bid Purchase was successful",
                    "transaction_id": transaction_id,
                    "supply_id": supply_id,
                    "single_product_dict": single_product_dict,
                    "price": bid.get_offer()
                }
            else:
                raise Exception("there was a problem with the Bid or the quantity in the store")
        else:
            raise Exception("Bid is not confirmed")

    def setBaskets(self, baskets):
        self.baskets = baskets

    # =======================JSON=======================#

    def toJson(self):
        return {
            "username": self.username,
            "baskets": JsonSerialize.toJsonAttributes(self.baskets)
        }
