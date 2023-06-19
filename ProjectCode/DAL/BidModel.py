from peewee import *

from ProjectCode.DAL.StoreModel import StoreModel
from ProjectCode.DAL.database_conf import DatabaseConf


class BidModel(Model):

    class Meta:
        database = DatabaseConf.database
        db_table = 'bid'

    bid_id = IntegerField(primary_key=True)
    user_name = CharField(max_length=100)
    store_name = CharField(max_length=100)
    offer = DoubleField()
    product_id = IntegerField()
    quantity = IntegerField()
    status = IntegerField()
    left_to_approval = IntegerField()
