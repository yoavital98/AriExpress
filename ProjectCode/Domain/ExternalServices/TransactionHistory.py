import json

from ProjectCode.Domain.ExternalServices.TransactionObjects.StoreTransaction import StoreTransaction
from ProjectCode.Domain.ExternalServices.TransactionObjects.UserTransaction import UserTransaction
from ProjectCode.Domain.Helpers.TypedDict import TypedDict


class TransactionHistory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.user_transactions = TypedDict(str, list)
            cls._instance.store_transactions = TypedDict(str, list)
            # Add any initialization code here
        return cls._instance

    def addUserTransaction(self, transaction: UserTransaction):
        if len(transaction != 3):
            raise Exception("Invalid transaction, should be in format (product_name, quantity, price)")
        if transaction.get_username() in self.user_transactions:
            user_list: list = self.user_transactions[transaction.get_username()]
            user_list.append(transaction)
        else:
            self.user_transactions[transaction.get_username()] = list().append(transaction)

    def addStoreTransaction(self, transaction: StoreTransaction):
        if len(transaction != 3):
            raise Exception("Invalid transaction, should be in format (product_name, quantity, price)")
        if transaction.get_storename() in self.store_transactions:
            store_list: list = self.store_transactions[transaction.get_storename()]
            store_list.append(transaction)

        else:
            self.store_transactions[transaction.get_storename()] = list().append(transaction)

    def get_User_Transactions(self, username):
        return self.user_transactions[username]

    def get_Store_Transactions(self, storename):
        return self.store_transactions[storename]

    def addNewStoreTransaction(self, username, store_name, products, overall_price):
        new_store_transaction = StoreTransaction(username, store_name, products, overall_price)
        self.addStoreTransaction(new_store_transaction)

    def addNewUserTransaction(self, username, products, overall_price):
        new_user_transaction: UserTransaction = UserTransaction(username, products, overall_price)
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


