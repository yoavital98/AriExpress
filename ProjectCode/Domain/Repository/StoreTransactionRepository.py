from peewee import *

from ProjectCode.DAL.ProductStoreTransactionModel import ProductStoreTransactionModel
from ProjectCode.DAL.StoreTransactionModel import StoreTransactionModel
from ProjectCode.Domain.ExternalServices.TransactionObjects.StoreTransaction import StoreTransaction
from ProjectCode.Domain.Repository.Repository import Repository


class StoreTransactionRepository(Repository):

    def __init__(self):
        self.model = StoreTransactionModel

    def __getitem__(self, store_name):
        try:
            return self.get(store_name)
        except Exception as e:
            raise Exception("StoreTransactionRepository: __getitem__ failed: " + str(e))

    def __setitem__(self, key, value): #key is meaningless
        try:
            return self.add(value)
        except Exception as e:
            raise Exception("StoreTransactionRepository: __setitem__ failed: " + str(e))

    def __delitem__(self, key):
        try:
            return self.remove(key)
        except Exception as e:
            raise Exception("StoreTransactionRepository: __delitem__ failed: " + str(e))

    def __contains__(self, key):
        try:
            return self.contains(key)
        except Exception as e:
            raise Exception("StoreTransactionRepository: __delitem__ failed: " + str(e))

    def get(self, pk=None):
        query = self.model.select()

        if pk is not None:
            query = query.where(self.model.store_name == pk)

        transactions = []
        for store_transaction in query:
            products = ProductStoreTransactionModel.select().where(
                ProductStoreTransactionModel.store_transaction == store_transaction
            )
            product_list = [
                (product.product_id, product.product_name, product.quantity, product.price)
                for product in products
            ]
            transaction = StoreTransaction(
                store_transaction.transaction_id,
                store_transaction.supply_id,
                store_transaction.user_name,
                store_transaction.store_name,
                product_list,
                store_transaction.overall_price,
            ).set_date(store_transaction.date)
            transactions.append(transaction)

        return transactions

    def add(self, store_transaction: StoreTransaction):
        # Create StoreTransactionModel object
        transaction_model = StoreTransactionModel(
            transaction_id=store_transaction.get_transaction_id(),
            supply_id=store_transaction.get_supply_id(),
            user_name=store_transaction.get_username(),
            store_name=store_transaction.get_storename(),
            overall_price=store_transaction.get_overall_price(),
            date=store_transaction.get_date()
        )
        transaction_model.save()

        # Create ProductStoreTransactionModel objects
        for product in store_transaction.get_products():
            product_model = ProductStoreTransactionModel(
                product_id=product[0],
                product_name=product[1],
                quantity=product[2],
                price=product[3],
                store_transaction=transaction_model
                #todo: product id is not primary key
            )
            product_model.save()

    def remove(self, pk):
        # Retrieve the store transactions by storename
        transactions = self.model.select().where(self.model.transaction_id == pk)

        # Delete the store transactions
        transactions.delete_instance()

        # Delete associated product store transactions manually
        for transaction in transactions:
            products = transaction.product_store_transaction
            for product in products:
                product.delete_instance()

    def keys(self):
        query = self.model.select(self.model.store_name).distinct()
        keys = [transaction.store_name for transaction in query]
        return keys

    def values(self):
        return self.get()

    def contains(self, store_name):
        query = self.model.select().where(self.model.store_name == store_name)
        return query.exists()
