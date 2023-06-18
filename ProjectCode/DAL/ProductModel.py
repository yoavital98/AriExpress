from peewee import *

from ProjectCode.DAL.StoreModel import StoreModel
from ProjectCode.DAL.database_conf import DatabaseConf


class ProductModel(Model):

    class Meta:
        database = DatabaseConf.database
        db_table = 'product'

    product_id = IntegerField()
    store = ForeignKeyField(StoreModel, backref='products')
    name = CharField(max_length=100)
    quantity = IntegerField()
    price = IntegerField()
    categories = CharField(max_length=100)

