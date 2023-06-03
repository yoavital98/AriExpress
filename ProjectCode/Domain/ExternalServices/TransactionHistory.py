import json

from ProjectCode.Domain.ExternalServices.TransactionObjects.StoreTransaction import StoreTransaction
from ProjectCode.Domain.ExternalServices.TransactionObjects.UserTransaction import UserTransaction
from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.MarketObjects.StoreObjects.Product import Product


class TransactionHistory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.user_transactions = TypedDict(str, list)
            cls._instance.store_transactions = TypedDict(str, list)
            # Add any initialization code here
        return cls._instance
    # insert empty list is a method for tests
    def insertEmptyListToUser(self, user_name):
        self.user_transactions[user_name] = list()

    def insertEmptyListToStore(self, store_name):
        self.store_transactions[store_name] = list()


    def addUserTransaction(self, transaction: UserTransaction):
        if transaction.get_username() in self.user_transactions.keys():
            user_list: list = self.user_transactions[transaction.get_username()]
            user_list.append(transaction)
        else:
            self.user_transactions[transaction.get_username()] = list()
            new_list: list = self.user_transactions.get(transaction.get_username())
            new_list.append(transaction)

    def addStoreTransaction(self, transaction: StoreTransaction):
        if transaction.get_storename() in self.store_transactions.keys():
            store_list: list = self.store_transactions[transaction.get_storename()]
            store_list.append(transaction)

        else:
            self.store_transactions[transaction.get_storename()] = list()
            new_list: list = self.store_transactions.get(transaction.get_storename())
            new_list.append(transaction)

    def get_User_Transactions(self, user_name):
        if user_name in self.user_transactions.keys():
            return self.user_transactions.get(user_name)
        else:
            raise Exception("Empty member purchases")

    def get_Store_Transactions(self, store_name):
        if store_name in self.store_transactions.keys():
            return self.store_transactions.get(store_name)
        else:
            raise Exception("Empty store purchases")


    def addNewStoreTransaction(self, username, store_name, products, overall_price):
        # product_list: list = list()
        # for product in products:
        #     product_to_add: Product = product[0]
        #     product_list.append((product_to_add.get_product_id(), product_to_add.get_name(), product[1], product.get_price()))
        new_store_transaction = StoreTransaction(username, store_name, products, overall_price)
        self.addStoreTransaction(new_store_transaction)

    def addNewUserTransaction(self, username, stores_products_dict, overall_price):
        new_user_transaction: UserTransaction = UserTransaction(username, stores_products_dict, overall_price)
        self.addUserTransaction(new_user_transaction)

    def getUserPurchaseHistory(self, user_name):
        if self.user_transactions.__contains__(user_name):
            return self.user_transactions.get(user_name)
        else:
            raise Exception("Member does not have a purchase history")

    def getStorePurchaseHistory(self, store_name):
        if self.store_transactions.__contains__(store_name):
            return self.store_transactions.get(store_name)
        else:
            raise Exception("Store does not have a purchase history")

    def clearAllHistory(self):
        self.user_transactions.clear()
        self.store_transactions.clear()
            
    def toJsonMember(self, user_name):
        if user_name not in self.user_transactions:
            raise ValueError(f"User: '{user_name}' has no transaction history.")
        transaction_list = []
        for user_transaction in self.user_transactions[user_name]:
            products_list = []
            for product_store, product_data in user_transaction.products.items():
                product_name, quantity, price = product_data
                product_info = {
                    "store_name": product_store,
                    "name": product_name,
                    "quantity": quantity,
                    "price": price
                }
                products_list.append(product_info)
            transaction_data = {
                "timestamp": user_transaction.get_date(),
                "products": products_list,
                "overall_price": user_transaction.get_overall_price()
            }
            transaction_list.append(transaction_data)
        data = {"transactions": transaction_list}
        return json.dumps(data)


