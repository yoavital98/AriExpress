from peewee import *


class CartModel(Model):

    class Meta:
        database = SqliteDatabase('database.db')
        db_table = 'cart'

    user_name = CharField(max_length=100, primary_key=True)
    #baskets = ManyToManyField(BasketModel, backref='cart')

