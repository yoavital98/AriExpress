from peewee import *

from ProjectCode.DAL.StoreModel import StoreModel
from ProjectCode.DAL.StoreOfUserTransactionModel import StoreOfUserTransactionModel
from ProjectCode.DAL.StoreTransactionModel import StoreTransactionModel


class ProductStoreTransactionModel(Model):

    class Meta:
        database = SqliteDatabase('database.db')
        db_table = 'product_user_transaction'

    product_id = IntegerField(primary_key=True)
    product_name = CharField(max_length=100)
    quantity = IntegerField()
    price = DoubleField()
    store = ForeignKeyField(StoreOfUserTransactionModel, backref='product_user_transaction')
