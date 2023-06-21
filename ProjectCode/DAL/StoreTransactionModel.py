from peewee import *

from ProjectCode.DAL.StoreModel import StoreModel
from ProjectCode.DAL.database_conf import DatabaseConf


class StoreTransactionModel(Model):

    class Meta:
        database = DatabaseConf.database
        db_table = 'store_transaction'


    transaction_id = IntegerField()
    supply_id = IntegerField()
    store_name = CharField()
    user_name = CharField(max_length=100)
    overall_price = DoubleField()
    date = DateTimeField()

