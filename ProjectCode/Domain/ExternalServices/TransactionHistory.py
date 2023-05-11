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
        if transaction.get_username() in self.user_transactions:
            user_list: list = self.user_transactions[transaction.get_username()]
            user_list.append(transaction)
        else:
            self.user_transactions[transaction.get_username()] = list().append(transaction)

    def addStoreTransaction(self, transaction: StoreTransaction):
        if transaction.get_storename() in self.store_transactions:
            store_list: list = self.store_transactions[transaction.get_storename()]
            store_list.append(transaction)
        else:
            self.store_transactions[transaction.get_storename()] = list().append(transaction)

    def get_User_Transactions(self, username):
        return self.user_transactions[username]

    def get_Store_Transactions(self, store_name):
        return self.store_transactions[store_name]

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
