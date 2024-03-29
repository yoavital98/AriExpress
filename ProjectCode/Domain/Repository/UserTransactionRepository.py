from peewee import *

from ProjectCode.DAL.ProductStoreTransactionModel import ProductStoreTransactionModel
from ProjectCode.DAL.ProductUserTransactionModel import ProductUserTransactionModel
from ProjectCode.DAL.StoreOfUserTransactionModel import StoreOfUserTransactionModel
from ProjectCode.DAL.UserTransactionModel import UserTransactionModel
from ProjectCode.Domain.ExternalServices.TransactionObjects.UserTransaction import UserTransaction
from ProjectCode.Domain.Repository.Repository import Repository


class UserTransactionRepository(Repository):

    def __init__(self):
        self.model = UserTransactionModel

    def __getitem__(self, user_name):
        try:
            return self.get(user_name)
        except Exception as e:
            raise Exception("UserTransactionRepository: __getitem__ failed: " + str(e))

    def __setitem__(self, key, value): #key is meaningless
        try:
            return self.add(value)
        except Exception as e:
            raise Exception("UserTransactionRepository: __setitem__ failed: " + str(e))

    def __delitem__(self, key):
        try:
            return self.remove(key)
        except Exception as e:
            raise Exception("UserTransactionRepository: __delitem__ failed: " + str(e))

    def __contains__(self, key):
        try:
            return self.contains(key)
        except Exception as e:
            raise Exception("UserTransactionRepository: __delitem__ failed: " + str(e))

    def get(self, pk=None):
        if pk is None:
            query = self.model.select()
        else:
            query = self.model.select().where(self.model.username == pk)

        user_transactions = []
        for transaction in query:
            products_dict = {}
            for store in StoreOfUserTransactionModel.select().where(
                    StoreOfUserTransactionModel.transaction == transaction
            ):
                products = []
                for product in ProductUserTransactionModel.select().where(
                        ProductUserTransactionModel.store == store
                ):
                    products.append((
                        product.product_id,
                        product.product_name,
                        product.quantity,
                        product.price
                    ))
                products_dict[store.store_name] = products

            user_transaction = UserTransaction(
                transaction.transaction_id,
                transaction.supply_id,
                transaction.username,
                products_dict,
                transaction.overall_price
            )
            user_transactions.append(user_transaction)
        return user_transactions

    def add(self, user_transaction: UserTransaction):
        try:
            transaction = self.model.create(
                transaction_id=user_transaction.get_transaction_id(),
                supply_id=user_transaction.get_supply_id(),
                username=user_transaction.get_username(),
                overall_price=user_transaction.get_overall_price(),
                date=user_transaction.get_date()
            )

            for store_name, products in user_transaction.get_products().items():
                store = StoreOfUserTransactionModel.create(
                    store_name=store_name,
                    transaction=transaction
                )
                for product in products:
                    ProductUserTransactionModel.create(
                        product_id=product[0],
                        product_name=product[1],
                        quantity=product[2],
                        price=product[3],
                        store=store  # Set the correct foreign key reference
                    )
        except Exception as e:
            raise Exception("UserTransactionRepository: add failed: " + str(e))

    def remove(self, pk):
        transactions = self.model.select().where(self.model.transaction_id == pk)

        for transaction in transactions:
            stores = StoreOfUserTransactionModel.select().where(
                StoreOfUserTransactionModel.transaction == transaction
            )

            for store in stores:
                products = ProductUserTransactionModel.select().where(
                    ProductUserTransactionModel.store == store
                )

                for product in products:
                    product.delete_instance()

                store.delete_instance()

            transaction.delete_instance()

    def keys(self):
        return [transaction.username for transaction in self.model.select()]
    def values(self):
        return self.get()

    def contains(self, transaction_id):
        query = self.model.select().where(self.model.transaction_id == transaction_id)
        return query.exists()
