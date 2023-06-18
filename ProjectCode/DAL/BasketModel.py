from peewee import *

from ProjectCode.DAL.StoreModel import StoreModel
from ProjectCode.DAL.database_conf import DatabaseConf


class BasketModel(Model):

    class Meta:
        database = DatabaseConf.database
        db_table = 'basket'


    user_name = CharField(max_length=100)
    store = ForeignKeyField(StoreModel, backref='basket')
    #cart = ForeignKeyField(CartModel, backref='baskets')



