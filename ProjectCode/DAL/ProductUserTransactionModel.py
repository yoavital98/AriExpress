from peewee import *

from ProjectCode.DAL.StoreModel import StoreModel
from ProjectCode.DAL.StoreOfUserTransactionModel import StoreOfUserTransactionModel
from ProjectCode.DAL.StoreTransactionModel import StoreTransactionModel
from ProjectCode.DAL.database_conf import DatabaseConf


class ProductUserTransactionModel(Model):

    class Meta:
        database = DatabaseConf.database
        db_table = 'product_user_transaction'

    product_id = IntegerField()
    product_name = CharField(max_length=100)
    quantity = IntegerField()
    price = DoubleField()
    store = ForeignKeyField(StoreOfUserTransactionModel, backref='product_user_transaction')
