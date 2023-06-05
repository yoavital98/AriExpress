from peewee import *

from ProjectCode.DAL.BasketModel import BasketModel


class CartModel(Model):

    class Meta:
        database = SqliteDatabase('database.db')
        db_table = 'cart'

    user_name = CharField(max_length=100, primary_key=True)
    store_name = CharField(max_length=100, primary_key=True)

