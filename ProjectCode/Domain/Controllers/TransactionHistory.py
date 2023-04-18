import string

from ProjectCode.Domain.Helpers.TypedDict import TypedDict
class TransactionHistory:
    def __init__(self):
        self.user_transactions = TypedDict(string, set)
        self.store_transactions = TypedDict(string, set)

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

