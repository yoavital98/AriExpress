from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.Objects.ExternalObjects.StoreTransaction import StoreTransaction
from ProjectCode.Domain.Objects.ExternalObjects.UserTransaction import UserTransaction


class TransactionHistory:
    def __init__(self):
        self.user_transactions = TypedDict(str, set)
        self.store_transactions = TypedDict(str, set)

    def addUserTransaction(self, transaction):
        if transaction.username in self.user_transactions:
            self.user_transactions[transaction.username].add(transaction)
        else:
            self.user_transactions[transaction.username] = set().add(transaction)


    def addStoreTransaction(self, transaction):
        if transaction.storename in self.store_transactions:
            self.store_transactions[transaction.storename].add(transaction)
        else:
            self.store_transactions[transaction.storename] = set().add(transaction)

    def get_User_Transactions(self, username):
        return self.user_transactions[username]



    def get_Store_Transactions(self, storename):
        return self.store_transactions[storename]

    def addNewStoreTransaction(self, username, storename, products, overall_price):
        new_store_transaction = StoreTransaction(username, storename,products, overall_price)
        store_transactions: set = self.store_transactions[storename]
        store_transactions.add(new_store_transaction)

    def addNewUserTransaction(self, username, products, overall_price):
        new_user_transaction = UserTransaction(username, products, overall_price)
        user_transactions: set = self.store_transactions[username]
        user_transactions.add(new_user_transaction)
