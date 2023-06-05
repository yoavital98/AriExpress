from peewee import *

from ProjectCode.DAL.StoreModel import StoreModel


class BasketModel(Model):

    class Meta:
        database = SqliteDatabase('database.db')
        db_table = 'basket'
        primary_key = CompositeKey('user_name', 'store')

    user_name = CharField(max_length=100)
    store = ForeignKeyField(StoreModel, backref='basket')
    #cart = ForeignKeyField(CartModel, backref='baskets')



