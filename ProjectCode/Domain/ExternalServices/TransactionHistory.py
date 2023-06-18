import json

from ProjectCode.Domain.ExternalServices.TransactionObjects.StoreTransaction import StoreTransaction
from ProjectCode.Domain.ExternalServices.TransactionObjects.UserTransaction import UserTransaction
from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.MarketObjects.StoreObjects.Product import Product
from ProjectCode.Domain.Repository.StoreTransactionRepository import StoreTransactionRepository
from ProjectCode.Domain.Repository.UserTransactionRepository import UserTransactionRepository


class TransactionHistory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
#            cls._instance.user_transactions = TypedDict(str, list)
#            cls._instance.store_transactions = TypedDict(str, list)
            cls._instance.user_transactions = UserTransactionRepository()
            cls._instance.store_transactions = StoreTransactionRepository()
            # Add any initialization code here
        return cls._instance

    # insert empty list is a method for tests
    def insertEmptyListToUser(self, user_name):
        pass

    def insertEmptyListToStore(self, store_name):
        pass

    def addUserTransaction(self, transaction: UserTransaction):
        self.user_transactions[transaction.get_username()] = transaction

    def addStoreTransaction(self, transaction: StoreTransaction):
        self.store_transactions[transaction.get_storename()] = transaction

    def get_User_Transactions(self, user_name):
        return self.user_transactions.get(user_name)

    def get_Store_Transactions(self, store_name):
        return self.store_transactions.get(store_name)


    def addNewStoreTransaction(self, transaction_id, supply_id, username, store_name, products, overall_price):
        # product_list: list = list()
        # for product in products:
        #     product_to_add: Product = product[0]
        #     product_list.append((product_to_add.get_product_id(), product_to_add.get_name(), product[1], product.get_price()))
        new_store_transaction = StoreTransaction(transaction_id, supply_id, username, store_name, products, overall_price)
        self.addStoreTransaction(new_store_transaction)

    def addNewUserTransaction(self, transaction_id, supply_id,username, stores_products_dict, overall_price):
        new_user_transaction: UserTransaction = UserTransaction(transaction_id, supply_id, username, stores_products_dict, overall_price)
        self.addUserTransaction(new_user_transaction)

    def clearAllHistory(self):
        pass
            
    def toJsonMember(self, user_name):
        # if user_name not in self.user_transactions:
        #     raise ValueError(f"User: '{user_name}' has no transaction history.")
        transaction_list = []
        for user_transaction in self.user_transactions.get(user_name):
            products_list = []
            for product_store, product_data in user_transaction.get_products().items():
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


