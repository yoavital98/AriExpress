import json

from ProjectCode.Domain.ExternalServices.TransactionObjects.StoreTransaction import StoreTransaction
from ProjectCode.Domain.ExternalServices.TransactionObjects.UserTransaction import UserTransaction
from ProjectCode.Domain.Helpers.TypedDict import TypedDict


class TransactionHistory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.user_transactions = TypedDict(str, set)
            cls._instance.store_transactions = TypedDict(str, set)
            # Add any initialization code here
        return cls._instance

    def addUserTransaction(self, transaction):
        if len(transaction != 3):
            raise Exception("Invalid transaction, should be in format (product_name, quantity, price)")
        if transaction.username in self.user_transactions:
            self.user_transactions[transaction.username].add(transaction)
        else:
            self.user_transactions[transaction.username] = set().add(transaction)

    def addStoreTransaction(self, transaction):
        if len(transaction != 3):
            raise Exception("Invalid transaction, should be in format (product_name, quantity, price)")
        if transaction.storename in self.store_transactions:
            self.store_transactions[transaction.storename].add(transaction)
        else:
            self.store_transactions[transaction.storename] = set().add(transaction)

    def get_User_Transactions(self, username):
        return self.user_transactions[username]

    def get_Store_Transactions(self, storename):
        return self.store_transactions[storename]

    def addNewStoreTransaction(self, username, storename, products, overall_price):
        new_store_transaction = StoreTransaction(username, storename, products, overall_price)
        store_transactions: set = self.store_transactions[storename]
        store_transactions.add(new_store_transaction)

    def addNewUserTransaction(self, username, products, overall_price):
        new_user_transaction = UserTransaction(username, products, overall_price)
        user_transactions: set = self.store_transactions[username]
        user_transactions.add(new_user_transaction)

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
