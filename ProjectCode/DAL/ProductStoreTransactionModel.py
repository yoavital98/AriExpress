from peewee import *

from ProjectCode.DAL.StoreModel import StoreModel
from ProjectCode.DAL.StoreTransactionModel import StoreTransactionModel
from ProjectCode.DAL.database_conf import DatabaseConf


class ProductStoreTransactionModel(Model):

    class Meta:
        database = DatabaseConf.database
        db_table = 'product_store_transaction'


    product_id = IntegerField()
    product_name = CharField(max_length=100)
    quantity = IntegerField()
    price = DoubleField()
    store_transaction = ForeignKeyField(StoreTransactionModel, backref='product_store_transaction')

    # self._products = products  # set of tuples (product_id, product_name, quantity, price))